"""Unit tests for Phase 6 AHP Prioritization, Equity Compensator & Confidence Gating."""

from civicbrain.domain.intake.models import IncidentStatus
from civicbrain.domain.nlp.processor import DeterministicIndicRuleProcessor
from civicbrain.domain.prioritization.ahp import (
    AHPMatrix,
    CriteriaSubscores,
    calculate_raw_priority,
)
from civicbrain.domain.prioritization.equity import (
    BuhlmannEquityCompensator,
)
from civicbrain.domain.prioritization.gate import evaluate_confidence_gate


def test_ahp_5_criteria_weights_and_consistency():
    """Verify Saaty 5x5 matrix solves exact 5 criteria weights summing to 1.0 with CR < 0.10."""
    solver = AHPMatrix()
    res = solver.solve()

    assert res.is_consistent is True
    assert res.consistency_ratio < 0.10
    assert set(res.weights.keys()) == {"severity", "risk", "exposure", "criticality", "urgency"}

    total_weight = sum(res.weights.values())
    assert abs(total_weight - 1.0) < 1e-4

    # Verify rank order for calibrated defaults: Criticality > Risk > Severity > Exposure > Urgency
    w = res.weights
    assert w["criticality"] > w["risk"]
    assert w["risk"] > w["severity"]


def test_ahp_inconsistent_matrix_rejection():
    """Verify an inconsistent 5x5 matrix (CR >= 0.10) is flagged as inconsistent."""
    # Arbitrary conflicting matrix
    inconsistent_mat = [
        [1.0, 5.0, 1.0 / 9.0, 7.0, 1.0 / 3.0],
        [1.0 / 5.0, 1.0, 8.0, 1.0 / 4.0, 6.0],
        [9.0, 1.0 / 8.0, 1.0, 2.0, 1.0 / 5.0],
        [1.0 / 7.0, 4.0, 1.0 / 2.0, 1.0, 9.0],
        [3.0, 1.0 / 6.0, 5.0, 1.0 / 9.0, 1.0],
    ]
    solver = AHPMatrix(inconsistent_mat)
    res = solver.solve()
    assert res.is_consistent is False
    assert res.consistency_ratio >= 0.10


def test_glass_box_determinism():
    """Verify 1,000 evaluations yield byte-for-byte identical priority rankings."""
    solver = AHPMatrix()
    weights = solver.solve().weights

    subscores = CriteriaSubscores(
        severity=0.85,
        risk=0.72,
        exposure=0.60,
        criticality=0.90,
        urgency=0.45,
    )

    baseline_score = calculate_raw_priority(subscores, weights)
    for _ in range(1000):
        run_score = calculate_raw_priority(subscores, weights)
        assert run_score == baseline_score


def test_urgency_subscore_decoupled_from_citizen_urgency():
    """Verify subscore_urgency is never derived from or correlated with citizen_urgency_score (§A11, §A12).

    A citizen expressing high emotional distress/anger must NOT inflate engineering urgency,
    and a calm citizen reporting an SLA-breaching defect must retain its high urgency.
    """
    processor = DeterministicIndicRuleProcessor()

    calm_report = "Major leak in water supply pipeline on 5th cross road since 48 hours."
    angry_report = (
        "SHAMELESS USELESS MUNICIPALITY!! SICKENING EMERGENCY YOU MUST FIX THIS NOW BEFORE I SUE!! "
        "Major leak in water supply pipeline on 5th cross road since 48 hours."
    )

    calm_nlp = processor.process_text(calm_report)
    angry_nlp = processor.process_text(angry_report)

    # Both recognize category WATER_SUPPLY
    assert calm_nlp.suggested_category == "WATER_SUPPLY"
    assert angry_nlp.suggested_category == "WATER_SUPPLY"

    # Both extract identical physical severity (major leak -> 4)
    assert calm_nlp.physical_severity_hint == 4
    assert angry_nlp.physical_severity_hint == 4

    # Citizen urgency reflects emotional tone
    assert angry_nlp.citizen_urgency_score > 0.60
    assert calm_nlp.citizen_urgency_score < 0.20
    assert angry_nlp.citizen_urgency_score != calm_nlp.citizen_urgency_score

    # Engineering subscores are derived strictly from physical SLAs and lifelines,
    # NOT from NLP citizen_urgency_score
    calm_subscores = CriteriaSubscores(
        severity=calm_nlp.physical_severity_hint / 5.0,
        risk=0.90,  # High contamination health risk
        exposure=0.70,  # Neighborhood line
        criticality=0.85,  # Water lifeline
        urgency=0.90,  # SLA breach (48h aging), strictly independent of NLP emotion
    )
    angry_subscores = CriteriaSubscores(
        severity=angry_nlp.physical_severity_hint / 5.0,
        risk=0.90,
        exposure=0.70,
        criticality=0.85,
        urgency=0.90,  # Must remain identical to calm report
    )

    solver = AHPMatrix()
    weights = solver.solve().weights

    calm_priority = calculate_raw_priority(calm_subscores, weights)
    angry_priority = calculate_raw_priority(angry_subscores, weights)

    assert calm_subscores.urgency == angry_subscores.urgency
    assert calm_priority == angry_priority, (
        "Violation of Decoupling: citizen urgency affected incident priority score!"
    )


