import React, { useState } from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import {
  LayoutDashboard,
  ClipboardList,
  MapPin,
  Settings,
  FileText,
  Menu,
  X,
} from 'lucide-react';
import { useAuth } from '../auth/AuthContext';
import { STAFF_CONSOLE_NAVIGATION, WorkspaceNavItem } from '../auth/roles';

export interface NavRailProps {
  className?: string;
}

const ICON_MAP: Record<string, React.ComponentType<{ className?: string }>> = {
  'command-deck': LayoutDashboard,
  'ops-board': ClipboardList,
  'city-pulse': MapPin,
  'control-room': Settings,
  'transparency-board': FileText,
};

/**
 * NavRail
 * Primary navigation for StaffConsoleShell.
 * Filters items strictly to workspaces the active role is permitted to access.
 * Responsive: Collapses to icon-only between 1024px and 1280px; hamburger toggle below 1024px.
 * Motion: Quiet — instant state swap.
 * Accessibility: Fully keyboard navigable, aria-current="page".
 */
export const NavRail: React.FC<NavRailProps> = ({ className = '' }) => {
  const { role } = useAuth();
  const location = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  // Filter items strictly by role
  const accessibleItems: WorkspaceNavItem[] = STAFF_CONSOLE_NAVIGATION.filter(item =>
    item.allowedRoles.includes(role)
  );

  return (
    <>
      {/* Mobile Hamburger Header (Visible strictly below 1024px) */}
      <div className="lg:hidden flex items-center justify-between p-2 border-b border-border bg-surface">
        <span className="font-ui font-semibold text-sm text-primary">Console Menu</span>
        <button
          type="button"
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          className="p-2 text-primary focus:outline-none focus:ring-2 focus:ring-focus rounded-sm"
          aria-label={mobileMenuOpen ? 'Close navigation' : 'Open navigation'}
          aria-expanded={mobileMenuOpen}
        >
          {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
        </button>
      </div>

      {/* Nav List */}
      <nav
        aria-label="Staff navigation rail"
        className={`${
          mobileMenuOpen ? 'block' : 'hidden'
        } lg:block flex-1 flex flex-col gap-1 py-2 ${className}`}
      >
        {accessibleItems.map(item => {
          const Icon = ICON_MAP[item.id] || LayoutDashboard;
          const isActive = location.pathname.startsWith(item.path);

          return (
            <NavLink
              key={item.id}
              to={item.path}
              aria-current={isActive ? 'page' : undefined}
              onClick={() => setMobileMenuOpen(false)}
              className={({ isActive: linkActive }) => `
                flex items-center gap-3 px-3 py-2.5 rounded-sm font-ui text-sm font-medium
                transition-none outline-none focus:ring-2 focus:ring-focus
                ${
                  linkActive
                    ? 'bg-surface-raised text-primary font-semibold border-l-2 border-action-primary shadow-flat'
                    : 'text-secondary hover:text-primary hover:bg-surface-raised/50'
                }
              `}
            >
              <Icon className="w-5 h-5 shrink-0" />
              {/* Text label hidden between 1024px and 1280px (icon-only mode per DESIGN.md §11) */}
              <span className="truncate xl:inline lg:hidden inline">
                {item.label}
              </span>
            </NavLink>
          );
        })}

        {accessibleItems.length === 0 && (
          <div className="p-3 font-mono text-xs text-secondary border border-dashed border-border rounded-sm">
            No console workspaces permitted for role: {role}
          </div>
        )}
      </nav>
    </>
  );
};
