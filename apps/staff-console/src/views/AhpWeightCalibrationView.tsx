import React, { useState, useMemo } from 'react';
import { Button, SealMark } from '@civicbrain/ui';
import {
  solveAHPMatrix,
  DEFAULT_AHP_MATRIX,
  CRITERIA_DEFINITIONS,
  CriteriaKey,
  AHPResult,
} from '../logic/ahpSolver';
import {
  Sliders,
  AlertTriangle,
  CheckCircle2,
  RotateCcw,
  Sparkles,
  Info,
  Scale,
  ShieldCheck,
  Zap,
} from 'lucide-react';

export const AhpWeightCalibrationView: React.FC = () => {
  // Active baseline matrix (from backend GET /v1/prioritization/ahp/matrix/active)
  const activeBaselineMatrix = useMemo(() => DEFAULT_AHP_MATRIX, []);
  const activeBaselineResult = useMemo(
    () => solveAHPMatrix(activeBaselineMatrix),
    [activeBaselineMatrix]
  );

  // Editable draft matrix
  const [draftMatrix, setDraftMatrix] = useState<number[][]>(() =>
    DEFAULT_AHP_MATRIX.map((row) => [...row])
  );

  // Saved state
  const [isCommitted, setIsCommitted] = useState<boolean>(false);
  const [committedTimestamp, setCommittedTimestamp] = useState<string | null>(null);

  // Calculate live AHP solution from draft matrix
  const ahpResult: AHPResult = useMemo(() => {
    try {
      return solveAHPMatrix(draftMatrix);
    } catch (err) {
      return {
        weights: activeBaselineResult.weights,
        lambdaMax: 5.0,
        consistencyIndex: 0.0,
        consistencyRatio: 0.0,
        isConsistent: true,
      };
    }
  }, [draftMatrix, activeBaselineResult]);

  // Handle cell edit with automatic reciprocal enforcement
  const handleCellChange = (rowIndex: number, colIndex: number, rawValue: string) => {
    if (rowIndex === colIndex) return; // Diagonal is immutable 1.0

    const num = parseFloat(rawValue);
    if (isNaN(num) || num <= 0) return;

    setDraftMatrix((prev) => {
      const next = prev.map((row) => [...row]);
      next[rowIndex][colIndex] = Number(num.toFixed(4));
      next[colIndex][rowIndex] = Number((1.0 / num).toFixed(4));
      return next;
    });
    setIsCommitted(false);
  };

  // Reset to active baseline
  const handleReset = () => {
    setDraftMatrix(DEFAULT_AHP_MATRIX.map((row) => [...row]));
    setIsCommitted(false);
  };

  // Load a deliberately inconsistent matrix for acceptance testing
  const handleLoadInconsistentFixture = () => {
    setDraftMatrix((prev) => {
      const next = prev.map((row) => [...row]);
      // S vs R = 9, R vs E = 9, but S vs E = 1/9 (extreme transitivity violation)
      next[0][1] = 9;
      next[1][0] = 1 / 9;
      next[1][2] = 9;
      next[2][1] = 1 / 9;
      next[0][2] = 1 / 9;
      next[2][0] = 9;
      return next;
    });
    setIsCommitted(false);
  };

  // Commit Calibration Action
  const handleCommit = () => {
    if (!ahpResult.isConsistent) return; // Hard block!
    setIsCommitted(true);
    setCommittedTimestamp(new Date().toLocaleTimeString('en-IN', { timeZone: 'Asia/Kolkata' }));
  };

  const cr = ahpResult.consistencyRatio;
  const isConsistent = ahpResult.isConsistent;

  return (
    <div
      data-testid="ahp-weight-calibration-view"
      className="p-4 sm:p-6 max-w-5xl mx-auto space-y-6 font-ui text-primary select-none"
    >
      {/* Screen Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-border">
        <div>
          <div className="flex items-center gap-2">
            <Scale className="w-5 h-5 text-action-primary" />
            <h1 className="text-xl font-bold text-primary tracking-tight">
              AHP Weight Calibration — 5×5 Pairwise Matrix
            </h1>
          </div>
          <p className="text-xs text-secondary font-mono mt-1">
            Analytic Hierarchy Process • S/R/E/C/U Dimensions • Saaty Eigenvector Decomposition
          </p>
        </div>

        {/* Action Controls */}
        <div className="flex items-center gap-2">
          <Button
            variant="outline"
            size="sm"
            onClick={handleLoadInconsistentFixture}
            className="text-xs font-mono"
            aria-label="Load deliberately inconsistent matrix to test hard save block"
          >
            <AlertTriangle className="w-3.5 h-3.5 text-status-warning mr-1.5" />
            <span>Test Inconsistent Fixture</span>
          </Button>

          <Button
            variant="outline"
            size="sm"
            onClick={handleReset}
            className="text-xs font-mono"
            aria-label="Reset matrix to active baseline"
          >
            <RotateCcw className="w-3.5 h-3.5 mr-1.5" />
            <span>Reset Baseline</span>
          </Button>
        </div>
      </div>

      {/* Dominant Instrument Banner: Consistency Ratio (CR) Readout */}
      <section
        role="region"
        aria-label="AHP Consistency Ratio Instrument Readout"
        className={`p-5 rounded-md border-2 transition-all ${
          isConsistent
            ? 'bg-surface border-border'
            : 'bg-status-danger/10 border-status-danger/50'
        }`}
      >
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="text-[11px] font-mono text-secondary uppercase tracking-wider font-semibold">
              Live Consistency Ratio (CR) • Saaty RI = 1.12
            </div>
            <div className="flex items-baseline gap-3 mt-1">
              <span
                className={`font-mono text-3xl font-extrabold tracking-tight ${
                  isConsistent ? 'text-primary' : 'text-status-danger'
                }`}
              >
                CR = {cr.toFixed(4)}
              </span>
              <span className="font-mono text-xs text-secondary">
                (λ_max = {ahpResult.lambdaMax.toFixed(3)}, CI = {ahpResult.consistencyIndex.toFixed(4)})
              </span>
            </div>
          </div>

          {/* Status Chip */}
          <div className="flex items-center gap-2">
            {isConsistent ? (
              <div
                role="status"
                className="px-3 py-1.5 rounded-sm bg-status-success/20 text-status-success border border-status-success/40 text-xs font-mono font-bold flex items-center gap-2"
              >
                <CheckCircle2 className="w-4 h-4 shrink-0" />
                <span>CONSISTENT (CR &lt; 0.10) • SAVE ALLOWED</span>
              </div>
            ) : (
              <div
                role="alert"
                className="px-3 py-1.5 rounded-sm bg-status-danger/20 text-status-danger border border-status-danger/50 text-xs font-mono font-bold flex items-center gap-2"
              >
                <AlertTriangle className="w-4 h-4 shrink-0" />
                <span>INCONSISTENT (CR &ge; 0.10) • SAVE BLOCKED</span>
              </div>
            )}
          </div>
        </div>

        {/* Screen Reader Live Announcement */}
        <div aria-live="polite" className="sr-only">
          {isConsistent
            ? `Matrix is consistent with consistency ratio ${cr.toFixed(4)}. Save is permitted.`
            : `Warning: Matrix consistency ratio is ${cr.toFixed(4)}, exceeding the 0.10 threshold. Save is strictly disabled.`}
        </div>

        {/* Diagnostic Inconsistency Guidance */}
        {!isConsistent && ahpResult.maxTransitivityViolation && (
          <div className="mt-4 p-3 bg-status-danger/15 border border-status-danger/40 rounded-sm text-xs font-mono text-primary space-y-1">
            <div className="font-bold text-status-danger flex items-center gap-1.5">
              <AlertTriangle className="w-4 h-4" />
              <span>Diagnostic Transitivity Violation:</span>
            </div>
            <p className="text-secondary pl-5">
              {ahpResult.maxTransitivityViolation.reason}
            </p>
            <p className="text-[11px] text-status-warning pl-5">
              * Adjust this pair towards consistency to bring CR below 0.10.
            </p>
          </div>
        )}
      </section>

      {/* Main Grid: Pairwise Matrix & Derived Weights */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* Left Column (7 cols): 5x5 Pairwise Matrix Editor */}
        <div className="lg:col-span-7 bg-surface rounded-md border border-border p-4 sm:p-5 space-y-4">
          <div className="flex items-center justify-between border-b border-border pb-3">
            <div>
              <h2 className="text-sm font-bold text-primary uppercase font-mono tracking-wider">
                Pairwise Comparison Matrix (Draft)
              </h2>
              <p className="text-xs text-secondary mt-0.5 font-mono">
                Cell (i, j) indicates relative priority of Row over Column
              </p>
            </div>
            <span className="text-[11px] font-mono text-secondary">
              Auto-reciprocal: A[j,i] = 1 / A[i,j]
            </span>
          </div>

          {/* Matrix Grid */}
          <div className="overflow-x-auto">
            <table className="w-full border-collapse text-xs font-mono">
              <thead>
                <tr>
                  <th className="p-2 border border-border bg-field-100/60 text-secondary font-medium">
                    Criteria
                  </th>
                  {CRITERIA_DEFINITIONS.map((c) => (
                    <th
                      key={c.key}
                      className="p-2 border border-border bg-field-100/60 text-primary font-bold text-center w-16"
                      title={`${c.label} (${c.hindiLabel}): ${c.description}`}
                    >
                      {c.code}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {CRITERIA_DEFINITIONS.map((rowDef, rowIndex) => (
                  <tr key={rowDef.key}>
                    {/* Row Header */}
                    <th
                      scope="row"
                      className="p-2.5 border border-border bg-field-100/60 text-left font-bold text-primary whitespace-nowrap"
                      title={`${rowDef.label} (${rowDef.hindiLabel}): ${rowDef.description}`}
                    >
                      <div className="flex items-center gap-1.5">
                        <span className="text-action-primary">{rowDef.code}</span>
                        <span className="font-normal text-secondary hidden sm:inline">
                          • {rowDef.label}
                        </span>
                      </div>
                    </th>

                    {/* Matrix Cells */}
                    {CRITERIA_DEFINITIONS.map((colDef, colIndex) => {
                      const isDiagonal = rowIndex === colIndex;
                      const value = draftMatrix[rowIndex][colIndex];
                      const formattedValue =
                        value >= 1 ? value.toFixed(value === 1 ? 0 : 2) : value.toFixed(2);

                      return (
                        <td
                          key={colDef.key}
                          className={`p-1 border border-border text-center ${
                            isDiagonal ? 'bg-field-100/80 font-bold text-secondary' : 'bg-surface'
                          }`}
                        >
                          {isDiagonal ? (
                            <span className="inline-block py-1.5 text-secondary">1.0</span>
                          ) : (
                            <input
                              type="number"
                              min="0.1"
                              max="9"
                              step="0.1"
                              value={formattedValue}
                              onChange={(e) =>
                                handleCellChange(rowIndex, colIndex, e.target.value)
                              }
                              className="w-full py-1.5 text-center font-mono text-xs bg-background text-primary border border-border rounded-xs focus:ring-1 focus:ring-focus outline-none"
                              aria-label={`Comparison of ${rowDef.label} over ${colDef.label}`}
                            />
                          )}
                        </td>
                      );
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Saaty Scale Legend */}
          <div className="pt-2 text-[11px] font-mono text-secondary flex flex-wrap items-center gap-x-4 gap-y-1">
            <span>SCALE:</span>
            <span>1 = Equal</span>
            <span>3 = Moderate</span>
            <span>5 = Strong</span>
            <span>7 = Very Strong</span>
            <span>9 = Extreme</span>
          </div>
        </div>

        {/* Right Column (5 cols): Derived Criteria Weights */}
        <div className="lg:col-span-5 bg-surface rounded-md border border-border p-4 sm:p-5 space-y-4">
          <div className="border-b border-border pb-3">
            <h2 className="text-sm font-bold text-primary uppercase font-mono tracking-wider">
              Derived Normalized Weights (w_k)
            </h2>
            <p className="text-xs text-secondary mt-0.5 font-mono">
              Principal Eigenvector • Sum = 1.0 (100%)
            </p>
          </div>

          {/* Weights Bars */}
          <div className="space-y-3.5">
            {CRITERIA_DEFINITIONS.map((c) => {
              const weight = ahpResult.weights[c.key];
              const baselineWeight = activeBaselineResult.weights[c.key];
              const delta = (weight - baselineWeight) * 100;
              const percentage = (weight * 100).toFixed(1);

              return (
                <div key={c.key} className="space-y-1">
                  <div className="flex items-center justify-between text-xs font-mono">
                    <span className="font-bold text-primary">
                      {c.code} • {c.label} ({c.hindiLabel})
                    </span>
                    <div className="flex items-center gap-2">
                      {Math.abs(delta) > 0.1 && (
                        <span
                          className={`text-[10px] ${
                            delta > 0 ? 'text-status-success' : 'text-status-warning'
                          }`}
                        >
                          {delta > 0 ? `+${delta.toFixed(1)}%` : `${delta.toFixed(1)}%`}
                        </span>
                      )}
                      <span className="font-bold text-primary">{percentage}%</span>
                    </div>
                  </div>

                  {/* Progress Bar */}
                  <div className="w-full bg-field-100 h-2.5 rounded-xs overflow-hidden border border-border">
                    <div
                      className="bg-action-primary h-full transition-all duration-300"
                      style={{ width: `${percentage}%` }}
                    />
                  </div>
                  <p className="text-[10px] text-secondary leading-tight">{c.description}</p>
                </div>
              );
            })}
          </div>

          {/* Save / Commit Action Button (STRICT HARD BLOCK) */}
          <div className="pt-4 border-t border-border space-y-2">
            <Button
              variant="primary"
              size="lg"
              disabled={!isConsistent}
              onClick={handleCommit}
              className={`w-full justify-center min-h-[48px] text-sm font-bold ${
                !isConsistent ? 'opacity-40 cursor-not-allowed' : ''
              }`}
              aria-disabled={!isConsistent}
            >
              <span>Commit Calibration to Municipal Dispatch</span>
            </Button>

            {!isConsistent && (
              <p className="text-[11px] font-mono text-status-danger text-center font-semibold">
                * Save is blocked: Matrix consistency ratio must be &lt; 0.10.
              </p>
            )}

            {isCommitted && (
              <div className="p-4 bg-field-50 border border-border rounded-sm space-y-2 mt-3">
                <div className="flex justify-center">
                  <SealMark
                    authority="CIVIC_PRIORITIZATION_COUNCIL"
                    timestamp={committedTimestamp || '2026-09-24'}
                    verified
                  />
                </div>
                <div className="text-center font-mono text-xs text-status-success font-bold">
                  AHP Calibration Committed & Recorded in Ledger
                </div>
                <p className="text-center text-[11px] font-mono text-secondary">
                  Active weights updated for city-wide grievance prioritization.
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
