"""Unit tests for Splink deduplication integration under provisional cold-start rules."""

from civicbrain.domain.intake.dedup import (
    calculate_jaro_winkler_similarity,
    evaluate_splink_record_linkage,
)
from civicbrain.domain.intake.models import DedupDecision


def test_jaro_winkler_similarity():
    """Verify deterministic string similarity calculation."""
    assert calculate_jaro_winkler_similarity("pothole", "pothole") == 1.0
    assert (
        calculate_jaro_winkler_similarity("pothole on main road deep", "pothole on main road") > 0.8
    )
    assert calculate_jaro_winkler_similarity("garbage dump", "broken streetlight") < 0.5
    assert calculate_jaro_winkler_similarity(None, "pothole") == 0.0


def test_splink_cold_start_dedup_exact_match():
    """Verify that co-located defect (<=15m) within 72h window and matching category is an exact match."""
    # 5 meters distance, 2 hours diff, category match, high similarity
    weight, prob, decision = evaluate_splink_record_linkage(
        distance_meters=5.0,
        diff_seconds=7200.0,
        category_match=True,
        text_similarity=0.85,
    )
    assert decision == DedupDecision.EXACT_MATCH
    assert prob >= 0.85
    assert weight > 0.0


def test_splink_cold_start_dedup_distinct():
    """Verify that far-away defect (>50m) or different category is marked distinct."""
    # 150 meters distance, 12 hours diff, same category
    weight, prob, decision = evaluate_splink_record_linkage(
        distance_meters=150.0,
        diff_seconds=43200.0,
        category_match=True,
        text_similarity=0.2,
    )
    assert decision == DedupDecision.DISTINCT
    assert prob < 0.50

    # 10 meters distance, but completely different category
    weight2, prob2, decision2 = evaluate_splink_record_linkage(
        distance_meters=10.0,
        diff_seconds=3600.0,
        category_match=False,
        text_similarity=0.1,
    )
    assert decision2 == DedupDecision.DISTINCT
    assert prob2 < 0.50
