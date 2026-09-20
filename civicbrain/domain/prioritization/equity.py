r"""Bühlmann Credibility Equity Compensator (§A13, Bootstrap Principle §A3).

Solves the civic grievance underreporting inequity:
1. Computes credibility factor Z_i = n_i / (n_i + K).
2. Blends city prior rate mu_0 with ward verified rate X_bar_i to get expected issue rate \hat{\mu}_i.
3. Compares expected rate to observed report rate O_i to find equity gap Delta_i = max(0, \hat{\mu}_i - O_i).
4. Derives equity boost \beta_i proportional to the gap.
"""

from dataclasses import dataclass

# Provisional defaults pending real-data tuning (Bootstrap Principle §A3)
DEFAULT_K_STRUCTURAL_PARAM: float = 10.0
PROVISIONAL_BETA_MAX: float = 0.25
PROVISIONAL_GAMMA: float = 0.50


@dataclass(frozen=True)
class WardEquityResult:
    """Computed Bühlmann credibility and equity gap evaluation."""

    credibility_factor: float
    expected_issue_rate: float
    observed_issue_rate: float
    equity_gap: float
    equity_boost: float


class BuhlmannEquityCompensator:
    """Self-calibrating actuarial equity engine."""

    def __init__(
        self,
        k_param: float = DEFAULT_K_STRUCTURAL_PARAM,
        beta_max: float = PROVISIONAL_BETA_MAX,
        gamma: float = PROVISIONAL_GAMMA,
    ) -> None:
        """Initialize compensator with provisional parameters pending empirical calibration."""
        self.k_param = k_param
        self.beta_max = beta_max
        self.gamma = gamma

    def compute_credibility_factor(self, verified_incident_count: int) -> float:
        """Compute Bühlmann credibility factor Z_i = n_i / (n_i + K).

        Cold start: n_i = 0 -> Z_i = 0.0 (100% collective prior).
        Asymptotic: n_i -> infinity -> Z_i -> 1.0 (100% empirical ward history).
        """
        n = max(0, verified_incident_count)
        z = n / (n + self.k_param)
        return round(float(z), 6)

    def compute_expected_issue_rate(
        self,
        historical_incident_rate: float,
        city_prior_rate: float,
        credibility_factor: float,
    ) -> float:
        r"""Compute expected issue rate \hat{\mu}_i = Z_i * X_bar_i + (1 - Z_i) * \mu_0."""
        z = credibility_factor
        expected = (z * historical_incident_rate) + ((1.0 - z) * city_prior_rate)
        return round(float(expected), 6)

    def calculate_equity_gap(
        self,
        expected_issue_rate: float,
        observed_issue_rate: float,
    ) -> float:
        r"""Compute the deficit Delta_i = max(0, \hat{\mu}_i - O_i)."""
        gap = max(0.0, expected_issue_rate - observed_issue_rate)
        return round(float(gap), 6)

    def calculate_equity_boost(
        self,
        equity_gap: float,
        expected_issue_rate: float,
    ) -> float:
        """Derive priority boost beta_i = min(beta_max, gamma * (Delta_i / (expected_rate + epsilon))).

        Boost is proportional to the relative equity deficit, bounded by beta_max.
        """
        if expected_issue_rate <= 0.0:
            return 0.0
        relative_gap = equity_gap / (expected_issue_rate + 1e-6)
        raw_boost = self.gamma * relative_gap
        boost = min(self.beta_max, raw_boost)
        return round(float(boost), 6)

    def evaluate_ward(
        self,
        verified_incident_count: int,
        historical_incident_rate: float,
        observed_issue_rate: float,
        city_prior_rate: float,
    ) -> WardEquityResult:
        """Full evaluation pipeline for a ward's reporting equity."""
        z = self.compute_credibility_factor(verified_incident_count)
        expected = self.compute_expected_issue_rate(
            historical_incident_rate=historical_incident_rate,
            city_prior_rate=city_prior_rate,
            credibility_factor=z,
        )
        gap = self.calculate_equity_gap(expected, observed_issue_rate)
        boost = self.calculate_equity_boost(gap, expected)
        return WardEquityResult(
            credibility_factor=z,
            expected_issue_rate=expected,
            observed_issue_rate=observed_issue_rate,
            equity_gap=gap,
            equity_boost=boost,
        )
