"""Unit & integration tests for Computer Vision protocol and Multi-Issue Photo-Splitting.

In strict accordance with:
- Hard Rule 1: No fabrication of model confidence or bounding boxes without real model execution.
- Correction 1: citizen_declared observations always get confidence = None, never 1.0.
  Drop the 'or 1.0' branch entirely.
- Standing Invariant 3: Parent intake report status is strictly the least-advanced child status.
"""

import uuid

import pytest

from civicbrain.domain.identity.models import Department, Organization, Ward, Zone
from civicbrain.domain.intake.models import (
    IntakeChannel,
    IntakeStatus,
    ObservationStatus,
)
from civicbrain.domain.intake.services import (
    process_photo_intake,
)
from civicbrain.domain.intake.taxonomy import (
    CategoryStatus,
    TaxonomyCategory,
    create_default_rubric,
)
from civicbrain.domain.intake.vision import (
    FixtureVisionDetector,
    HonestColdStartDetector,
)


@pytest.mark.asyncio
async def test_cold_start_arbitrary_photo_honest_triage():
    """Verify arbitrary photo in cold-start produces UNCLASSIFIED with confidence=None and needs_manual_triage=True."""
    detector = HonestColdStartDetector()
    image_bytes = b"\xff\xd8\xff\xe0arbitrary_camera_capture_jpeg"
    defects = await detector.detect(
        image_bytes, "unknown_citizen_photo.jpg", citizen_categories=None
    )

    assert len(defects) == 1
    defect = defects[0]
    assert defect.category_code == "UNCLASSIFIED"
    # Hard Rule 1: Zero fabricated confidence scores
    assert defect.confidence is None
    # Zero fabricated bounding box coordinates
    assert defect.bbox is None
    assert defect.needs_manual_triage is True
    assert defect.detection_source == "unclassified"


@pytest.mark.asyncio
async def test_citizen_declared_confidence_strictly_none():
    """Verify citizen_declared observations always get confidence = None, never 1.0 (Correction 1)."""
    detector = HonestColdStartDetector()
    image_bytes = b"\xff\xd8\xff\xe0pothole_photo_jpeg"
    citizen_categories = ["POTHOLE", "GARBAGE"]
    defects = await detector.detect(
        image_bytes, "citizen_pothole.jpg", citizen_categories=citizen_categories
    )

    assert len(defects) == 2
    for defect in defects:
        assert defect.detection_source == "citizen_declared"
        # User Correction 1: confidence must be None, strictly NEVER 1.0
        assert defect.confidence is None
        assert defect.bbox is None
        assert defect.needs_manual_triage is False

    codes = [d.category_code for d in defects]
    assert "POTHOLE" in codes
    assert "GARBAGE" in codes


@pytest.mark.asyncio
async def test_fixture_vision_detector_deterministic_multi_issue():
    """Verify FixtureVisionDetector loads pre-annotated multi-defect ground-truth for testing."""
    fixture_detector = FixtureVisionDetector()
    image_bytes = b"synthetic_fixture_bytes"
    defects = await fixture_detector.detect(image_bytes, "test_multi_issue_road_swm.jpg")

    assert len(defects) == 2
    pothole = next(d for d in defects if d.category_code == "POTHOLE")
    garbage = next(d for d in defects if d.category_code == "GARBAGE")

    assert pothole.confidence == 0.92
    assert pothole.bbox == {"x": 0.15, "y": 0.55, "w": 0.30, "h": 0.25}
    assert pothole.detection_source == "test_fixture"
    assert pothole.needs_manual_triage is False

    assert garbage.confidence == 0.88
    assert garbage.bbox == {"x": 0.65, "y": 0.40, "w": 0.28, "h": 0.35}
    assert garbage.detection_source == "test_fixture"
    assert garbage.needs_manual_triage is False


