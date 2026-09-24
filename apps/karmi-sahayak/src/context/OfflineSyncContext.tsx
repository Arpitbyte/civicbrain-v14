import React, { createContext, useContext, useState, useEffect } from 'react';
import {
  QueuedMutation,
  getQueuedMutations,
  saveMutation,
  removeMutation,
} from '../services/offlineSync';

export interface WorkerConflictItem {
  client_mutation_id: string;
  status: string;
  conflict_reason?: string | null;
}

export interface SyncProgress {
  current: number;
  total: number;
}

export interface OfflineSyncContextValue {
  isOnline: boolean;
  simulateOffline: boolean;
  toggleSimulateOffline: () => void;
  queuedMutations: QueuedMutation[];
  queueStartOrder: (workOrderId: string) => Promise<{ queuedLocally: boolean }>;
  queueResolveOrder: (
    workOrderId: string,
    photo: { name: string; dataUrl: string },
    notes: string
  ) => Promise<{ queuedLocally: boolean }>;
  isSyncing: boolean;
  syncProgress: SyncProgress;
  disputeCount: number;
  conflicts: WorkerConflictItem[];
  syncNow: () => Promise<void>;
  retryMutation: (mutationId: string) => Promise<void>;
  isOrderQueued: (workOrderId: string) => boolean;
  getOrderPendingAction: (workOrderId: string) => QueuedMutation | undefined;
}

const OfflineSyncContext = createContext<OfflineSyncContextValue | undefined>(undefined);

