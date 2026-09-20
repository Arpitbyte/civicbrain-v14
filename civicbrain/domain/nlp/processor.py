"""NLP Pipeline, Multilingual Ingestion & Emotion-Severity Decoupling (§A11).

In strict accordance with:
- Hard Rule 1: Zero paid external API dependencies; lightweight CPU-only heuristic rule engine.
- Emotion-Severity Decoupling Principle: Citizen emotional intensity, capitalization, or anger
  must NEVER inflate the physical engineering severity score.
- Bootstrap Principle (§A3): Unrecognized colloquial phrases return suggested_category = None
  and requires_human_triage = True instead of hallucinating labels.
"""

import re
from typing import Protocol

from pydantic import BaseModel, ConfigDict, Field


class TextAnalysisResult(BaseModel):
    """Normalized analysis result returned by NLP processing pipeline (§A11)."""

    model_config = ConfigDict(from_attributes=True)

    detected_language: str = Field(
        ..., description="ISO 639-1 code or dialect (e.g. en, hi, kn, hinglish)"
    )
    detected_script: str = Field(
        ..., description="Detected Unicode script (e.g. Latin, Devanagari, Kannada, Tamil)"
    )
    normalized_text: str = Field(..., description="Transliteration/whitespace normalized text")
    suggested_category: str | None = Field(
        None, description="Inferred civic taxonomy category code"
    )
    physical_severity_hint: int | None = Field(
        None,
        ge=1,
        le=5,
        description="Physical engineering severity hint (1 to 5) strictly decoupled from emotion",
    )
    citizen_urgency_score: float = Field(
        0.0,
        ge=0.0,
        le=1.0,
        description="Decoupled citizen emotional urgency/frustration score (0.0 to 1.0)",
    )
    extracted_keywords: list[str] = Field(
        default_factory=list, description="Extracted civic terms and keywords"
    )
    requires_human_triage: bool = Field(
        False, description="Flagged for manual operator review if ambiguous"
    )


class NLPProcessor(Protocol):
    """Standard protocol for multilingual civic grievance text analysis."""

    def process_text(self, text: str, citizen_category: str | None = None) -> TextAnalysisResult:
        """Process incoming citizen grievance text into structured NLP metadata."""
        ...


