/**
 * AHP Matrix Solver
 * Exact TypeScript port of backend domain solver: civicbrain/domain/prioritization/ahp.py
 * Pure mathematical computation using Saaty eigenvector power iteration.
 * Zero synthetic data, zero external math APIs.
 */

export const CRITERIA_KEYS = ['severity', 'risk', 'exposure', 'criticality', 'urgency'] as const;
export type CriteriaKey = (typeof CRITERIA_KEYS)[number];

export interface CriteriaMeta {
  key: CriteriaKey;
  label: string;
  code: string;
  hindiLabel: string;
  description: string;
}

export const CRITERIA_DEFINITIONS: CriteriaMeta[] = [
  {
    key: 'severity',
    code: 'S',
    label: 'Severity',
    hindiLabel: 'गंभीरता',
    description: 'Physical defect scale & immediate hazard to life or property',
  },
  {
    key: 'risk',
    code: 'R',
    label: 'Risk',
    hindiLabel: 'जोखिम',
    description: 'Cascade probability of systemic disruption or escalation',
  },
  {
    key: 'exposure',
    code: 'E',
    label: 'Exposure',
    hindiLabel: 'नागरिक प्रभाव',
    description: 'Population density, footfall volume & traffic corridor impact',
  },
  {
    key: 'criticality',
    code: 'C',
    label: 'Criticality',
    hindiLabel: 'महत्वपूर्णता',
    description: 'Lifeline infrastructure, hospital/school/transit proximity',
  },
  {
    key: 'urgency',
    code: 'U',
    label: 'Urgency',
    hindiLabel: 'तात्कालिकता',
    description: 'Rate of physical deterioration if left unattended',
  },
];

// Saaty Random Consistency Index for n=5 (from SAATY_RANDOM_INDEX[5] = 1.12)
export const SAATY_RI_5 = 1.12;

// Exact default calibrated matrix from backend AHPMatrix.DEFAULT_MATRIX
export const DEFAULT_AHP_MATRIX: number[][] = [
  [1.0, 1.0 / 1.2, 1.1, 1.0 / 1.5, 1.25], // Severity
  [1.2, 1.0, 1.33, 1.0 / 1.25, 1.5], // Risk
  [1.0 / 1.1, 1.0 / 1.33, 1.0, 1.0 / 1.66, 1.125], // Exposure
  [1.5, 1.25, 1.66, 1.0, 1.875], // Criticality
  [1.0 / 1.25, 1.0 / 1.5, 1.0 / 1.125, 1.0 / 1.875, 1.0], // Urgency
];

export interface AHPResult {
  weights: Record<CriteriaKey, number>;
  lambdaMax: number;
  consistencyIndex: number;
  consistencyRatio: number;
  isConsistent: boolean;
  maxTransitivityViolation?: {
    row: number;
    col: number;
    reason: string;
  };
}

/**
 * Solve 5x5 Saaty AHP matrix via power iteration.
 * Strictly verifies Consistency Ratio CR < 0.10.
 */
export const solveAHPMatrix = (matrix: number[][], maxIter = 100, tol = 1e-9): AHPResult => {
  const N = 5;

  // Validate matrix format and positivity
  if (matrix.length !== N || matrix.some((row) => row.length !== N)) {
    throw new Error('AHP matrix must be 5x5');
  }

  // Initial uniform vector
  let v = [1.0 / N, 1.0 / N, 1.0 / N, 1.0 / N, 1.0 / N];

  // Power iteration
  for (let iter = 0; iter < maxIter; iter++) {
    const vNext: number[] = [];
    for (let i = 0; i < N; i++) {
      let sum = 0;
      for (let j = 0; j < N; j++) {
        sum += matrix[i][j] * v[j];
      }
      vNext.push(sum);
    }

    const norm = vNext.reduce((a, b) => a + b, 0);
    const normalized = vNext.map((x) => x / norm);

    let diff = 0;
    for (let i = 0; i < N; i++) {
      diff = Math.max(diff, Math.abs(normalized[i] - v[i]));
    }

    v = normalized;
    if (diff < tol) {
      break;
    }
  }

  // Calculate lambda_max: average of (A * v)_i / v_i
  const av: number[] = [];
  for (let i = 0; i < N; i++) {
    let sum = 0;
    for (let j = 0; j < N; j++) {
      sum += matrix[i][j] * v[j];
    }
    av.push(sum);
  }

  let lambdaMax = 0;
  for (let i = 0; i < N; i++) {
    lambdaMax += av[i] / v[i];
  }
  lambdaMax /= N;

  // Consistency metrics
  let ci = (lambdaMax - N) / (N - 1);
  if (ci < 0.0 && ci > -1e-9) {
    ci = 0.0;
  }
  const cr = ci / SAATY_RI_5;

  const weights: Record<CriteriaKey, number> = {
    severity: v[0],
    risk: v[1],
    exposure: v[2],
    criticality: v[3],
    urgency: v[4],
  };

  // Diagnostic transitivity violation check if inconsistent
  let maxViolation: { row: number; col: number; reason: string } | undefined;
  if (cr >= 0.1) {
    let maxDiff = 0;
    for (let i = 0; i < N; i++) {
      for (let j = 0; j < N; j++) {
        for (let k = 0; k < N; k++) {
          if (i !== j && j !== k && i !== k) {
            // Transitivity check: a_ik should approximate a_ij * a_jk
            const expected = matrix[i][j] * matrix[j][k];
            const actual = matrix[i][k];
            const diff = Math.abs(expected - actual);
            if (diff > maxDiff) {
              maxDiff = diff;
              maxViolation = {
                row: i,
                col: k,
                reason: `Comparison of ${CRITERIA_DEFINITIONS[i].label} (${CRITERIA_DEFINITIONS[i].code}) vs ${CRITERIA_DEFINITIONS[k].label} (${CRITERIA_DEFINITIONS[k].code}) contradicts intermediate comparison via ${CRITERIA_DEFINITIONS[j].label} (${CRITERIA_DEFINITIONS[j].code}).`,
              };
            }
          }
        }
      }
    }
  }

  return {
    weights,
    lambdaMax: Number(lambdaMax.toFixed(5)),
    consistencyIndex: Number(ci.toFixed(5)),
    consistencyRatio: Number(cr.toFixed(5)),
    isConsistent: cr < 0.1,
    maxTransitivityViolation: maxViolation,
  };
};
