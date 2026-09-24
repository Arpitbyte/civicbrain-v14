import React from 'react';
import {
  BrowserRouter,
  Routes,
  Route,
  Navigate,
  Outlet,
  Link,
} from 'react-router-dom';
import { FieldShell, OfflineSyncBadge } from '@civicbrain/ui';
import { OfflineSyncProvider, useOfflineSync } from './context/OfflineSyncContext';

import { MyOrdersView } from './views/MyOrdersView';
import { WorkOrderActionView } from './views/WorkOrderActionView';
import { SyncStatusView } from './views/SyncStatusView';

const FieldLayout: React.FC = () => {
  const { isOnline, queuedMutations, isSyncing, disputeCount, simulateOffline, toggleSimulateOffline } =
    useOfflineSync();

  return (
    <FieldShell
      syncBadgeSlot={
        <div className="flex items-center gap-2">
          {/* Dev Simulation Switch */}
          <button
            onClick={toggleSimulateOffline}
            className={`text-[10px] font-mono px-1.5 py-0.5 rounded-xs border transition-colors ${
              simulateOffline
                ? 'bg-status-warning/20 text-status-warning border-status-warning/50'
                : 'bg-surface text-secondary border-border hover:text-primary'
            }`}
            title="Toggle simulated offline network"
            aria-label={`Simulated offline network mode: ${simulateOffline ? 'ON' : 'OFF'}`}
          >
            {simulateOffline ? 'DEV: OFFLINE SIM' : 'DEV: ONLINE'}
          </button>

          <Link to="/sync" aria-label="View synchronization status">
            <OfflineSyncBadge
              isOnline={isOnline}
              pendingCount={queuedMutations.length}
              isSyncing={isSyncing}
              disputeCount={disputeCount}
            />
          </Link>
        </div>
      }
    >
      <Outlet />
    </FieldShell>
  );
};

export const App: React.FC = () => {
  return (
    <OfflineSyncProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<FieldLayout />}>
            <Route index element={<Navigate to="/my-orders" replace />} />
            <Route path="my-orders" element={<MyOrdersView />} />
            <Route path="orders/:id" element={<WorkOrderActionView />} />
            <Route path="sync" element={<SyncStatusView />} />
            <Route path="*" element={<Navigate to="/my-orders" replace />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </OfflineSyncProvider>
  );
};
