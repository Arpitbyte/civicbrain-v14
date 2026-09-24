import React from 'react';
import { Link } from 'react-router-dom';
import { useOfflineSync } from '../context/OfflineSyncContext';
import { SealMark, Button } from '@civicbrain/ui';
import {
  RefreshCw,
  Clock,
  Wifi,
  WifiOff,
  AlertTriangle,
  ArrowLeft,
  CheckCircle2,
  FileText,
} from 'lucide-react';

export const SyncStatusView: React.FC = () => {
  const { isOnline, queuedMutations, isSyncing, syncNow, disputeCount } = useOfflineSync();

  return (
    <div className="space-y-4 font-ui text-primary max-w-md mx-auto w-full pb-12">
      {/* Header & Back Link */}
      <div className="flex items-center justify-between pb-3 border-b border-border">
        <Link
          to="/my-orders"
          className="flex items-center gap-1.5 text-xs font-mono text-secondary hover:text-primary min-h-[48px] px-2"
          aria-label="Back to assigned work orders list"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>My Orders</span>
        </Link>
        <div className="flex items-center gap-1.5 font-mono text-xs text-secondary">
          {isOnline ? (
            <span className="flex items-center gap-1 text-status-success">
              <Wifi className="w-3.5 h-3.5" />
              <span>Online</span>
            </span>
          ) : (
            <span className="flex items-center gap-1 text-status-warning">
              <WifiOff className="w-3.5 h-3.5" />
              <span>Offline Mode</span>
            </span>
          )}
        </div>
      </div>

      <div>
        <h1 className="text-xl font-bold text-primary">Sync Status & Mutation Log</h1>
        <p className="font-mono text-xs text-secondary mt-0.5">
          Local Storage Queue • POST /v1/dispatch/sync
        </p>
      </div>

      {/* Sync Control Action Card */}
      <div className="p-4 bg-surface rounded-md border border-border space-y-3">
        <div className="flex items-center justify-between">
          <div>
            <div className="font-mono text-xs uppercase tracking-wider text-secondary">
              Queued Mutations
            </div>
            <div className="text-2xl font-bold font-mono text-primary mt-0.5">
              {queuedMutations.length}
              <span className="text-xs font-normal text-secondary ml-1">items pending</span>
            </div>
          </div>
          <button
            onClick={syncNow}
            disabled={!isOnline || queuedMutations.length === 0 || isSyncing}
            className={`min-h-[48px] px-4 font-ui font-bold text-sm rounded-sm flex items-center gap-2 transition-all ${
              isOnline && queuedMutations.length > 0 && !isSyncing
                ? 'bg-action-primary text-station-950 hover:opacity-90 active:scale-[0.98]'
                : 'bg-field-100 text-secondary border border-border cursor-not-allowed opacity-50'
            }`}
          >
            <RefreshCw className={`w-4 h-4 ${isSyncing ? 'animate-spin' : ''}`} />
            <span>{isSyncing ? 'Replaying Sync...' : 'Sync Now'}</span>
          </button>
        </div>

        {!isOnline && (
          <div className="p-2.5 bg-status-warning/15 border border-status-warning/40 rounded-sm text-xs font-mono text-status-warning flex items-center gap-2">
            <WifiOff className="w-4 h-4 shrink-0" />
            <span>Device is offline. Mutations will replay automatically on reconnect.</span>
          </div>
        )}
      </div>

      {/* Queued Mutations Manifest List */}
      <div className="space-y-2">
        <div className="text-xs font-mono font-semibold uppercase tracking-wider text-secondary">
          Pending Mutation Manifest
        </div>

        {queuedMutations.length === 0 ? (
          <div className="p-6 bg-surface rounded-md border border-border text-center space-y-3">
            <div className="flex justify-center">
              <SealMark
                authority="CIVIC_DISPATCH_LEDGER"
                timestamp={new Date().toLocaleTimeString()}
                verified
              />
            </div>
            <div className="font-bold text-sm text-primary">All Mutations Synced</div>
            <p className="text-xs font-mono text-secondary">
              Your device is in sync with municipal dispatch records.
            </p>
          </div>
        ) : (
          <div className="space-y-2">
            {queuedMutations.map((m) => (
              <div
                key={m.id}
                className="p-3 bg-surface rounded-md border border-border space-y-1 font-mono text-xs"
              >
                <div className="flex items-center justify-between">
                  <span className="text-action-primary font-bold">{m.type}</span>
                  <span className="text-[11px] text-secondary">
                    {new Date(m.queuedAt).toLocaleTimeString()}
                  </span>
                </div>
                <div className="text-primary font-semibold">Target: {m.workOrderId}</div>
                {m.payload.photoName && (
                  <div className="text-secondary text-[11px] flex items-center gap-1">
                    <FileText className="w-3 h-3 text-action-primary" />
                    <span>Attached proof: {m.payload.photoName}</span>
                  </div>
                )}
                {m.payload.notes && (
                  <div className="text-secondary text-[11px]">Notes: "{m.payload.notes}"</div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Supervisor Conflict Review Section */}
      <div className="space-y-2 pt-2 border-t border-border">
        <div className="text-xs font-mono font-semibold uppercase tracking-wider text-secondary">
          Supervisor Conflict Reviews ({disputeCount})
        </div>
        {disputeCount === 0 ? (
          <div className="p-3 bg-field-50 border border-border rounded-sm text-xs font-mono text-secondary flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-status-success shrink-0" />
            <span>No pending status collision conflicts.</span>
          </div>
        ) : (
          <div className="p-3 bg-status-danger/15 border border-status-danger/40 rounded-sm text-xs font-mono text-primary space-y-1">
            <div className="text-status-danger font-bold flex items-center gap-1.5">
              <AlertTriangle className="w-4 h-4" />
              <span>{disputeCount} Task Collision Flagged</span>
            </div>
            <p className="text-secondary text-[11px]">
              A supervisor is reviewing competing claims for this order.
            </p>
          </div>
        )}
      </div>
    </div>
  );
};