@pytest.mark.asyncio
async def test_process_photo_intake_multi_department_splitting():
    """Verify photo splitting pipeline splits defects into atomic observations across distinct departments."""
    from civicbrain.infra.database import async_session_maker

    async with async_session_maker() as session:
        org_id = None
        try:
            # 1. Seed Organization, Ward, and 2 distinct Departments (ROADS and SWM)
            org = Organization(
                name="Bruhat Bengaluru Mahanagara Palike",
                code=f"BBMP_{uuid.uuid4().hex[:6]}",
                ulb_type="municipal_corporation",
                state="Karnataka",
            )
            session.add(org)
            await session.flush()
            org_id = org.id

            dept_roads = Department(
                organization_id=org.id, name="Roads & Infrastructure", code="ROADS"
            )
            dept_swm = Department(organization_id=org.id, name="Solid Waste Management", code="SWM")
            session.add_all([dept_roads, dept_swm])
            await session.flush()

            # Create containing zone and ward boundary around (77.5946, 12.9716)
            zone = Zone(
                organization_id=org.id,
                name="Central Zone",
                code=f"CZ_{uuid.uuid4().hex[:4]}",
                geom="SRID=4326;POLYGON((77.50 12.90, 77.70 12.90, 77.70 13.05, 77.50 13.05, 77.50 12.90))",
            )
            session.add(zone)
            await session.flush()

            ward = Ward(
                organization_id=org.id,
                zone_id=zone.id,
                name="Shantala Nagar",
                ward_number=111,
                code=f"WARD_{uuid.uuid4().hex[:4]}",
                geom="SRID=4326;POLYGON((77.58 12.96, 77.61 12.96, 77.61 12.98, 77.58 12.98, 77.58 12.96))",
            )
            session.add(ward)
            await session.flush()

            # 2. Seed approved Living Taxonomy categories for POTHOLE and GARBAGE
            cat_pothole = TaxonomyCategory(
                organization_id=org.id,
                department_id=dept_roads.id,
                code="POTHOLE",
                name="Pothole / Road Surface Defect",
                severity_rubric=create_default_rubric("Pothole").model_dump(),
                status=CategoryStatus.APPROVED,
                is_active=True,
            )
            cat_garbage = TaxonomyCategory(
                organization_id=org.id,
                department_id=dept_swm.id,
                code="GARBAGE",
                name="Garbage Dump / Waste Overflow",
                severity_rubric=create_default_rubric("Garbage").model_dump(),
                status=CategoryStatus.APPROVED,
                is_active=True,
            )
            session.add_all([cat_pothole, cat_garbage])
            await session.commit()

            # 3. Ingest multi-issue photo using FixtureVisionDetector
            fixture_detector = FixtureVisionDetector()
            report, observations = await process_photo_intake(
                session=session,
                organization_id=org.id,
                image_bytes=b"dummy_image_bytes",
                filename="multi_issue_road_swm.jpg",
                latitude=12.9716,
                longitude=77.5946,
                channel=IntakeChannel.PWA,
                detector=fixture_detector,
            )
            await session.commit()

            # Verify parent report
            assert report.id is not None
            assert report.ward_id == ward.id
            assert report.status == IntakeStatus.SUBMITTED
            assert report.tracking_token is not None and len(report.tracking_token) >= 16

            # Verify atomic observations were routed to different departments
            assert len(observations) == 2
            obs_roads = next(o for o in observations if o.category_code == "POTHOLE")
            obs_swm = next(o for o in observations if o.category_code == "GARBAGE")

            assert obs_roads.department_id == dept_roads.id
            assert obs_roads.confidence == 0.92
            assert obs_roads.bbox is not None
            assert obs_roads.status == ObservationStatus.LINKED_TO_INCIDENT
            assert obs_roads.incident_id is not None

            assert obs_swm.department_id == dept_swm.id
            assert obs_swm.confidence == 0.88
            assert obs_swm.bbox is not None
            assert obs_swm.status == ObservationStatus.LINKED_TO_INCIDENT
            assert obs_swm.incident_id is not None

            # Observations belong to distinct operational incidents for their respective departments
            assert obs_roads.incident_id != obs_swm.incident_id
        finally:
            if org_id:
                await session.rollback()
                from sqlalchemy import delete

                await session.execute(delete(Organization).where(Organization.id == org_id))
                await session.commit()


@pytest.mark.asyncio
async def test_process_photo_intake_cold_start_arbitrary_unclassified():
    """Verify arbitrary photo in cold start creates an UNCLASSIFIED observation needing manual triage."""
    from civicbrain.infra.database import async_session_maker

    async with async_session_maker() as session:
        org_id = None
        try:
            org = Organization(
                name="Chennai Municipal Corporation",
                code=f"CMC_{uuid.uuid4().hex[:6]}",
                ulb_type="municipal_corporation",
                state="Tamil Nadu",
            )
            session.add(org)
            await session.flush()
            org_id = org.id

            dept = Department(organization_id=org.id, name="General Administration", code="GENERAL")
            session.add(dept)
            await session.flush()

            zone = Zone(
                organization_id=org.id,
                name="North Zone",
                code=f"NZ_{uuid.uuid4().hex[:4]}",
                geom="SRID=4326;POLYGON((80.10 12.90, 80.40 12.90, 80.40 13.20, 80.10 13.20, 80.10 12.90))",
            )
            session.add(zone)
            await session.flush()

            ward = Ward(
                organization_id=org.id,
                zone_id=zone.id,
                name="Ward 1",
                ward_number=1,
                code=f"W_{uuid.uuid4().hex[:4]}",
                geom="SRID=4326;POLYGON((80.20 13.00, 80.30 13.00, 80.30 13.10, 80.20 13.10, 80.20 13.00))",
            )
            session.add(ward)
            await session.commit()

            # Honest cold-start detector
            cold_detector = HonestColdStartDetector()
            report, observations = await process_photo_intake(
                session=session,
                organization_id=org.id,
                image_bytes=b"arbitrary_unlabeled_photo",
                filename="arbitrary_unlabeled_photo.jpg",
                latitude=13.05,
                longitude=80.25,
                channel=IntakeChannel.PWA,
                detector=cold_detector,
            )
            await session.commit()

            assert len(observations) == 1
            obs = observations[0]
            assert obs.category_code == "UNCLASSIFIED"
            assert obs.confidence is None  # Hard Rule 1
            assert obs.bbox is None
            assert obs.needs_manual_triage is True
            assert obs.status == ObservationStatus.DETECTED
            assert obs.incident_id is None  # Queued for manual triage, not auto-routed
            assert report.status == IntakeStatus.SUBMITTED
        finally:
            if org_id:
                await session.rollback()
                from sqlalchemy import delete

                await session.execute(delete(Organization).where(Organization.id == org_id))
                await session.commit()
