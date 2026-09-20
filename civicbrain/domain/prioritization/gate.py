"""Confidence-Gated Incident Evaluation and Dispatch Routing (§A12, §A13).

When overall confidence is low and priority is high, routes to human review
instead of auto-proceeding to dispatch.
"""

from dataclasses import dataclass

from civicbrain.domain.intake.models import IncidentStatus
from civicbrain.domain.prioritization.ahp import CriteriaSubscores, calculate_raw_priority

# Thresholds for confidence gating
DEFAULT_PRIORITY_THRESHOLD: float = 70.0
DEFAULT_CONFIDENCE_THRESHOLD: float = 0.50


@dataclass(frozen=True)
class PrioritizationResult:
    """Itemized glass-box evaluation breakdown."""

    raw_priority_score: float
    equity_boost: float
    final_priority_score: float
    confidence_score: float
    requires_human_review: bool
    review_reason: str | None
    target_status: IncidentStatus


def evaluate_confidence_gate(
    subscores: CriteriaSubscores,
    weights: dict[str, float],
    equity_boost: float,
    confidence_score: float,
    priority_threshold: float = DEFAULT_PRIORITY_THRESHOLD,
    confidence_threshold: float = DEFAULT_CONFIDENCE_THRESHOLD,
) -> PrioritizationResult:
    """Evaluate 5 subscores, add equity boost, and apply the confidence gate."""
    raw_p = calculate_raw_priority(subscores, weights)
    # Final priority on [0.0, 100.0] scale
    final_p = round(min(100.0, (raw_p + equity_boost) * 100.0), 6)
    conf = round(float(confidence_score), 6)

    # Confidence Gating Rule (§A12, §A13):
    # When priority is high but confidence is low, hold back from auto-dispatch.
    if final_p >= priority_threshold and conf < confidence_threshold:
        requires_review = True
        reason = "high_priority_low_confidence"
        status = IncidentStatus.TRIAGED
    else:
        requires_review = False
        reason = None
        status = IncidentStatus.PRIORITIZED

    return PrioritizationResult(
        raw_priority_score=raw_p,
        equity_boost=round(equity_boost, 6),
        final_priority_score=final_p,
        confidence_score=conf,
        requires_human_review=requires_review,
        review_reason=reason,
        target_status=status,
    )
