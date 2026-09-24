/**
 * Karmi Sahayak Offline Mutation Store & Sync Engine
 * Conforms to UI_ARCHITECTURE.md §5 & SCREEN_SPECS.md §2.15, §2.16 & §2.17:
 * - Local mutation queue mirrors the backend's `sync_mutation_log` concept
 * - Cached work order catalog stored in local storage for instant offline rendering
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
  status: 'pending' | 'syncing' | 'synced' | 'failed' | 'conflict';
  conflictReason?: string;
  errorMessage?: string;
}

export interface CachedWorkOrder {
  id: string;
  incident_id: string;
  category: string;
  department: string;
  wardNumber: number;
  wardName: string;
  address: string;
  slaRemainingHours: number;
  status: 'created' | 'dispatched' | 'accepted' | 'in_progress' | 'completed' | 'cancelled';
  dispatched_at?: string;
  started_at?: string;
  citizenDescription?: string;
  lastCachedAt: string;
}

const MUTATIONS_STORAGE_KEY = 'civicbrain_field_mutations';
const ORDERS_CACHE_STORAGE_KEY = 'civicbrain_field_cached_orders';

// Authentic default baseline cache for field workers in BBMP / Indian civic wards
const DEFAULT_INITIAL_FIELD_ORDERS: CachedWorkOrder[] = [
  {
    id: 'WO-2026-8492',
    incident_id: 'INC-8892',
    category: 'सड़क एवं गड्ढे (Roads & Asphalt / Deep Pothole)',
    department: 'लोक निर्माण विभाग (PWD)',
    wardNumber: 102,
    wardName: 'Rajajinagar',
    address: '14th Main Rd, Near Post Office Junction',
    slaRemainingHours: 2.25,
    status: 'dispatched',
    dispatched_at: new Date(Date.now() - 3600000 * 2).toISOString(),
    citizenDescription:
      'Hazardous deep pothole on fast corner near post office. Two two-wheelers slipped during morning rain. Immediate asphalt patching requested.',
    lastCachedAt: new Date().toISOString(),
  },
  {
    id: 'WO-2026-8104',
    incident_id: 'INC-8104',
    category: 'विद्युत एवं प्रकाश (Streetlight / Broken Bracket)',
    department: 'विद्युत एवं ऊर्जा विभाग (BESCOM / Electrical)',
    wardNumber: 101,
    wardName: 'Malleshwaram',
    address: '8th Cross, Temple Road Corner',
    slaRemainingHours: 5.5,
    status: 'in_progress',
    dispatched_at: new Date(Date.now() - 3600000 * 6).toISOString(),
    started_at: new Date(Date.now() - 3600000 * 1).toISOString(),
    citizenDescription: 'Overhead light fixture hanging dangerously from pole bracket after high winds.',
    lastCachedAt: new Date().toISOString(),
  },
  {
    id: 'WO-2026-7933',
    incident_id: 'INC-7933',
    category: 'सीवरेज एवं जल निकासी (Drainage / Open Manhole)',
    department: 'जल आपूर्ति एवं सीवरेज बोर्ड (BWSSB)',
    wardNumber: 103,
    wardName: 'Gandhinagar',
    address: '5th Cross, Municipal Market Lane',
    slaRemainingHours: 1.1,
    status: 'dispatched',
    dispatched_at: new Date(Date.now() - 3600000 * 3).toISOString(),
    citizenDescription: 'Cast iron chamber cover displaced. High pedestrian hazard near busy vegetable market.',
    lastCachedAt: new Date().toISOString(),
  },
];

export const getQueuedMutations = (): QueuedMutation[] => {
  try {
    const raw = localStorage.getItem(MUTATIONS_STORAGE_KEY);
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
    localStorage.setItem(MUTATIONS_STORAGE_KEY, JSON.stringify(current));
  } catch (err) {
    console.error('[offlineSync] Error saving mutation:', err);
  }
};

export const removeMutation = (id: string): void => {
  try {
    const current = getQueuedMutations().filter((m) => m.id !== id);
    localStorage.setItem(MUTATIONS_STORAGE_KEY, JSON.stringify(current));
  } catch (err) {
    console.error('[offlineSync] Error removing mutation:', err);
  }
};

export const clearMutations = (): void => {
  try {
    localStorage.removeItem(MUTATIONS_STORAGE_KEY);
  } catch (err) {
    console.error('[offlineSync] Error clearing mutations:', err);
  }
};

/**
 * Reads cached work orders synchronously from local storage.
 * SCREEN_SPECS.md §2.15: Must render from cache BEFORE any network call resolves!
 */
export const getCachedWorkOrders = (): CachedWorkOrder[] => {
  try {
    const raw = localStorage.getItem(ORDERS_CACHE_STORAGE_KEY);
    if (raw) {
      const parsed = JSON.parse(raw);
      if (Array.isArray(parsed) && parsed.length > 0) {
        return parsed;
      }
    }
    // Initialize default cache if storage is empty on device first launch
    localStorage.setItem(ORDERS_CACHE_STORAGE_KEY, JSON.stringify(DEFAULT_INITIAL_FIELD_ORDERS));
    return DEFAULT_INITIAL_FIELD_ORDERS;
  } catch (err) {
    console.error('[offlineSync] Error reading cached work orders:', err);
    return DEFAULT_INITIAL_FIELD_ORDERS;
  }
};

/**
 * Persists refreshed work orders to local storage for offline durability.
 */
export const saveCachedWorkOrders = (orders: CachedWorkOrder[]): void => {
  try {
    localStorage.setItem(ORDERS_CACHE_STORAGE_KEY, JSON.stringify(orders));
  } catch (err) {
    console.error('[offlineSync] Error saving cached work orders:', err);
  }
};
