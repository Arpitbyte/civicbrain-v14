// packages/ui/src/auth/roles.ts
// Single source of truth for user roles and permission routing per FRONTEND_CONTEXT.md §5

export type StaffRole =
  | 'citizen'
  | 'field_worker'
  | 'department_staff'
  | 'dispatcher'
  | 'zonal_supervisor'
  | 'corporator'
  | 'admin';

export const ALL_STAFF_ROLES: StaffRole[] = [
  'admin',
  'dispatcher',
  'department_staff',
  'zonal_supervisor',
  'corporator',
  'field_worker',
  'citizen',
];

/**
 * Default landing route for each role when accessing the platform.
 * Redirects here on unauthorized route attempts (never a dead-end 403 page).
 */
export const ROLE_DEFAULT_ROUTES: Record<StaffRole, string> = {
  admin: '/deck',
  dispatcher: '/deck',
  department_staff: '/ops',
  zonal_supervisor: '/pulse',
  corporator: '/corporator/digest',
  field_worker: '/my-orders',
  citizen: '/',
};

/**
 * Permitted workspaces per role in staff-console.
 * Ordered per DESIGN.md §2's table:
 * Command Deck -> Ops Board -> City Pulse -> Control Room -> Transparency Board
 */
export interface WorkspaceNavItem {
  id: string;
  label: string;
  path: string;
  workspace: 'command-deck' | 'ops-board' | 'city-pulse' | 'control-room' | 'transparency-board';
  allowedRoles: StaffRole[];
}

export const STAFF_CONSOLE_NAVIGATION: WorkspaceNavItem[] = [
  {
    id: 'command-deck',
    label: 'Command Deck',
    path: '/deck',
    workspace: 'command-deck',
    allowedRoles: ['dispatcher', 'admin'],
  },
  {
    id: 'ops-board',
    label: 'Ops Board',
    path: '/ops',
    workspace: 'ops-board',
    allowedRoles: ['department_staff', 'admin'],
  },
  {
    id: 'city-pulse',
    label: 'City Pulse',
    path: '/pulse',
    workspace: 'city-pulse',
    allowedRoles: ['zonal_supervisor', 'admin'],
  },
  {
    id: 'control-room',
    label: 'Control Room',
    path: '/control/staff',
    workspace: 'control-room',
    allowedRoles: ['admin'],
  },
  {
    id: 'transparency-board',
    label: 'Transparency Board',
    path: '/corporator/digest',
    workspace: 'transparency-board',
    allowedRoles: ['corporator', 'admin'],
  },
];
