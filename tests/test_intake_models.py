"""Unit tests for Phase 2 domain models, §A16 lifecycle, and least-advanced aggregation."""

from civicbrain.domain.intake.models import (
    IncidentStatus,
    IntakeStatus,
)
from civicbrain.domain.intake.services import (
    calculate_intake_status_from_children,
)


def test_incident_status_enum_values():
    """Verify incident_status_enum covers all 11 states per §A16."""
    expected_states = {
        "reported",
        "triaged",
        "verified",
        "prioritized",
        "assigned",
        "in_progress",
        "resolved",
        "confirmed",
        "rejected",
        "appealed",
        "reopened",
    }
    actual_states = {s.value for s in IncidentStatus}
    assert expected_states == actual_states


def test_least_advanced_child_status_aggregation():
    """Verify §A7 & Standing Invariant 3 least-advanced aggregation logic."""
    # Case 1: One resolved, one in progress -> in_progress (partially_resolved)
    status = calculate_intake_status_from_children(
        [IncidentStatus.RESOLVED, IncidentStatus.IN_PROGRESS]
    )
    assert status == IntakeStatus.PARTIALLY_RESOLVED

    # Case 2: One in_progress, one triaged -> processing
    status = calculate_intake_status_from_children(
        [IncidentStatus.IN_PROGRESS, IncidentStatus.TRIAGED]
    )
    assert status == IntakeStatus.PROCESSING

    # Case 3: All resolved -> resolved
    status = calculate_intake_status_from_children(
        [IncidentStatus.RESOLVED, IncidentStatus.RESOLVED]
    )
    assert status == IntakeStatus.RESOLVED

    # Case 4: All confirmed -> closed
    status = calculate_intake_status_from_children(
        [IncidentStatus.CONFIRMED, IncidentStatus.CONFIRMED]
    )
    assert status == IntakeStatus.CLOSED

    # Case 5: All rejected -> rejected
    status = calculate_intake_status_from_children(
        [IncidentStatus.REJECTED, IncidentStatus.REJECTED]
    )
    assert status == IntakeStatus.REJECTED

    # Case 6: One rejected, one in_progress -> in_progress (rejected is filtered out)
    status = calculate_intake_status_from_children(
        [IncidentStatus.REJECTED, IncidentStatus.IN_PROGRESS]
    )
    assert status == IntakeStatus.IN_PROGRESS

    # Case 7: One resolved, one appealed -> in_progress (appealed pulls back to active)
    status = calculate_intake_status_from_children(
        [IncidentStatus.RESOLVED, IncidentStatus.APPEALED]
    )
    assert status == IntakeStatus.PARTIALLY_RESOLVED

    # Case 8: Only appealed -> in_progress
    status = calculate_intake_status_from_children([IncidentStatus.APPEALED])
    assert status == IntakeStatus.IN_PROGRESS

    # Case 9: Only reopened -> in_progress
    status = calculate_intake_status_from_children([IncidentStatus.REOPENED])
    assert status == IntakeStatus.IN_PROGRESS
