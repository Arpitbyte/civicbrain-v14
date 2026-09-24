import React from 'react';
import {
  CheckCircle2,
  Circle,
  AlertTriangle,
  RotateCcw,
  Clock,
  ArrowRight,
} from 'lucide-react';

export type IncidentStatusType =
  | 'reported'
  | 'triaged'
  | 'verified'
  | 'prioritized'
  | 'assigned'
  | 'in_progress'
  | 'resolved'
  | 'confirmed'
  | 'rejected'
  | 'appealed'
  | 'reopened';

export interface ObservationItem {
  id: string;
  department: string;
  category: string;
  status: IncidentStatusType;
  updated_at?: string;
  notes?: string;
}

export interface StatusTimelineProps {
  /**
   * List of observations.
   * If length > 1, implements the least-advanced-child aggregation rule at the top
   * and renders each observation's lifecycle below.
   * If length === 0, fails loudly / returns null (upstream data bug).
   */
  observations: ObservationItem[];
  className?: string;
}

// 11-State Progression Linear Rank matching backend (§A16, services.py PROGRESSION_RANK)
export const INCIDENT_PROGRESSION_RANK: Record<IncidentStatusType, number> = {
  reported: 1,
  triaged: 2,
  verified: 3,
  prioritized: 4,
  assigned: 5,
  in_progress: 6,
  reopened: 6,
  appealed: 6,
  resolved: 7,
  confirmed: 8,
  rejected: 0, // Special state
};

// 6 Core Canonical milestones for citizen and staff view
const LINEAR_STAGES: Array<{ status: IncidentStatusType; label: string }> = [
  { status: 'reported', label: 'Reported' },
  { status: 'triaged', label: 'Triaged' },
  { status: 'verified', label: 'Verified' },
  { status: 'assigned', label: 'Assigned' },
  { status: 'in_progress', label: 'In Progress' },
  { status: 'resolved', label: 'Resolved' },
];

/**
 * Computes parent aggregate status according to FRONTEND_CONTEXT.md §4 & §7.2
 * and backend calculate_intake_status_from_children logic:
 * - If all children are rejected -> rejected
 * - If at least one resolved and others active -> partially_resolved
 * - Otherwise min rank among non-rejected children
 */
export function computeLeastAdvancedChildStatus(
  observations: ObservationItem[]
): {
  parentStatus: string;
  isPartiallyResolved: boolean;
  minStatus: IncidentStatusType;
} {
  if (!observations || observations.length === 0) {
    return { parentStatus: 'submitted', isPartiallyResolved: false, minStatus: 'reported' };
  }

  const allRejected = observations.every((o) => o.status === 'rejected');
  if (allRejected) {
    return { parentStatus: 'rejected', isPartiallyResolved: false, minStatus: 'rejected' };
  }

  const activeObs = observations.filter((o) => o.status !== 'rejected');
  if (activeObs.length === 0) {
    return { parentStatus: 'rejected', isPartiallyResolved: false, minStatus: 'rejected' };
  }

  const hasResolved = activeObs.some(
    (o) => INCIDENT_PROGRESSION_RANK[o.status] >= INCIDENT_PROGRESSION_RANK.resolved
  );
  const hasUnresolved = activeObs.some(
    (o) => INCIDENT_PROGRESSION_RANK[o.status] < INCIDENT_PROGRESSION_RANK.resolved
  );

  const minObs = activeObs.reduce((min, curr) =>
    INCIDENT_PROGRESSION_RANK[curr.status] < INCIDENT_PROGRESSION_RANK[min.status] ? curr : min
  );

  if (hasResolved && hasUnresolved) {
    return {
      parentStatus: 'partially_resolved',
      isPartiallyResolved: true,
      minStatus: minObs.status,
    };
  }

  return {
    parentStatus: minObs.status,
    isPartiallyResolved: false,
    minStatus: minObs.status,
  };
}

/**
 * StatusTimeline
 * Conforms to FRONTEND_CONTEXT.md §4 & §7.2, SCREEN_SPECS.md Tier 1:
 * - Implements least-advanced-child aggregation rule when multiple observations exist
 * - Renders per-observation lifecycle bars (never collapsed to one generic progress bar)
 * - Accessibility: Step states read as text + stage position (never color-only per DESIGN.md §12)
 * - Fails loudly in dev if zero observations provided
 */
