import React from 'react';
import { Wifi, WifiOff, RefreshCw, AlertTriangle } from 'lucide-react';

export interface OfflineSyncBadgeProps {
  /**
   * Count of queued local mutations in IndexedDB pending replay
   */
  pendingCount?: number;
  /**
   * Whether the client network is currently online
   */
  isOnline?: boolean;
  /**
   * Count of detected sync collisions or disputed items
   */
  disputeCount?: number;
  /**
   * Whether a sync replay is actively in progress
   */
  isSyncing?: boolean;
  onClick?: () => void;
  className?: string;
}

/**
 * OfflineSyncBadge
 * Conforms to SCREEN_SPECS.md §0.3 & Tier 1:
 * - Persistent badge for Karmi Sahayak and staff shells
 * - Shows queued mutation count, online/offline status, and tap for Sync Status
 * - Pill radius-full status chip
 */
export const OfflineSyncBadge: React.FC<OfflineSyncBadgeProps> = ({
  pendingCount = 0,
  isOnline = true,
  disputeCount = 0,
  isSyncing = false,
  onClick,
  className = '',
}) => {
  const hasPending = pendingCount > 0;
  const hasDisputes = disputeCount > 0;

  let statusBg = 'bg-surface-raised text-primary border-border';
  let icon = <Wifi className="w-3.5 h-3.5 text-status-success" aria-hidden="true" />;
  let labelText = 'Live Synced';

  if (!isOnline) {
    statusBg = 'bg-status-warning/15 text-station-900 border-status-warning/40';
    icon = <WifiOff className="w-3.5 h-3.5 text-status-warning" aria-hidden="true" />;
    labelText = hasPending ? `Offline (${pendingCount} queued)` : 'Offline';
  } else if (isSyncing) {
    statusBg = 'bg-action-primary/15 text-primary border-action-primary/30';
    icon = <RefreshCw className="w-3.5 h-3.5 text-action-primary animate-spin" aria-hidden="true" />;
    labelText = `Syncing ${pendingCount}...`;
  } else if (hasDisputes) {
    statusBg = 'bg-status-danger/15 text-status-danger border-status-danger/30';
    icon = <AlertTriangle className="w-3.5 h-3.5 text-status-danger" aria-hidden="true" />;
    labelText = `${disputeCount} Sync Collision`;
  } else if (hasPending) {
    statusBg = 'bg-action-primary/15 text-primary border-action-primary/30';
    icon = <RefreshCw className="w-3.5 h-3.5 text-action-primary" aria-hidden="true" />;
    labelText = `${pendingCount} Queued`;
  }

  return (
    <button
      type="button"
      onClick={onClick}
      role="status"
      aria-label={`Sync Status: ${labelText}`}
      className={`
        inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-ui font-medium border
        select-none cursor-pointer transition-transform duration-fast active:scale-95 outline-none
        focus-visible:ring-2 focus-visible:ring-focus
        ${statusBg}
        ${className}
      `}
    >
      {icon}
      <span className="font-mono text-[11px] font-semibold">{labelText}</span>
    </button>
  );
};