class DeterministicIndicRuleProcessor:
    """Deterministic, lightweight multilingual processor optimized for Render free-tier CPU/RAM limits.

    Operates without loading heavyweight transformer weights into memory while providing
    accurate script detection, transliteration normalization, and emotion-severity decoupling.
    """

    # Category vocabulary across English, Hindi, Kannada, Tamil, and Romanized forms
    CATEGORY_LEXICON: dict[str, list[str]] = {
        "POTHOLE": [
            "pothole",
            "potholes",
            "crater",
            "craters",
            "asphalt damage",
            "khadda",
            "gaddha",
            "gadde",
            "khadde",
            "gundi",
            "kuzhi",
            "road damage",
            "road broken",
            "rough road",
            "bad road",
            "broken road",
            "खड्डा",
            "गड्ढा",
            "खड्डे",
            "गड्ढे",
            "ಗುಂಡಿ",
            "ರಸ್ತೆ ಗುಂಡಿ",
            "ಕುழி",
        ],
        "GARBAGE": [
            "garbage",
            "trash",
            "waste",
            "dump",
            "dumping",
            "litter",
            "rubbish",
            "debris",
            "dustbin",
            "kachra",
            "kooda",
            "kasa",
            "kuppa",
            "kachada",
            "solid waste",
            "plastic waste",
            "कचरा",
            "कूड़ा",
            "ಕಸ",
            "ತಿಪ್ಪೆ",
            "குப்பை",
        ],
        "DRAINAGE": [
            "drain",
            "drainage",
            "sewage",
            "sewer",
            "gutter",
            "overflow",
            "waterlogging",
            "water logged",
            "nala",
            "mori",
            "kaalave",
            "kaluve",
            "manhole",
            "clogged drain",
            "नाली",
            "सीवर",
            "नाल",
            "ಚರಂಡಿ",
            "ಕಾಲುವೆ",
            "சாக்கடை",
            "வடிகால்",
        ],
        "STREETLIGHT": [
            "streetlight",
            "street light",
            "streetlamp",
            "lamp",
            "pole",
            "dark",
            "darkness",
            "bulb",
            "bijli",
            "kambha",
            "current",
            "batti",
            "pole broken",
            "no light",
            "light illa",
            "स्ट्रीट लाइट",
            "बत्ती",
            "बिजली",
            "ಬೀದಿ ದೀಪ",
            "ಕಂಬ",
            "தெருவிளக்கு",
        ],
        "WATER_SUPPLY": [
            "water supply",
            "drinking water",
            "pipeline",
            "pipe leak",
            "water pipe",
            "no water",
            "peene ka pani",
            "kudiya neeru",
            "tanni",
            "jal",
            "leaking pipe",
            "पानी",
            "जल",
            "ಕುಡಿಯುವ ನೀರು",
            "ನೀರು",
            "குடிநீர்",
            "தண்ணீர்",
        ],
    }

    # Physical severity keywords (Strictly engineering scale, decoupled from sentiment)
    PHYSICAL_SEVERITY_KEYWORDS: dict[int, list[str]] = {
        5: [
            "massive crater",
            "cave-in",
            "collapsed road",
            "submerged",
            "high voltage",
            "life threatening",
            "huge crater",
            "deep pit",
        ],
        4: [
            "deep",
            "deep pothole",
            "burst main",
            "flooding",
            "knee deep",
            "waist deep",
            "broken main",
            "major leak",
        ],
        3: ["open manhole", "large", "overflowing", "sparking", "medium size", "uncovered"],
        2: ["medium", "dim", "pile", "unclean", "slow leak", "small crack"],
        1: ["small", "minor", "flickering", "litter", "slight"],
    }

    # Emotional urgency / distress markers (Affects citizen_urgency_score ONLY)
    EMOTION_DISTRESS_TERMS: list[str] = [
        "urgent",
        "urgently",
        "emergency",
        "immediate",
        "immediately",
        "danger",
        "dangerous",
        "accident",
        "hospital",
        "dying",
        "threat",
        "disaster",
        "shame",
        "shameful",
        "ridiculous",
        "worst",
        "pathetc",
        "pathetic",
        "useless",
        "careless",
        "negligent",
        "help",
        "please help",
        "jaldi",
        "turant",
        "sheeghra",
        "beku",
        "sikiram",
        "aabathu",
    ]

    def detect_script(self, text: str) -> tuple[str, str]:
        """Detect script and primary language using Unicode block ranges."""
        has_devanagari = any("\u0900" <= c <= "\u097f" for c in text)
        has_kannada = any("\u0c80" <= c <= "\u0cff" for c in text)
        has_tamil = any("\u0b80" <= c <= "\u0bff" for c in text)
        has_telugu = any("\u0c00" <= c <= "\u0c7f" for c in text)

        if has_kannada:
            return "kn", "Kannada"
        if has_tamil:
            return "ta", "Tamil"
        if has_telugu:
            return "te", "Telugu"
        if has_devanagari:
            return "hi", "Devanagari"

        # Check for Romanized Indian phrases (Hinglish/Kanglish markers)
        text_lower = text.lower()
        hinglish_markers = [
            " hai",
            " ko",
            " mein",
            " nahi",
            " rasta",
            " khadda",
            " kachra",
            " maadi",
            " illa",
            " bekagide",
        ]
        if any(marker in text_lower for marker in hinglish_markers):
            return "hinglish", "Latin"

        return "en", "Latin"

    def process_text(self, text: str, citizen_category: str | None = None) -> TextAnalysisResult:
        """Analyze grievance text extracting category hints and decoupled emotion metrics."""
        raw_text = text.strip()
        if not raw_text:
            return TextAnalysisResult(
                detected_language="en",
                detected_script="Latin",
                normalized_text="",
                suggested_category=citizen_category,
                physical_severity_hint=None,
                citizen_urgency_score=0.0,
                extracted_keywords=[],
                requires_human_triage=True,
            )

        lang, script = self.detect_script(raw_text)

        # Normalize whitespace and lowercase for keyword matching
        normalized = " ".join(raw_text.split())
        normalized_lower = normalized.lower()

        # 1. Category extraction
        matched_category = None
        extracted_terms: list[str] = []

        if citizen_category:
            matched_category = citizen_category.strip().upper()

        for category, keywords in self.CATEGORY_LEXICON.items():
            for kw in keywords:
                # Use word boundary matching for English/Latin, substring for Indic scripts
                pattern = r"\b" + re.escape(kw) + r"\b" if script == "Latin" else re.escape(kw)
                if re.search(pattern, normalized_lower, re.IGNORECASE):
                    extracted_terms.append(kw)
                    if not matched_category:
                        matched_category = category

        # 2. Emotion / Urgency analysis (Affects citizen_urgency_score ONLY)
        # Evaluates punctuation, capitalization ratio, and emotional distress terms
        matched_distress: list[str] = []
        for dt in self.EMOTION_DISTRESS_TERMS:
            if re.search(r"\b" + re.escape(dt) + r"\b", normalized_lower, re.IGNORECASE):
                matched_distress.append(dt)

        exclamation_count = normalized.count("!")
        question_count = normalized.count("?")
        punct_score = min(exclamation_count * 0.15 + question_count * 0.05, 0.40)

        # Capitalization ratio for Latin text
        alpha_chars = [c for c in normalized if c.isalpha()]
        caps_ratio = sum(1 for c in alpha_chars if c.isupper()) / max(len(alpha_chars), 1)
        caps_score = 0.25 if caps_ratio > 0.35 and len(alpha_chars) >= 8 else 0.0

        distress_score = min(len(matched_distress) * 0.25, 0.50)
        calculated_urgency = min(round(punct_score + caps_score + distress_score, 2), 1.0)

        # 3. Physical Severity Hint (Strictly engineering scale, decoupled from emotion)
        physical_severity = None
        for sev in (5, 4, 3, 2, 1):
            terms = self.PHYSICAL_SEVERITY_KEYWORDS[sev]
            for pt in terms:
                if re.search(r"\b" + re.escape(pt) + r"\b", normalized_lower, re.IGNORECASE):
                    physical_severity = sev
                    extracted_terms.append(pt)
                    break
            if physical_severity is not None:
                break

        # 4. Cold-Start Honesty Flag
        # If no recognized civic category could be matched and no citizen category was supplied
        requires_triage = matched_category is None

        # Clean duplicate keywords while preserving order
        seen = set()
        deduped_keywords = []
        for k in extracted_terms:
            if k not in seen:
                seen.add(k)
                deduped_keywords.append(k)

        return TextAnalysisResult(
            detected_language=lang,
            detected_script=script,
            normalized_text=normalized,
            suggested_category=matched_category,
            physical_severity_hint=physical_severity,
            citizen_urgency_score=calculated_urgency,
            extracted_keywords=deduped_keywords,
            requires_human_triage=requires_triage,
        )