export const StatusTimeline: React.FC<StatusTimelineProps> = ({
  observations,
  className = '',
}) => {
  // Hard requirement: zero observations is an upstream data bug — fail loudly in dev, do not render
  if (!observations || observations.length === 0) {
    if (process.env.NODE_ENV !== 'production') {
      console.error(
        '[StatusTimeline] Invariant Violation: Zero observations provided. A report cannot exist without observations.'
      );
    }
    return null;
  }

  const hasMultiple = observations.length > 1;
  const { parentStatus, isPartiallyResolved, minStatus } = computeLeastAdvancedChildStatus(observations);

  return (
    <div className={`flex flex-col gap-6 w-full font-ui text-primary ${className}`}>
      {/* If multi-observation, show Parent Aggregated Banner */}
      {hasMultiple && (
        <div
          role="status"
          aria-live="polite"
          className="p-4 rounded-md border border-border bg-surface-raised flex flex-col gap-1.5"
        >
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-text-secondary uppercase tracking-wider">
              Aggregated Case Status (Least-Advanced Child Rule)
            </span>
            <span
              className={`
                px-2.5 py-0.5 rounded-full text-xs font-semibold uppercase tracking-wider border
                ${
                  isPartiallyResolved
                    ? 'bg-action-primary/15 text-primary border-action-primary/40'
                    : parentStatus === 'resolved' || parentStatus === 'confirmed'
                    ? 'bg-status-success/15 text-status-success border-status-success/30'
                    : 'bg-status-warning/15 text-station-900 border-status-warning/40'
                }
              `}
            >
              {isPartiallyResolved ? 'Partially Resolved' : parentStatus.replace('_', ' ')}
            </span>
          </div>

          <p className="text-xs text-text-secondary">
            {isPartiallyResolved
              ? 'At least 1 department has resolved their task, but overall report remains active until all issues are completed.'
              : `Overall report is anchored to the least-advanced child (${minStatus.replace('_', ' ')}).`}
          </p>
        </div>
      )}

      {/* Observation Lifecycles */}
      <div className="flex flex-col gap-6">
        {observations.map((obs, idx) => {
          const currentRank = INCIDENT_PROGRESSION_RANK[obs.status] ?? 1;
          const isRejected = obs.status === 'rejected';
          const isReopened = obs.status === 'reopened';
          const isAppealed = obs.status === 'appealed';

          return (
            <div
              key={obs.id || idx}
              className="p-4 rounded-md border border-border bg-surface flex flex-col gap-4"
            >
              {/* Observation Header */}
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1 pb-2 border-b border-border">
                <div className="flex items-center gap-2">
                  <span className="font-mono text-xs font-bold text-text-secondary">
                    #{idx + 1}
                  </span>
                  <span className="font-semibold text-sm text-primary">
                    {obs.category}
                  </span>
                  <span className="text-xs text-text-secondary font-mono">
                    ({obs.department})
                  </span>
                </div>

                <div className="flex items-center gap-2 self-start sm:self-auto">
                  {obs.updated_at && (
                    <span className="text-[11px] font-mono text-text-secondary">
                      Updated: {obs.updated_at}
                    </span>
                  )}
                  <span
                    className={`
                      text-xs font-semibold px-2 py-0.5 rounded-full border
                      ${
                        obs.status === 'resolved' || obs.status === 'confirmed'
                          ? 'bg-status-success/15 text-status-success border-status-success/30'
                          : isRejected
                          ? 'bg-status-danger/15 text-status-danger border-status-danger/30'
                          : 'bg-surface-raised text-primary border-border'
                      }
                    `}
                  >
                    {obs.status.replace('_', ' ')}
                  </span>
                </div>
              </div>

              {/* Special State Notice (Rejected, Reopened, Appealed) */}
              {(isRejected || isReopened || isAppealed) && (
                <div
                  role="alert"
                  className="text-xs p-2.5 rounded-sm bg-surface-raised border border-border flex items-center gap-2"
                >
                  {isRejected ? (
                    <AlertTriangle className="w-4 h-4 text-status-danger flex-shrink-0" />
                  ) : (
                    <RotateCcw className="w-4 h-4 text-status-warning flex-shrink-0" />
                  )}
                  <span>
                    {isRejected
                      ? 'Issue was reviewed and rejected. An appeal can be submitted with additional evidence.'
                      : isReopened
                      ? 'Issue was reopened after citizen resolution dispute. Field crew re-dispatched.'
                      : 'Supervisor appeal in progress following citizen review.'}
                  </span>
                </div>
              )}

              {/* Stepper Progress Track */}
              <nav aria-label={`Progress tracker for ${obs.category}`}>
                <ol className="flex items-center justify-between w-full relative">
                  {LINEAR_STAGES.map((stage, sIdx) => {
                    const stageRank = INCIDENT_PROGRESSION_RANK[stage.status];
                    const isCompleted = currentRank > stageRank || currentRank >= 7;
                    const isCurrent = currentRank === stageRank;

                    return (
                      <li
                        key={stage.status}
                        className="flex flex-col items-center flex-1 relative group"
                        aria-current={isCurrent ? 'step' : undefined}
                      >
                        {/* Connecting Line between steps */}
                        {sIdx > 0 && (
                          <div
                            className={`
                              absolute top-3 right-1/2 left-[-50%] h-0.5 -z-0
                              ${
                                currentRank >= stageRank
                                  ? 'bg-action-primary'
                                  : 'bg-border'
                              }
                            `}
                            aria-hidden="true"
                          />
                        )}

                        {/* Step Marker */}
                        <div
                          className={`
                            w-6 h-6 rounded-full flex items-center justify-center z-10 border transition-colors
                            ${
                              isCompleted
                                ? 'bg-action-primary border-action-primary text-text-inverse'
                                : isCurrent
                                ? 'bg-surface-raised border-action-primary text-action-primary ring-2 ring-focus'
                                : 'bg-surface border-border text-text-secondary'
                            }
                          `}
                        >
                          {isCompleted ? (
                            <CheckCircle2 className="w-3.5 h-3.5 stroke-[2.5]" aria-hidden="true" />
                          ) : isCurrent ? (
                            <span className="w-2 h-2 rounded-full bg-action-primary animate-pulse" />
                          ) : (
                            <span className="text-[10px] font-mono">{sIdx + 1}</span>
                          )}
                        </div>

                        {/* Step Label */}
                        <span
                          className={`
                            text-[11px] mt-1.5 font-medium select-none text-center
                            ${
                              isCurrent
                                ? 'text-primary font-bold'
                                : isCompleted
                                ? 'text-primary'
                                : 'text-text-secondary'
                            }
                          `}
                        >
                          {stage.label}
                        </span>

                        {/* Screen reader detail */}
                        <span className="sr-only">
                          {stage.label}: {isCompleted ? 'Completed' : isCurrent ? 'Current step' : 'Pending'}
                        </span>
                      </li>
                    );
                  })}
                </ol>
              </nav>

              {obs.notes && (
                <div className="text-xs text-text-secondary bg-surface-raised p-2.5 rounded-sm border border-border/60">
                  <strong className="text-primary font-medium">Field Observation: </strong>
                  {obs.notes}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};
