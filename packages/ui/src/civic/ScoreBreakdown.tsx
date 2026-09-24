import React, { useState } from 'react';
import { ChevronDown, ChevronUp, Layers, TrendingUp, HelpCircle } from 'lucide-react';
import { ConfidenceBadge } from './ConfidenceBadge';

export interface ScoreSubscores {
  severity: number;
  risk: number;
  exposure: number;
  criticality: number;
  urgency: number;
  [key: string]: number;
}

export interface ScoreWeights {
  severity?: number;
  risk?: number;
  exposure?: number;
  criticality?: number;
  urgency?: number;
  [key: string]: number | undefined;
}

export interface ScoreBreakdownProps {
  /**
   * Final composite priority rank (0.0 - 1.0 or scaled 0.0 - 100.0).
   * Matches API response field: priority_score / final_priority_score
   */
  priority_score: number;
  /**
   * Unadjusted multi-criteria score (0.0 - 1.0).
   * Matches API response field: raw_priority_score
   */
  raw_priority_score?: number;
  /**
   * Compensatory equity multiplier (beta >= 0).
   * Matches API response field: equity_boost
   */
  equity_boost?: number;
  /**
   * Statistical credibility factor Z (0.0 - 1.0).
   * Matches API response field: confidence_score
   */
  confidence_score?: number | null;
  /**
   * 5 orthogonal sub-scores (0.0 - 1.0 each)
   */
  subscores?: ScoreSubscores;
  /**
   * Active AHP pairwise weights used
   */
  weights_used?: ScoreWeights;
  /**
   * Ward identification or name for context
   */
  ward_name?: string;
  defaultExpanded?: boolean;
  className?: string;
}

/**
 * ScoreBreakdown
 * Conforms to FRONTEND_CONTEXT.md §3, PROJECT_REFERENCE_FOR_FRONTEND.md §3.3, and SCREEN_SPECS.md Tier 1:
 * - Glass-box itemized formula:
 *   priority_score = raw_priority_score * (1 + equity_boost)
 *   raw_priority_score = S*w_s + R*w_r + E*w_e + C*w_c + U*w_u (5 AHP criteria)
 * - Collapsed: final score + confidence only
 * - Expanded: each weighted criterion + equity boost + mono numerals
 * - Motion: Quiet tier (instant/fast height transition, no bouncy theater)
 */
