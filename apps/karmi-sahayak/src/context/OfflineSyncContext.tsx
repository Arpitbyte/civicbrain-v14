import React, { createContext, useContext, useState, useEffect } from 'react';
import {
  QueuedMutation,
  getQueuedMutations,
  saveMutation,
  removeMutation,
} from '../services/offlineSync';

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
  disputeCount: number;
  syncNow: () => Promise<void>;
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
  const [disputeCount, setDisputeCount] = useState<number>(0);

  // Effective online state
  const effectiveOnline = nativeOnline && !simulateOffline;

  // Sync listener
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

  const toggleSimulateOffline = () => {
    setSimulateOffline((prev) => !prev);
  };

  const queueStartOrder = async (workOrderId: string): Promise<{ queuedLocally: boolean }> => {
    if (effectiveOnline) {
      // Simulate direct live POST .../start API success
      await new Promise((r) => setTimeout(r, 400));
      return { queuedLocally: false };
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
      // Simulate live POST .../resolve API success
      await new Promise((r) => setTimeout(r, 600));
      return { queuedLocally: false };
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

  const syncNow = async (): Promise<void> => {
    if (!effectiveOnline || queuedMutations.length === 0) return;

    setIsSyncing(true);
    // Simulate replaying queued mutations via POST /v1/dispatch/sync
    await new Promise((r) => setTimeout(r, 1200));

    // For test purposes, mark as synced and remove
    queuedMutations.forEach((m) => removeMutation(m.id));
    setQueuedMutations([]);
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
        disputeCount,
        syncNow,
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
