"""Unit tests for Phase 5 NLP Pipeline & Emotion-Severity Decoupling (§A11)."""

import uuid
from datetime import UTC, datetime, timedelta

import jwt
import pytest
from httpx import ASGITransport, AsyncClient

from civicbrain.domain.nlp.processor import DeterministicIndicRuleProcessor
from civicbrain.infra.config import settings
from civicbrain.main import app


def test_emotion_severity_decoupling():
    """Verify citizen emotional intensity and anger NEVER inflate physical engineering severity (§A11)."""
    processor = DeterministicIndicRuleProcessor()

    calm_text = "There is a deep pothole on 8th main road."
    angry_text = (
        "SHAME ON BBMP!! THIS IS RIDICULOUS AND DANGEROUS EMERGENCY ACCIDENT WAITING TO HAPPEN!! "
        "There is a deep pothole on 8th main road!!!!"
    )

    calm_res = processor.process_text(calm_text)
    angry_res = processor.process_text(angry_text)

    # 1. Physical engineering severity MUST be identical (both detect 'deep' -> severity 4)
    assert calm_res.physical_severity_hint == 4
    assert angry_res.physical_severity_hint == 4
    assert calm_res.physical_severity_hint == angry_res.physical_severity_hint, (
        "Emotion-Severity Decoupling violation! Angry text inflated physical severity."
    )

    # 2. Both recognize category POTHOLE
    assert calm_res.suggested_category == "POTHOLE"
    assert angry_res.suggested_category == "POTHOLE"

    # 3. Citizen urgency score MUST reflect the emotional distress in the angry report
    assert calm_res.citizen_urgency_score < 0.20
    assert angry_res.citizen_urgency_score >= 0.70
    assert angry_res.citizen_urgency_score > calm_res.citizen_urgency_score


def test_multilingual_and_romanized_ingestion():
    """Verify script detection and category resolution across Hindi, Kannada, Tamil, and Hinglish."""
    processor = DeterministicIndicRuleProcessor()

    # Hindi Devanagari (Pothole)
    hi_res = processor.process_text("सड़क पर बहुत बड़ा गड्ढा है")
    assert hi_res.detected_language == "hi"
    assert hi_res.detected_script == "Devanagari"
    assert hi_res.suggested_category == "POTHOLE"

    # Kannada (Pothole)
    kn_res = processor.process_text("ರಸ್ತೆಯಲ್ಲಿ ದೊಡ್ಡ ಗುಂಡಿ ಬಿದ್ದಿದೆ")
    assert kn_res.detected_language == "kn"
    assert kn_res.detected_script == "Kannada"
    assert kn_res.suggested_category == "POTHOLE"

    # Tamil (Streetlight)
    ta_res = processor.process_text("தெருவிளக்கு எரியவில்லை")
    assert ta_res.detected_language == "ta"
    assert ta_res.detected_script == "Tamil"
    assert ta_res.suggested_category == "STREETLIGHT"

    # Hinglish / Romanized (Pothole + Urgency)
    hinglish_res = processor.process_text("rasta par bahut bada khadda hai jaldi fix karo!")
    assert hinglish_res.detected_language == "hinglish"
    assert hinglish_res.detected_script == "Latin"
    assert hinglish_res.suggested_category == "POTHOLE"
    assert "khadda" in hinglish_res.extracted_keywords
    assert hinglish_res.citizen_urgency_score > 0.0

    # Garbage in Hindi
    garbage_res = processor.process_text("कॉलोनी में कचरा बहुत दिनों से नहीं उठाया गया")
    assert garbage_res.suggested_category == "GARBAGE"

    # Drainage in Kannada
    drain_res = processor.process_text("ಚರಂಡಿ ನೀರು ರಸ್ತೆಗೆ ಹರಿಯುತ್ತಿದೆ")
    assert drain_res.suggested_category == "DRAINAGE"


def test_cold_start_honesty_on_unrecognized_text():
    """Verify unrecognized text returns suggested_category = None and flags human triage (Hard Rule 1, §A3)."""
    processor = DeterministicIndicRuleProcessor()

    res = processor.process_text("Good morning everyone hope you have a nice day ahead.")
    assert res.suggested_category is None
    assert res.physical_severity_hint is None
    assert res.requires_human_triage is True


@pytest.mark.asyncio
async def test_nlp_analyze_api_auth_enforcement():
    """Verify POST /v1/nlp/analyze requires authentication and rejects unauthenticated calls."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # 1. Unauthenticated call must be rejected with 401
        res_unauth = await client.post(
            "/v1/nlp/analyze",
            json={"text": "Large pothole on 10th cross road"},
        )
        assert res_unauth.status_code == 401

        # 2. Authenticated call with valid mock token succeeds
        fake_uid = str(uuid.uuid4())
        token = jwt.encode(
            {
                "sub": fake_uid,
                "role": "admin",
                "exp": datetime.now(UTC) + timedelta(hours=1),
            },
            settings.SECRET_KEY,
            algorithm="HS256",
        )
        headers = {"Authorization": f"Bearer {token}"}

        res_auth = await client.post(
            "/v1/nlp/analyze",
            json={"text": "Massive crater on 10th cross road!! Emergency!!"},
            headers=headers,
        )
        assert res_auth.status_code == 200
        data = res_auth.json()
        assert data["suggested_category"] == "POTHOLE"
        assert data["physical_severity_hint"] == 5  # 'massive crater'
        assert data["citizen_urgency_score"] >= 0.50
        assert data["requires_human_triage"] is False
