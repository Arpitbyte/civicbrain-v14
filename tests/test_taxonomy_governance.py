"""Unit tests for Living Taxonomy Governance (§A11, Standing Invariant 1).

Guarantees:
- Approval strictly requires a validated 5-level severity rubric.
- Incomplete rubrics (<5 levels, duplicate tiers, short criteria) are rejected.
- Decoupled from static AHP criteria weights.
- Categories can be proposed in 'proposed' state and approved by admin.
"""

import pytest
from pydantic import ValidationError

from civicbrain.domain.intake.taxonomy import (
    CategoryStatus,
    RubricLevel,
    SeverityRubric,
    create_default_rubric,
)


def test_default_rubric_generator():
    """Verify create_default_rubric generates all 5 required tiers with valid criteria and scores."""
    rubric = create_default_rubric("Pothole")
    assert len(rubric.levels) == 5
    tiers = [lvl.level for lvl in rubric.levels]
    assert tiers == [1, 2, 3, 4, 5]
    for lvl in rubric.levels:
        assert len(lvl.criteria) >= 10
        assert 1.0 <= lvl.baseline_score <= 5.0
    assert rubric.buhlmann_k == 10.0


def test_severity_rubric_validation_success():
    """Verify valid 5-level rubric passes schema validation."""
    levels = [
        RubricLevel(
            level=1, criteria="Surface hairline cracks, no structural impact", baseline_score=1.0
        ),
        RubricLevel(
            level=2, criteria="Shallow depression under 2 inches depth", baseline_score=2.0
        ),
        RubricLevel(
            level=3, criteria="Deep crater between 2 and 4 inches depth", baseline_score=3.0
        ),
        RubricLevel(level=4, criteria="Severe crater exceeding 4 inches depth", baseline_score=4.0),
        RubricLevel(
            level=5, criteria="Catastrophic roadway collapse or breach", baseline_score=5.0
        ),
    ]
    rubric = SeverityRubric(levels=levels, buhlmann_k=8.5)
    assert len(rubric.levels) == 5
    assert rubric.buhlmann_k == 8.5


def test_severity_rubric_rejects_missing_levels():
    """Verify rubric with fewer than 5 levels is strictly rejected."""
    levels = [
        RubricLevel(level=1, criteria="Minor surface wear and tear", baseline_score=1.0),
        RubricLevel(level=2, criteria="Moderate surface wear and tear", baseline_score=2.0),
        RubricLevel(level=4, criteria="Major degradation of surface", baseline_score=4.0),
        RubricLevel(level=5, criteria="Total failure of road surface", baseline_score=5.0),
    ]
    with pytest.raises(ValidationError):
        SeverityRubric(levels=levels)


def test_severity_rubric_rejects_duplicate_levels():
    """Verify rubric with 5 items but duplicate tiers (missing a tier) is rejected."""
    levels = [
        RubricLevel(level=1, criteria="Minor surface wear and tear", baseline_score=1.0),
        RubricLevel(level=2, criteria="Moderate surface wear and tear", baseline_score=2.0),
        RubricLevel(level=2, criteria="Duplicate tier two criteria here", baseline_score=2.5),
        RubricLevel(level=4, criteria="Major degradation of surface", baseline_score=4.0),
        RubricLevel(level=5, criteria="Total failure of road surface", baseline_score=5.0),
    ]
    with pytest.raises(ValidationError) as exc_info:
        SeverityRubric(levels=levels)
    assert "Severity rubric must contain exactly tiers 1 through 5" in str(exc_info.value)


def test_severity_rubric_rejects_short_criteria():
    """Verify criteria description must be at least 10 characters."""
    with pytest.raises(ValidationError):
        RubricLevel(level=1, criteria="Too short", baseline_score=1.0)


def test_severity_rubric_rejects_out_of_bounds_scores():
    """Verify baseline scores outside [1.0, 5.0] are rejected."""
    with pytest.raises(ValidationError):
        RubricLevel(level=1, criteria="Valid criteria text for testing", baseline_score=0.5)

    with pytest.raises(ValidationError):
        RubricLevel(level=5, criteria="Valid criteria text for testing", baseline_score=5.5)


def test_category_status_enum_values():
    """Verify category_status_enum contains proposed, approved, deprecated."""
    assert CategoryStatus.PROPOSED == "proposed"
    assert CategoryStatus.APPROVED == "approved"
    assert CategoryStatus.DEPRECATED == "deprecated"
