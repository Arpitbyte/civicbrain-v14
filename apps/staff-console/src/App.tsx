import React from 'react';
import {
  BrowserRouter,
  Routes,
  Route,
  Navigate,
  Outlet,
  useLocation,
} from 'react-router-dom';
import {
  StaffConsoleShell,
  NavRail,
  RoleGate,
  AuthProvider,
  useAuth,
  StaffWorkspace,
  StaffRole,
  ALL_STAFF_ROLES,
  PrimitivesShowcase,
} from '@civicbrain/ui';

import { IncidentQueueView } from './views/IncidentQueueView';
import { IncidentDetailView } from './views/IncidentDetailView';
import { PrioritizationReRunView } from './views/PrioritizationReRunView';
import { ConflictAdjudicationView } from './views/ConflictAdjudicationView';
import { WorkOrderDispatchView } from './views/WorkOrderDispatchView';
import { DepartmentQueueView } from './views/DepartmentQueueView';
import { WorkOrderDetailView } from './views/WorkOrderDetailView';
import { HeatmapClusterView } from './views/HeatmapClusterView';
import { CausalGraphView } from './views/CausalGraphView';
import { EtaConfidenceView } from './views/EtaConfidenceView';
import { StaffDirectoryView } from './views/StaffDirectoryView';
import { BulkImportView } from './views/BulkImportView';
import { OrgHierarchyView } from './views/OrgHierarchyView';
import { TaxonomyGovernanceView } from './views/TaxonomyGovernanceView';
import { AhpWeightCalibrationView } from './views/AhpWeightCalibrationView';
import { ServiceTimePriorsView } from './views/ServiceTimePriorsView';
import { CouncilorDigestView } from './views/CouncilorDigestView';

const RoleSwitcher: React.FC = () => {
  const { role, setRole } = useAuth();
  return (
    <div className="space-y-1">
      <div className="text-[11px] font-mono text-secondary uppercase tracking-wider">
        Active Role (Dev Gating)
      </div>
      <select
        value={role}
        onChange={e => setRole(e.target.value as StaffRole)}
        className="w-full bg-surface text-primary border border-border rounded-sm text-xs font-mono p-1 focus:ring-1 focus:ring-focus outline-none"
        aria-label="Switch staff role for testing"
      >
        {ALL_STAFF_ROLES.map(r => (
          <option key={r} value={r}>
            {r}
          </option>
        ))}
      </select>
    </div>
  );
};

const StaffConsoleLayout: React.FC = () => {
  const location = useLocation();

  // Determine workspace from current route
  let activeWorkspace: StaffWorkspace = 'command-deck';
  if (location.pathname.startsWith('/ops')) {
    activeWorkspace = 'ops-board';
  } else if (location.pathname.startsWith('/pulse')) {
    activeWorkspace = 'city-pulse';
  } else if (location.pathname.startsWith('/control')) {
    activeWorkspace = 'control-room';
  }

  return (
    <StaffConsoleShell
      workspace={activeWorkspace}
      navSlot={<NavRail />}
      userSlot={<RoleSwitcher />}
    >
      <Outlet />
    </StaffConsoleShell>
  );
};

export const App: React.FC = () => {
  return (
    <AuthProvider initialRole="admin">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<StaffConsoleLayout />}>
            <Route index element={<Navigate to="/deck" replace />} />

            {/* Command Deck Routes (/deck) */}
            <Route
              path="deck"
              element={
                <RoleGate allowedRoles={['dispatcher', 'admin']}>
                  <IncidentQueueView />
                </RoleGate>
              }
            />
            <Route
              path="deck/incidents/:id"
              element={
                <RoleGate allowedRoles={['dispatcher', 'admin']}>
                  <IncidentDetailView />
                </RoleGate>
              }
            />
            <Route
              path="deck/prioritize/:id"
              element={
                <RoleGate allowedRoles={['dispatcher', 'admin']}>
                  <PrioritizationReRunView />
                </RoleGate>
              }
            />
            <Route
              path="deck/conflicts"
              element={
                <RoleGate allowedRoles={['dispatcher', 'admin']}>
                  <ConflictAdjudicationView />
                </RoleGate>
              }
            />
            <Route
              path="deck/dispatch/new"
              element={
                <RoleGate allowedRoles={['dispatcher', 'department_staff', 'admin']}>
                  <WorkOrderDispatchView />
                </RoleGate>
              }
            />

            {/* Ops Board Routes (/ops) */}
            <Route
              path="ops"
              element={
                <RoleGate allowedRoles={['department_staff', 'admin']}>
                  <DepartmentQueueView />
                </RoleGate>
              }
            />
            <Route
              path="ops/work-orders/:id"
              element={
                <RoleGate allowedRoles={['department_staff', 'admin']}>
                  <WorkOrderDetailView />
                </RoleGate>
              }
            />

            {/* City Pulse Routes (/pulse) */}
            <Route
              path="pulse"
              element={
                <RoleGate allowedRoles={['zonal_supervisor', 'admin']}>
                  <HeatmapClusterView />
                </RoleGate>
              }
            />
            <Route
              path="pulse/causal"
              element={
                <RoleGate allowedRoles={['zonal_supervisor', 'admin']}>
                  <CausalGraphView />
                </RoleGate>
              }
            />
            <Route
              path="pulse/eta/:incidentId"
              element={
                <RoleGate allowedRoles={['zonal_supervisor', 'admin']}>
                  <EtaConfidenceView />
                </RoleGate>
              }
            />

            {/* Control Room Routes (/control) */}
            <Route
              path="control/staff"
              element={
                <RoleGate allowedRoles={['admin']}>
                  <StaffDirectoryView />
                </RoleGate>
              }
            />
            <Route
              path="control/staff/import"
              element={
                <RoleGate allowedRoles={['admin']}>
                  <BulkImportView />
                </RoleGate>
              }
            />
            <Route
              path="control/hierarchy"
              element={
                <RoleGate allowedRoles={['admin']}>
                  <OrgHierarchyView />
                </RoleGate>
              }
            />
            <Route
              path="control/taxonomy"
              element={
                <RoleGate allowedRoles={['admin']}>
                  <TaxonomyGovernanceView />
                </RoleGate>
              }
            />
            <Route
              path="control/ahp"
              element={
                <RoleGate allowedRoles={['admin']}>
                  <AhpWeightCalibrationView />
                </RoleGate>
              }
            />
            <Route
              path="control/priors"
              element={
                <RoleGate allowedRoles={['admin']}>
                  <ServiceTimePriorsView />
                </RoleGate>
              }
            />

            {/* Corporator Digest (/corporator/digest) */}
            <Route
              path="corporator/digest"
              element={
                <RoleGate allowedRoles={['corporator', 'admin']}>
                  <CouncilorDigestView />
                </RoleGate>
              }
            />

            {/* Primitives Tier 0 Showcase */}
            <Route path="primitives" element={<PrimitivesShowcase />} />

            {/* Fallback */}
            <Route path="*" element={<Navigate to="/deck" replace />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
};
