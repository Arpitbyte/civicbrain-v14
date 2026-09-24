import { IncidentStatusType } from '@civicbrain/ui';

/**
 * Authoritative 11-State Incident Lifecycle (§A16, FRONTEND_CONTEXT.md §4,
 * and PROJECT_REFERENCE_FOR_FRONTEND.md §7.1 state diagram).
 *
 * reported -> triaged, rejected
 * triaged -> verified, rejected
 * verified -> prioritized
 * prioritized -> assigned
 * assigned -> in_progress
 * in_progress -> resolved
 * resolved -> confirmed, appealed
 * rejected -> appealed
 * appealed -> reopened
 * reopened -> prioritized
 * confirmed -> (terminal)
 */
export const VALID_NEXT_STATUS_TRANSITIONS: Record<IncidentStatusType, IncidentStatusType[]> = {
  reported: ['triaged', 'rejected'],
  triaged: ['verified', 'rejected'],
  verified: ['prioritized'],
  prioritized: ['assigned'],
  assigned: ['in_progress'],
  in_progress: ['resolved'],
  resolved: ['confirmed', 'appealed'],
  rejected: ['appealed'],
  appealed: ['reopened'],
  reopened: ['prioritized'],
  confirmed: [],
};

export const STATUS_LABELS: Record<IncidentStatusType, string> = {
  reported: 'Reported',
  triaged: 'Triage Case',
  verified: 'Mark Verified',
  prioritized: 'Prioritize Case',
  assigned: 'Dispatch / Assign',
  in_progress: 'Commence Work',
  resolved: 'Mark Resolved',
  confirmed: 'Confirm & Close',
  rejected: 'Reject Defect',
  appealed: 'File Dispute Appeal',
  reopened: 'Reopen Incident',
};

export function getValidNextStatuses(currentStatus: IncidentStatusType): IncidentStatusType[] {
  return VALID_NEXT_STATUS_TRANSITIONS[currentStatus] || [];
}
