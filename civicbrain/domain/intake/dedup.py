"""Direct Fellegi-Sunter implementation using provisional cold-start weights (§A11).

In accordance with:
- Hard Rule 4: Deterministic over LLM (zero LLM calls for deduplication).
- The Bootstrap Principle (§A3): Uses direct Fellegi-Sunter record linkage math with
  explicit 'provisional cold-start defaults pending re-estimation' until operational
  pairwise volume enables empirical EM parameter estimation. Full Splink Linker/EM
  batch estimation is deferred as a documented future upgrade once empirical pair volume
  accumulates.
"""

import logging
import math

from civicbrain.domain.intake.models import DedupDecision

logger = logging.getLogger(__name__)

# Provisional cold-start parameters pending re-estimation via Splink EM in a future upgrade
COLD_START_PARAMS = {
    "spatial_exact_threshold_m": 15.0,
    "spatial_near_threshold_m": 50.0,
    "temporal_window_hours": 72.0,
    "text_similarity_threshold": 0.80,
    "p_match_high": 0.85,
    "p_match_low": 0.50,
}

# Empirical cold-start Bayes log2 weights
# w_i = log2(m_i / u_i) on agreement; log2((1 - m_i) / (1 - u_i)) on disagreement
SPATIAL_EXACT_WEIGHT = math.log2(0.85 / 0.01)  # ~ +6.40
SPATIAL_NEAR_WEIGHT = math.log2(0.60 / 0.05)  # ~ +3.58
SPATIAL_FAR_WEIGHT = math.log2(0.05 / 0.94)  # ~ -4.23

TIME_WITHIN_WEIGHT = math.log2(0.90 / 0.10)  # ~ +3.17
TIME_OUTSIDE_WEIGHT = math.log2(0.10 / 0.90)  # ~ -3.17

CAT_MATCH_WEIGHT = math.log2(0.95 / 0.05)  # ~ +4.24
CAT_MISMATCH_WEIGHT = math.log2(0.05 / 0.95)  # ~ -4.24

TEXT_HIGH_WEIGHT = math.log2(0.70 / 0.02)  # ~ +5.12
TEXT_LOW_WEIGHT = math.log2(0.30 / 0.98)  # ~ -1.71

# Cold-start prior odds P(M) / (1 - P(M)) assuming base prior P(M) = 0.05
PRIOR_ODDS = 0.05 / (1.0 - 0.05)


def calculate_jaro_winkler_similarity(s1: str | None, s2: str | None) -> float:
    """Deterministic Jaro-Winkler similarity calculation for cold-start text matching."""
    if not s1 or not s2:
        return 0.0
    s1, s2 = s1.lower().strip(), s2.lower().strip()
    if s1 == s2:
        return 1.0

    len1, len2 = len(s1), len(s2)
    max_dist = max(len1, len2) // 2 - 1
    if max_dist < 0:
        max_dist = 0

    s1_matches = [False] * len1
    s2_matches = [False] * len2
    matches = 0

    for i in range(len1):
        start = max(0, i - max_dist)
        end = min(i + max_dist + 1, len2)
        for j in range(start, end):
            if s2_matches[j]:
                continue
            if s1[i] != s2[j]:
                continue
            s1_matches[i] = True
            s2_matches[j] = True
            matches += 1
            break

    if matches == 0:
        return 0.0

    transpositions = 0
    k = 0
    for i in range(len1):
        if not s1_matches[i]:
            continue
        while not s2_matches[k]:
            k += 1
        if s1[i] != s2[k]:
            transpositions += 1
        k += 1

    transpositions //= 2
    jaro = (matches / len1 + matches / len2 + (matches - transpositions) / matches) / 3.0

    # Winkler prefix bonus (up to 4 chars)
    prefix_len = 0
    for i in range(min(4, min(len1, len2))):
        if s1[i] == s2[i]:
            prefix_len += 1
        else:
            break

    return jaro + prefix_len * 0.1 * (1.0 - jaro)


def evaluate_splink_record_linkage(
    distance_meters: float,
    diff_seconds: float,
    category_match: bool,
    text_similarity: float,
) -> tuple[float, float, DedupDecision]:
    """Evaluates pairwise record linkage using direct Fellegi-Sunter cold-start math.

    Returns:
        (total_match_weight, posterior_probability, decision)
    """
    total_weight = 0.0

    # 1. Spatial proximity
    if distance_meters <= COLD_START_PARAMS["spatial_exact_threshold_m"]:
        total_weight += SPATIAL_EXACT_WEIGHT
    elif distance_meters <= COLD_START_PARAMS["spatial_near_threshold_m"]:
        total_weight += SPATIAL_NEAR_WEIGHT
    else:
        total_weight += SPATIAL_FAR_WEIGHT

    # 2. Temporal proximity
    hours_diff = diff_seconds / 3600.0
    if hours_diff <= COLD_START_PARAMS["temporal_window_hours"]:
        total_weight += TIME_WITHIN_WEIGHT
    else:
        total_weight += TIME_OUTSIDE_WEIGHT

    # 3. Category alignment
    if category_match:
        total_weight += CAT_MATCH_WEIGHT
    else:
        total_weight += CAT_MISMATCH_WEIGHT

    # 4. Text similarity
    if text_similarity >= COLD_START_PARAMS["text_similarity_threshold"]:
        total_weight += TEXT_HIGH_WEIGHT
    else:
        total_weight += TEXT_LOW_WEIGHT

    # Posterior probability via Bayes odds update
    odds = PRIOR_ODDS * (2.0**total_weight)
    posterior_prob = odds / (1.0 + odds)
    posterior_prob = max(0.0, min(1.0, posterior_prob))

    # Decision boundaries
    if posterior_prob >= COLD_START_PARAMS["p_match_high"]:
        decision = DedupDecision.EXACT_MATCH
    elif posterior_prob >= COLD_START_PARAMS["p_match_low"]:
        decision = DedupDecision.PROBABLE_MATCH
    else:
        decision = DedupDecision.DISTINCT

    return total_weight, posterior_prob, decision
