/**
 * Karmi Sahayak Offline Mutation Store & Sync Engine
 * Conforms to UI_ARCHITECTURE.md §5 & SCREEN_SPECS.md §2.16 & §2.17:
 * - Local mutation queue mirrors the backend's `sync_mutation_log` concept
 * - Every local action (start, resolve, photo capture) is queued as a mutation object
 * - Replayed via POST /v1/dispatch/sync on reconnect
 */

export interface QueuedMutation {
  id: string;
  type: 'START_WORK_ORDER' | 'RESOLVE_WORK_ORDER';
  workOrderId: string;
  payload: {
    photoName?: string;
    photoDataUrl?: string;
    notes?: string;
    timestamp: string;
  };
  queuedAt: string;
  status: 'pending' | 'syncing' | 'synced' | 'conflict';
  conflictReason?: string;
}

const STORAGE_KEY = 'civicbrain_field_mutations';

export const getQueuedMutations = (): QueuedMutation[] => {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch (err) {
    console.error('[offlineSync] Error reading mutations from storage:', err);
    return [];
  }
};

export const saveMutation = (mutation: QueuedMutation): void => {
  try {
    const current = getQueuedMutations();
    const existingIndex = current.findIndex((m) => m.id === mutation.id);
    if (existingIndex >= 0) {
      current[existingIndex] = mutation;
    } else {
      current.push(mutation);
    }
    localStorage.setItem(STORAGE_KEY, JSON.stringify(current));
  } catch (err) {
    console.error('[offlineSync] Error saving mutation:', err);
  }
};

export const removeMutation = (id: string): void => {
  try {
    const current = getQueuedMutations().filter((m) => m.id !== id);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(current));
  } catch (err) {
    console.error('[offlineSync] Error removing mutation:', err);
  }
};

export const clearMutations = (): void => {
  try {
    localStorage.removeItem(STORAGE_KEY);
  } catch (err) {
    console.error('[offlineSync] Error clearing mutations:', err);
  }
};