export const ScoreBreakdown: React.FC<ScoreBreakdownProps> = ({
  priority_score,
  raw_priority_score,
  equity_boost = 0.0,
  confidence_score = null,
  subscores = { severity: 0.8, risk: 0.6, exposure: 0.7, criticality: 0.5, urgency: 0.9 },
  weights_used = { severity: 0.35, risk: 0.25, exposure: 0.15, criticality: 0.15, urgency: 0.10 },
  ward_name,
  defaultExpanded = false,
  className = '',
}) => {
  const [isExpanded, setIsExpanded] = useState(defaultExpanded);

  // Normalize scores to 0-100 scale for UI display if given as 0.0-1.0
  const normalizedFinalScore = priority_score <= 1.0 ? Math.round(priority_score * 100) : Math.round(priority_score);
  const normalizedRawScore = raw_priority_score !== undefined
    ? (raw_priority_score <= 1.0 ? (raw_priority_score * 100).toFixed(1) : raw_priority_score.toFixed(1))
    : (normalizedFinalScore / (1 + equity_boost)).toFixed(1);

  const equityBoostPercent = Math.round(equity_boost * 100);

  const criteriaList: Array<{
    key: keyof ScoreSubscores;
    label: string;
    description: string;
    defaultWeight: number;
  }> = [
    { key: 'severity', label: 'Severity (S)', description: 'Physical magnitude of defect', defaultWeight: 0.35 },
    { key: 'risk', label: 'Risk (R)', description: 'Immediate public safety / hazard risk', defaultWeight: 0.25 },
    { key: 'exposure', label: 'Exposure (E)', description: 'Pedestrian / vehicle traffic volume', defaultWeight: 0.15 },
    { key: 'criticality', label: 'Criticality (C)', description: 'Systemic municipal facility importance', defaultWeight: 0.15 },
    { key: 'urgency', label: 'Urgency (U)', description: 'Rate of temporal damage escalation', defaultWeight: 0.10 },
  ];

  return (
    <div
      className={`
        bg-surface rounded-md border border-border overflow-hidden font-ui text-primary
        transition-colors duration-fast ${className}
      `}
    >
      {/* Header bar: Collapsed view */}
      <div
        role="button"
        tabIndex={0}
        aria-expanded={isExpanded}
        onClick={() => setIsExpanded((prev) => !prev)}
        onKeyDown={(e) => {
          if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            setIsExpanded((prev) => !prev);
          }
        }}
        className="
          flex items-center justify-between p-4 cursor-pointer select-none
          hover:bg-surface-raised transition-colors duration-fast outline-none
          focus-visible:ring-2 focus-visible:ring-focus focus-visible:ring-inset
        "
      >
        <div className="flex items-center gap-3">
          <div className="flex items-baseline gap-1.5">
            <span className="text-xs font-semibold text-text-secondary uppercase tracking-wider">
              Priority Score
            </span>
            <span className="font-mono text-2xl font-bold tracking-tight text-primary">
              {normalizedFinalScore}
            </span>
            <span className="text-xs text-text-secondary font-mono">/100</span>
          </div>

          <ConfidenceBadge confidence_score={confidence_score} size="sm" />
        </div>

        <div className="flex items-center gap-2 text-xs font-medium text-text-secondary">
          <span className="hidden sm:inline">
            {isExpanded ? 'Hide Glass-Box Breakdown' : 'Expand AHP Formula'}
          </span>
          {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
        </div>
      </div>

      {/* Expanded itemization: Glass-box breakdown */}
      {isExpanded && (
        <div className="border-t border-border bg-surface-raised p-4 space-y-4">
          <div className="flex items-center justify-between text-xs text-text-secondary pb-2 border-b border-border/60">
            <div className="flex items-center gap-1.5 font-mono">
              <Layers className="w-3.5 h-3.5 text-action-primary" />
              <span>AHP Multi-Criteria Decomposition (5 Orthogonal Sub-scores)</span>
            </div>
            {ward_name && <span className="font-medium text-primary">Ward: {ward_name}</span>}
          </div>

          {/* 5 AHP Criteria Rows */}
          <div className="space-y-2">
            {criteriaList.map(({ key, label, description, defaultWeight }) => {
              const subscoreVal = subscores[key] ?? 0.5;
              const weightVal = weights_used[key] ?? defaultWeight;
              const weightedContribution = ((subscoreVal * weightVal) * 100).toFixed(1);

              return (
                <div
                  key={key}
                  className="flex flex-col sm:flex-row sm:items-center justify-between text-xs py-1.5 px-2 rounded-sm bg-surface/70 border border-border/40 gap-1.5"
                >
                  <div className="flex flex-col min-w-0">
                    <span className="font-semibold text-primary">{label}</span>
                    <span className="text-[11px] text-text-secondary truncate">{description}</span>
                  </div>

                  <div className="flex items-center gap-4 text-xs font-mono self-end sm:self-auto">
                    <span className="text-text-secondary">
                      Score: <strong className="text-primary font-mono">{subscoreVal.toFixed(2)}</strong>
                    </span>
                    <span className="text-text-secondary">
                      Weight: <strong className="text-primary font-mono">{Math.round(weightVal * 100)}%</strong>
                    </span>
                    <span className="text-action-primary font-semibold font-mono w-16 text-right">
                      +{weightedContribution}
                    </span>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Equity Boost & Final Calculation Bar */}
          <div className="pt-3 border-t border-border flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs">
            <div className="flex items-center gap-2">
              <TrendingUp className="w-4 h-4 text-status-success flex-shrink-0" />
              <div>
                <div className="font-semibold text-primary">
                  Bühlmann Credibility Equity Boost: <span className="font-mono text-status-success">+{equityBoostPercent}%</span>
                </div>
                <div className="text-[11px] text-text-secondary">
                  Compensates for historical reporting under-representation in underserved wards.
                </div>
              </div>
            </div>

            <div className="font-mono text-xs text-right bg-surface px-3 py-2 rounded-sm border border-border">
              <div className="text-text-secondary text-[11px]">
                Raw: {normalizedRawScore} × (1 + {equity_boost.toFixed(2)})
              </div>
              <div className="text-primary font-bold text-sm">
                Final = {normalizedFinalScore}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
