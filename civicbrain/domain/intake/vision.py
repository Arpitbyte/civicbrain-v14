"""Computer Vision Protocol, Honest Cold-Start Triage & Fixture Detectors.

In strict accordance with:
- Hard Rule 1: No fabrication of model confidence or bounding boxes without real inference.
- Correction 1: citizen_declared observations always get confidence = None, never 1.0.
  Drop the 'or 1.0' branch entirely.
"""

from typing import Protocol

from pydantic import BaseModel, ConfigDict, Field


class DetectedDefect(BaseModel):
    """Atomic localized defect detected from photo analysis or citizen declaration."""

    model_config = ConfigDict(extra="forbid")

    category_code: str
    confidence: float | None = Field(
        default=None,
        description="Model confidence score in [0.0, 1.0]. Strictly None if no model evaluated.",
    )
    bbox: dict[str, float] | None = Field(
        default=None,
        description="Bounding box dict {'x': float, 'y': float, 'w': float, 'h': float} in [0, 1].",
    )
    severity_hint: int | None = Field(
        default=None,
        ge=1,
        le=5,
        description="Suggested severity tier 1-5 from model rubric matching.",
    )
    detection_source: str = Field(
        description="Provenance of detection: citizen_declared, test_fixture, model_yolo_world, unclassified",
    )
    needs_manual_triage: bool = Field(
        default=False,
        description="True if photo could not be autonomously classified and requires human triage.",
    )


class VisionDetector(Protocol):
    """Protocol for vision analysis backends."""

    async def detect(
        self,
        image_bytes: bytes,
        filename: str,
        citizen_categories: list[str] | None = None,
    ) -> list[DetectedDefect]:
        """Analyze image bytes and return list of detected defects."""
        ...


class HonestColdStartDetector:
    """Production web detector under zero-GPU and 512MB RAM constraints (Render free tier).

    Zero fabricated confidence scores. Zero fabricated bounding boxes.
    If citizen declared categories: assigns confidence = None (strictly never 1.0).
    If no categories declared: returns UNCLASSIFIED with confidence = None and needs_manual_triage = True.
    """

    async def detect(
        self,
        image_bytes: bytes,
        filename: str,
        citizen_categories: list[str] | None = None,
    ) -> list[DetectedDefect]:
        # If citizen explicitly selected categories, honor them with no fabricated confidence
        if citizen_categories and len(citizen_categories) > 0:
            defects: list[DetectedDefect] = []
            for cat in citizen_categories:
                clean_cat = cat.strip().upper()
                if not clean_cat:
                    continue
                defects.append(
                    DetectedDefect(
                        category_code=clean_cat,
                        confidence=None,  # Correction 1: citizen_declared observations always get confidence = None, never 1.0
                        bbox=None,
                        severity_hint=None,
                        detection_source="citizen_declared",
                        needs_manual_triage=False,
                    )
                )
            if defects:
                return defects

        # Cold-start arbitrary photo with no citizen categories:
        # Mark honestly as UNCLASSIFIED queued for human review.
        return [
            DetectedDefect(
                category_code="UNCLASSIFIED",
                confidence=None,
                bbox=None,
                severity_hint=None,
                detection_source="unclassified",
                needs_manual_triage=True,
            )
        ]


class FixtureVisionDetector:
    """Deterministic fixture detector for multi-defect pipeline testing and CI.

    Produces realistic bounding boxes and department routing solely for pre-defined test assets.
    """

    FIXTURES: dict[str, list[DetectedDefect]] = {
        "multi_issue_road_swm.jpg": [
            DetectedDefect(
                category_code="POTHOLE",
                confidence=0.92,
                bbox={"x": 0.15, "y": 0.55, "w": 0.30, "h": 0.25},
                severity_hint=3,
                detection_source="test_fixture",
                needs_manual_triage=False,
            ),
            DetectedDefect(
                category_code="GARBAGE",
                confidence=0.88,
                bbox={"x": 0.65, "y": 0.40, "w": 0.28, "h": 0.35},
                severity_hint=2,
                detection_source="test_fixture",
                needs_manual_triage=False,
            ),
        ],
        "single_issue_street_light.jpg": [
            DetectedDefect(
                category_code="STREET_LIGHT",
                confidence=0.95,
                bbox={"x": 0.40, "y": 0.10, "w": 0.20, "h": 0.45},
                severity_hint=4,
                detection_source="test_fixture",
                needs_manual_triage=False,
            )
        ],
    }

    def __init__(self, fallback_detector: VisionDetector | None = None) -> None:
        self.fallback = fallback_detector or HonestColdStartDetector()

    async def detect(
        self,
        image_bytes: bytes,
        filename: str,
        citizen_categories: list[str] | None = None,
    ) -> list[DetectedDefect]:
        # Check if filename or substring matches a known fixture
        for fixture_name, defects in self.FIXTURES.items():
            if fixture_name in filename.lower():
                return [d.model_copy() for d in defects]

        return await self.fallback.detect(image_bytes, filename, citizen_categories)


# Default global detector instance for application dependency injection
default_vision_detector: VisionDetector = HonestColdStartDetector()


def get_vision_detector() -> VisionDetector:
    """Dependency provider for FastAPI route handlers."""
    return default_vision_detector
