import React from 'react';
import {
  BrowserRouter,
  Routes,
  Route,
  Navigate,
  Outlet,
  Link,
} from 'react-router-dom';
import { FieldShell } from '@civicbrain/ui';

import { MyOrdersView } from './views/MyOrdersView';
import { WorkOrderActionView } from './views/WorkOrderActionView';
import { SyncStatusView } from './views/SyncStatusView';

const FieldLayout: React.FC = () => {
  return (
    <FieldShell
      syncBadgeSlot={
        <Link
          to="/sync"
          className="font-mono text-xs text-secondary hover:text-primary px-2 py-0.5 border border-border rounded-sm outline-none focus:ring-1 focus:ring-focus"
          aria-label="View synchronization status"
        >
          ● 0 Queued
        </Link>
      }
    >
      <Outlet />
    </FieldShell>
  );
};

export const App: React.FC = () => {
  return (
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
  );
};
