"""Analytic Hierarchy Process (AHP) Engine over 5 Orthogonal Dimensions (§A12).

Dimensions:
1. Severity (S)
2. Risk (R)
3. Exposure (E)
4. Criticality (C)
5. Urgency (U)

Pure CPU computation using NumPy / power iteration. Zero external math APIs.
"""

from dataclasses import dataclass
from typing import ClassVar

import numpy as np

# Saaty Random Consistency Index for n=1..10 (RI_5 = 1.12)
SAATY_RANDOM_INDEX: dict[int, float] = {
    1: 0.0,
    2: 0.0,
    3: 0.58,
    4: 0.90,
    5: 1.12,
    6: 1.24,
    7: 1.32,
    8: 1.41,
    9: 1.45,
    10: 1.49,
}

CRITERIA_KEYS: list[str] = ["severity", "risk", "exposure", "criticality", "urgency"]


@dataclass(frozen=True)
class CriteriaSubscores:
    """The 5 orthogonal incident evaluation sub-scores in [0.0, 1.0]."""

    severity: float
    risk: float
    exposure: float
    criticality: float
    urgency: float

    def __post_init__(self) -> None:
        for key in CRITERIA_KEYS:
            val = getattr(self, key)
            if not (0.0 <= val <= 1.0):
                raise ValueError(f"Subscore '{key}' must be within [0.0, 1.0], got {val}")

    def to_vector(self) -> np.ndarray:
        return np.array(
            [self.severity, self.risk, self.exposure, self.criticality, self.urgency],
            dtype=np.float64,
        )


@dataclass
class AHPResult:
    """Computed AHP weights and consistency verification statistics."""

    weights: dict[str, float]
    lambda_max: float
    consistency_index: float
    consistency_ratio: float
    is_consistent: bool


class AHPMatrix:
    """5x5 Saaty Pairwise Comparison Matrix solver with strict CR < 0.10 validation."""

    N: ClassVar[int] = 5
    RI: ClassVar[float] = 1.12

    # Calibrated cold-start Saaty matrix (§A12 default)
    # Order: [Severity, Risk, Exposure, Criticality, Urgency]
    # Criticality > Risk > Severity > Exposure > Urgency
    DEFAULT_MATRIX: ClassVar[list[list[float]]] = [
        [1.0, 1.0 / 1.2, 1.1, 1.0 / 1.5, 1.25],  # Severity
        [1.2, 1.0, 1.33, 1.0 / 1.25, 1.5],  # Risk
        [1.0 / 1.1, 1.0 / 1.33, 1.0, 1.0 / 1.66, 1.125],  # Exposure
        [1.5, 1.25, 1.66, 1.0, 1.875],  # Criticality
        [1.0 / 1.25, 1.0 / 1.5, 1.0 / 1.125, 1.0 / 1.875, 1.0],  # Urgency
    ]

    def __init__(self, matrix: list[list[float]] | None = None) -> None:
        raw_mat = matrix if matrix is not None else self.DEFAULT_MATRIX
        self.matrix = np.array(raw_mat, dtype=np.float64)

        if self.matrix.shape != (self.N, self.N):
            raise ValueError(
                f"AHP matrix must be of shape ({self.N}, {self.N}), got {self.matrix.shape}"
            )

        self._validate_reciprocal()

    def _validate_reciprocal(self) -> None:
        """Verify matrix is positive and reciprocal: A[i, j] * A[j, i] == 1, A[i, i] == 1."""
        for i in range(self.N):
            if not np.isclose(self.matrix[i, i], 1.0, atol=1e-5):
                raise ValueError(
                    f"Diagonal element A[{i},{i}] must be 1.0, got {self.matrix[i, i]}"
                )
            for j in range(self.N):
                if self.matrix[i, j] <= 0:
                    raise ValueError(
                        f"Matrix elements must be positive, got A[{i},{j}] = {self.matrix[i, j]}"
                    )
                product = self.matrix[i, j] * self.matrix[j, i]
                if not np.isclose(product, 1.0, atol=1e-4):
                    raise ValueError(
                        f"Matrix must be reciprocal: A[{i},{j}] * A[{j},{i}] = {product} != 1.0"
                    )

    def solve(self) -> AHPResult:
        """Extract principal eigenvector via power iteration / NumPy eigen decomposition.

        Enforces strict Consistency Ratio CR = CI / RI < 0.10.
        """
        eigvals, eigvecs = np.linalg.eig(self.matrix)
        max_idx = int(np.argmax(np.real(eigvals)))
        lambda_max = float(np.real(eigvals[max_idx]))

        # Principal eigenvector (normalized to sum to 1.0)
        vec = np.real(eigvecs[:, max_idx])
        vec = np.abs(vec)
        weights_arr = vec / np.sum(vec)

        # Consistency metrics
        ci = float((lambda_max - self.N) / (self.N - 1))
        # Handle numerical precision: small negative ci is treated as 0.0
        if ci < 0.0 and ci > -1e-9:
            ci = 0.0
        cr = float(ci / self.RI) if self.RI > 0 else 0.0

        weights_dict = {CRITERIA_KEYS[i]: round(float(weights_arr[i]), 6) for i in range(self.N)}
        # Re-normalize to exact 1.0
        total_w = sum(weights_dict.values())
        if total_w > 0:
            weights_dict = {k: round(v / total_w, 6) for k, v in weights_dict.items()}

        is_consistent = cr < 0.10

        return AHPResult(
            weights=weights_dict,
            lambda_max=round(lambda_max, 6),
            consistency_index=round(ci, 6),
            consistency_ratio=round(cr, 6),
            is_consistent=is_consistent,
        )


def calculate_raw_priority(subscores: CriteriaSubscores, weights: dict[str, float]) -> float:
    """Calculate deterministic linear combination raw priority score in [0.0, 1.0].

    P_raw = sum(w_k * s_k)
    """
    raw_score = (
        weights["severity"] * subscores.severity
        + weights["risk"] * subscores.risk
        + weights["exposure"] * subscores.exposure
        + weights["criticality"] * subscores.criticality
        + weights["urgency"] * subscores.urgency
    )
    return round(float(np.clip(raw_score, 0.0, 1.0)), 6)