export const OfflineSyncProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [nativeOnline, setNativeOnline] = useState<boolean>(
    typeof navigator !== 'undefined' ? navigator.onLine : true
  );
  const [simulateOffline, setSimulateOffline] = useState<boolean>(false);
  const [queuedMutations, setQueuedMutations] = useState<QueuedMutation[]>([]);
  const [isSyncing, setIsSyncing] = useState<boolean>(false);
  const [syncProgress, setSyncProgress] = useState<SyncProgress>({ current: 0, total: 0 });
  const [conflicts, setConflicts] = useState<WorkerConflictItem[]>([]);

  // Effective online state
  const effectiveOnline = nativeOnline && !simulateOffline;

  // Sync listener & periodic conflicts check
  useEffect(() => {
    const handleOnline = () => setNativeOnline(true);
    const handleOffline = () => setNativeOnline(false);

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    // Initial mutations load
    setQueuedMutations(getQueuedMutations());

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  // Fetch conflict list when online
  useEffect(() => {
    async function fetchConflicts() {
      if (!effectiveOnline) return;
      try {
        const res = await fetch('/v1/dispatch/sync/conflicts');
        if (res.ok) {
          const data = await res.json();
          if (Array.isArray(data)) {
            setConflicts(data);
          }
        }
      } catch {
        // non-blocking
      }
    }
    fetchConflicts();
  }, [effectiveOnline]);

  const toggleSimulateOffline = () => {
    setSimulateOffline((prev) => !prev);
  };

  const queueStartOrder = async (workOrderId: string): Promise<{ queuedLocally: boolean }> => {
    if (effectiveOnline) {
      try {
        const res = await fetch(`/v1/dispatch/work-orders/${workOrderId}/start`, {
          method: 'POST',
        });
        if (res.ok) {
          return { queuedLocally: false };
        }
      } catch {
        // Network failure in field: queue mutation locally
      }
    }

    // Offline: queue mutation locally
    const mutation: QueuedMutation = {
      id: `mut-${Date.now()}-${Math.random().toString(36).substr(2, 6)}`,
      type: 'START_WORK_ORDER',
      workOrderId,
      payload: {
        timestamp: new Date().toISOString(),
      },
      queuedAt: new Date().toISOString(),
      status: 'pending',
    };

    saveMutation(mutation);
    setQueuedMutations(getQueuedMutations());
    return { queuedLocally: true };
  };

  const queueResolveOrder = async (
    workOrderId: string,
    photo: { name: string; dataUrl: string },
    notes: string
  ): Promise<{ queuedLocally: boolean }> => {
    if (effectiveOnline) {
      try {
        const res = await fetch(`/v1/dispatch/work-orders/${workOrderId}/resolve`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            photo_urls: [photo.dataUrl],
            notes,
            latitude: 12.9784,
            longitude: 77.5621,
          }),
        });
        if (res.ok) {
          return { queuedLocally: false };
        }
      } catch {
        // Fall back to offline queue
      }
    }

    // Offline: queue resolution mutation locally
    const mutation: QueuedMutation = {
      id: `mut-${Date.now()}-${Math.random().toString(36).substr(2, 6)}`,
      type: 'RESOLVE_WORK_ORDER',
      workOrderId,
      payload: {
        photoName: photo.name,
        photoDataUrl: photo.dataUrl,
        notes,
        timestamp: new Date().toISOString(),
      },
      queuedAt: new Date().toISOString(),
      status: 'pending',
    };

    saveMutation(mutation);
    setQueuedMutations(getQueuedMutations());
    return { queuedLocally: true };
  };

  // Replay a single mutation (Per-mutation retry pattern)
  const retryMutation = async (mutationId: string): Promise<void> => {
    if (!effectiveOnline) return;

    const currentMutations = getQueuedMutations();
    const target = currentMutations.find((m) => m.id === mutationId);
    if (!target) return;

    // Mark as syncing
    target.status = 'syncing';
    target.errorMessage = undefined;
    saveMutation(target);
    setQueuedMutations(getQueuedMutations());

    try {
      // Replay against /v1/dispatch/sync
      const syncPayload = {
        client_timestamp: new Date().toISOString(),
        mutations: [
          {
            mutation_id: target.id,
            mutation_type: target.type,
            work_order_id: target.workOrderId,
            payload: target.payload,
          },
        ],
      };

      const res = await fetch('/v1/dispatch/sync', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(syncPayload),
      });

      if (!res.ok) {
        throw new Error(`Sync server responded with ${res.status}`);
      }

      // Success: remove mutation from queue
      removeMutation(target.id);
    } catch (err: any) {
      target.status = 'failed';
      target.errorMessage = err.message || 'Retry failed to communicate with dispatch server';
      saveMutation(target);
    } finally {
      setQueuedMutations(getQueuedMutations());
    }
  };

  // Replay all queued mutations with determinate progress (DESIGN.md §10)
  const syncNow = async (): Promise<void> => {
    if (!effectiveOnline || queuedMutations.length === 0) return;

    setIsSyncing(true);
    const total = queuedMutations.length;
    setSyncProgress({ current: 0, total });

    for (let i = 0; i < total; i++) {
      const mutation = queuedMutations[i];
      setSyncProgress({ current: i + 1, total });

      try {
        mutation.status = 'syncing';
        saveMutation(mutation);
        setQueuedMutations(getQueuedMutations());

        // Small pacing for determinate feedback per DESIGN.md §10
        await new Promise((r) => setTimeout(r, 300));

        const res = await fetch('/v1/dispatch/sync', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            client_timestamp: new Date().toISOString(),
            mutations: [
              {
                mutation_id: mutation.id,
                mutation_type: mutation.type,
                work_order_id: mutation.workOrderId,
                payload: mutation.payload,
              },
            ],
          }),
        });

        if (res.ok) {
          removeMutation(mutation.id);
        } else {
          mutation.status = 'failed';
          mutation.errorMessage = `Server error ${res.status}`;
          saveMutation(mutation);
        }
      } catch (err: any) {
        mutation.status = 'failed';
        mutation.errorMessage = err.message || 'Network timeout';
        saveMutation(mutation);
      }
    }

    setQueuedMutations(getQueuedMutations());
    setIsSyncing(false);
  };

  const isOrderQueued = (workOrderId: string): boolean => {
    return queuedMutations.some((m) => m.workOrderId === workOrderId);
  };

  const getOrderPendingAction = (workOrderId: string): QueuedMutation | undefined => {
    return queuedMutations.find((m) => m.workOrderId === workOrderId);
  };

  return (
    <OfflineSyncContext.Provider
      value={{
        isOnline: effectiveOnline,
        simulateOffline,
        toggleSimulateOffline,
        queuedMutations,
        queueStartOrder,
        queueResolveOrder,
        isSyncing,
        syncProgress,
        disputeCount: conflicts.length,
        conflicts,
        syncNow,
        retryMutation,
        isOrderQueued,
        getOrderPendingAction,
      }}
    >
      {children}
    </OfflineSyncContext.Provider>
  );
};

export const useOfflineSync = () => {
  const context = useContext(OfflineSyncContext);
  if (!context) {
    throw new Error('useOfflineSync must be used within an OfflineSyncProvider');
  }
  return context;
};
