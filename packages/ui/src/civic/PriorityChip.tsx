import React from 'react';
import { AlertCircle } from 'lucide-react';

export type PriorityLevel = 1 | 2 | 3 | 4;

export interface PriorityChipProps {
  /**
   * Priority rank tier (1 = Low, 2 = Medium, 3 = High, 4 = Critical)
   */
  level: PriorityLevel;
  /**
   * Optional exact numeric priority score (0.0 - 1.0 or 0 - 100)
   */
  score?: number;
  size?: 'sm' | 'md';
  className?: string;
}

/**
 * PriorityChip
 * Conforms to DESIGN.md §5 & §12, SCREEN_SPECS.md Tier 1:
 * - Single-hue Marker scale (never good/bad traffic lights!)
 * - Always pairs text label + numeric value + marker color (never color alone)
 * - Screen-reader accessible: "Priority 3 High, Score: 78"
 * - Status chip pill (radius-full)
 */
export const PriorityChip: React.FC<PriorityChipProps> = ({
  level,
  score,
  size = 'md',
  className = '',
}) => {
  const config = {
    1: {
      label: 'P1 Low',
      sla: '72h SLA',
      classes: 'bg-priority-1/20 text-station-800 border-priority-1',
    },
    2: {
      label: 'P2 Medium',
      sla: '48h SLA',
      classes: 'bg-priority-2/20 text-station-900 border-priority-2',
    },
    3: {
      label: 'P3 Urgent',
      sla: '24h SLA',
      classes: 'bg-priority-3/25 text-station-900 border-priority-3 font-semibold',
    },
    4: {
      label: 'P4 Emergency',
      sla: '6h SLA',
      classes: 'bg-priority-4 text-text-inverse border-priority-4 font-bold',
    },
  }[level];

  const formattedScore = score !== undefined ? (score <= 1.0 ? Math.round(score * 100) : Math.round(score)) : null;

  return (
    <span
      role="status"
      aria-label={`Priority Level ${level}: ${config.label}, ${config.sla}${formattedScore !== null ? `, Score: ${formattedScore}` : ''}`}
      className={`
        inline-flex items-center gap-1.5 rounded-full border font-ui select-none
        ${config.classes}
        ${size === 'sm' ? 'text-[11px] py-0.5 px-2' : 'text-xs py-1 px-2.5'}
        ${className}
      `}
    >
      <AlertCircle className="w-3 h-3 flex-shrink-0" aria-hidden="true" />
      <span>{config.label}</span>
      {formattedScore !== null && (
        <span className="font-mono opacity-90 pl-0.5">({formattedScore})</span>
      )}
    </span>
  );
};
