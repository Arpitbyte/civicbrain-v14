import React from 'react';
import { HelpCircle, ShieldCheck, AlertCircle, Clock } from 'lucide-react';

export type ConfidenceBand = 'cold_start' | 'low' | 'medium' | 'high';

export interface ConfidenceBadgeProps {
  /**
   * Numeric credibility or confidence factor Z (0.0 - 1.0).
   * If null or undefined, renders the honest cold-start state:
   * "Citizen Declared" or "Pending Automated Triage".
   * Never fabricates a percentage!
   */
  confidence_score?: number | null;
  /**
   * Optional custom label when in cold-start (defaults to "Citizen Declared").
   */
  coldStartLabel?: 'Citizen Declared' | 'Pending Automated Triage';
  size?: 'sm' | 'md';
  className?: string;
}

/**
 * ConfidenceBadge
 * Conforms to FRONTEND_CONTEXT.md §7.1, DESIGN.md §5 & §12, and SCREEN_SPECS.md Tier 1:
 * - Statistical certainty value Z = n / (n + K) (Bühlmann credibility)
 * - Numeric Z value + text band + icon, NEVER color-only
 * - When confidence_score is null/undefined (cold-start):
 *   honestly renders "Citizen Declared" or "Pending Automated Triage", never a fabricated percentage!
 * - Never red (uses amber for low, marker for medium, seal for high)
 */
export const ConfidenceBadge: React.FC<ConfidenceBadgeProps> = ({
  confidence_score,
  coldStartLabel = 'Citizen Declared',
  size = 'md',
  className = '',
}) => {
  // Honest cold-start check: if null or undefined, never fabricate a percentage
  if (confidence_score === null || confidence_score === undefined) {
    const isPending = coldStartLabel === 'Pending Automated Triage';
    return (
      <span
        role="status"
        aria-label={`Confidence: ${coldStartLabel} (Unscored cold start)`}
        className={`
          inline-flex items-center gap-1.5 font-ui font-medium rounded-full select-none border
          bg-surface-raised text-text-secondary border-border
          ${size === 'sm' ? 'text-[11px] py-0.5 px-2.5' : 'text-xs py-1 px-3'}
          ${className}
        `}
      >
        {isPending ? (
          <Clock className="w-3.5 h-3.5 text-text-secondary flex-shrink-0" aria-hidden="true" />
        ) : (
          <HelpCircle className="w-3.5 h-3.5 text-text-secondary flex-shrink-0" aria-hidden="true" />
        )}
        <span>{coldStartLabel}</span>
      </span>
    );
  }

  // Clamped valid score [0.0 - 1.0]
  const score = Math.max(0, Math.min(1, confidence_score));
  const percentage = Math.round(score * 100);

  // Derive band per DESIGN.md §3.2 & §5
  // low (< 0.40): amber, medium (0.40 - 0.75): marker, high (>= 0.75): seal
  let band: ConfidenceBand;
  let bandLabel: string;
  let colorClasses: string;
  let icon: React.ReactNode;

  if (score >= 0.75) {
    band = 'high';
    bandLabel = 'High Credibility';
    colorClasses = 'bg-status-success/15 text-status-success border-status-success/30';
    icon = <ShieldCheck className="w-3.5 h-3.5 text-status-success flex-shrink-0" aria-hidden="true" />;
  } else if (score >= 0.4) {
    band = 'medium';
    bandLabel = 'Calibrating';
    colorClasses = 'bg-action-primary/15 text-primary border-action-primary/30';
    icon = <ShieldCheck className="w-3.5 h-3.5 text-action-primary flex-shrink-0" aria-hidden="true" />;
  } else {
    band = 'low';
    bandLabel = 'City Prior';
    colorClasses = 'bg-status-warning/15 text-station-900 border-status-warning/40';
    icon = <AlertCircle className="w-3.5 h-3.5 text-status-warning flex-shrink-0" aria-hidden="true" />;
  }

  return (
    <span
      role="status"
      aria-label={`Confidence: ${percentage}%, ${bandLabel}, Z factor: ${score.toFixed(2)}`}
      className={`
        inline-flex items-center gap-1.5 font-ui font-medium rounded-full select-none border
        ${colorClasses}
        ${size === 'sm' ? 'text-[11px] py-0.5 px-2.5' : 'text-xs py-1 px-3'}
        ${className}
      `}
    >
      {icon}
      <span className="font-mono font-semibold">{percentage}%</span>
      <span className="text-[10px] uppercase tracking-wider opacity-85">({bandLabel})</span>
    </span>
  );
};
