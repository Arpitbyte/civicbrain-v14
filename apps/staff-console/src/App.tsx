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
  CivicShowcase,
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

const ROLE_LABELS: Record<StaffRole, { title: string; hindi: string }> = {
  admin: { title: 'Municipal Commissioner / Admin', hindi: 'आयुक्त / प्रशासक' },
  dispatcher: { title: 'Central Control Room Dispatcher', hindi: 'नियंत्रण कक्ष' },
  department_staff: { title: 'Department Officer', hindi: 'विभागीय अधिकारी' },
  zonal_supervisor: { title: 'Zonal Health / Engg Supervisor', hindi: 'जोनल पर्यवेक्षक' },
  field_worker: { title: 'Field Staff / Safai Karmachari', hindi: 'सफाई कर्मी / कर्मचारी' },
  corporator: { title: 'Elected Ward Councilor / Corporator', hindi: 'वार्ड पार्षद / नगरसेवक' },
};

const RoleSwitcher: React.FC = () => {
  const { role, setRole } = useAuth();
  return (
    <div className="space-y-1.5 p-2 bg-surface-raised/40 rounded border border-border/50">
      <div className="text-[10px] font-semibold text-text-secondary uppercase tracking-wider flex items-center justify-between">
        <span>सक्रिय भूमिका / Staff Role</span>
        <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" title="Active Session" />
      </div>
      <select
        value={role}
        onChange={e => setRole(e.target.value as StaffRole)}
        className="w-full bg-surface text-primary border border-border rounded text-xs py-1.5 px-2 focus:ring-1 focus:ring-focus outline-none cursor-pointer"
        aria-label="Switch municipal staff role"
      >
        {ALL_STAFF_ROLES.map(r => {
          const info = ROLE_LABELS[r];
          return (
            <option key={r} value={r}>
              {info ? `${info.title} (${info.hindi})` : r}
            </option>
          );
        })}
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

            {/* Civic Tier 1 Showcase */}
            <Route path="civic" element={<CivicShowcase />} />

            {/* Fallback */}
            <Route path="*" element={<Navigate to="/deck" replace />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
};