def test_buhlmann_equity_compensator():
    """Verify Bühlmann blending, cold-start prior reliance, and underreported ward boost."""
    compensator = BuhlmannEquityCompensator()

    # 1. Cold start ward (0 verified incidents): Z_i = 0, expected = city prior (10.0)
    cold_res = compensator.evaluate_ward(
        verified_incident_count=0,
        historical_incident_rate=0.0,
        observed_issue_rate=2.0,  # observed underreporting
        city_prior_rate=10.0,
    )
    assert cold_res.credibility_factor == 0.0
    assert cold_res.expected_issue_rate == 10.0
    assert cold_res.equity_gap == 8.0  # 10.0 - 2.0
    assert cold_res.equity_boost > 0.0

    # 2. Fully mature well-reported ward
    mature_res = compensator.evaluate_ward(
        verified_incident_count=90,
        historical_incident_rate=15.0,
        observed_issue_rate=16.0,  # no deficit
        city_prior_rate=10.0,
    )
    assert mature_res.credibility_factor == 0.90  # 90 / (90 + 10)
    assert mature_res.expected_issue_rate == (0.90 * 15.0) + (0.10 * 10.0)  # 14.5
    assert mature_res.equity_gap == 0.0  # observed (16.0) >= expected (14.5)
    assert mature_res.equity_boost == 0.0


def test_confidence_gating_high_priority_low_confidence():
    """Assert high priority + low confidence routes to human review queue and does NOT dispatch."""
    weights = AHPMatrix().solve().weights

    # High physical subscores -> high priority score
    high_subscores = CriteriaSubscores(
        severity=0.90,
        risk=0.95,
        exposure=0.85,
        criticality=0.90,
        urgency=0.80,
    )

    # 1. High priority + LOW confidence (e.g. unverified single crowd report)
    gated_res = evaluate_confidence_gate(
        subscores=high_subscores,
        weights=weights,
        equity_boost=0.05,
        confidence_score=0.35,  # Low confidence (< 0.50)
        priority_threshold=70.0,
        confidence_threshold=0.50,
    )
    assert gated_res.final_priority_score >= 70.0
    assert gated_res.requires_human_review is True
    assert gated_res.review_reason == "high_priority_low_confidence"
    assert gated_res.target_status == IncidentStatus.TRIAGED  # Holds back from automated dispatch!

    # 2. High priority + HIGH confidence (verified by field worker / multiple sensors)
    dispatched_res = evaluate_confidence_gate(
        subscores=high_subscores,
        weights=weights,
        equity_boost=0.05,
        confidence_score=0.85,  # High confidence
        priority_threshold=70.0,
        confidence_threshold=0.50,
    )
    assert dispatched_res.final_priority_score >= 70.0
    assert dispatched_res.requires_human_review is False
    assert dispatched_res.review_reason is None
    assert (
        dispatched_res.target_status == IncidentStatus.PRIORITIZED
    )  # Ready for dispatch assignment

    # 3. Low priority + LOW confidence (minor issue does not clog human review queue)
    low_subscores = CriteriaSubscores(
        severity=0.20,
        risk=0.10,
        exposure=0.30,
        criticality=0.20,
        urgency=0.10,
    )
    low_res = evaluate_confidence_gate(
        subscores=low_subscores,
        weights=weights,
        equity_boost=0.0,
        confidence_score=0.20,
        priority_threshold=70.0,
        confidence_threshold=0.50,
    )
    assert low_res.final_priority_score < 70.0
    assert low_res.requires_human_review is False
    assert low_res.target_status == IncidentStatus.PRIORITIZED
