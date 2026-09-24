import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from './AuthContext';
import { StaffRole, ROLE_DEFAULT_ROUTES } from './roles';

export interface RoleGateProps {
  allowedRoles: StaffRole[];
  children: React.ReactNode;
}

/**
 * RoleGate
 * Centralized role-based access control wrapper per Prompt 2 requirements.
 * Any attempt to access an unauthorized route redirects to the role's default workspace.
 * Never renders a dead-end 403 error page.
 */
export const RoleGate: React.FC<RoleGateProps> = ({ allowedRoles, children }) => {
  const { role, isLoading } = useAuth();
  const location = useLocation();

  if (isLoading) {
    return (
      <div className="p-8 font-mono text-xs text-secondary animate-pulse">
        Authenticating role permissions...
      </div>
    );
  }

  if (!allowedRoles.includes(role)) {
    const fallbackRoute = ROLE_DEFAULT_ROUTES[role] || '/deck';
    // Prevent infinite redirect loops if fallback route itself is restricted
    if (location.pathname === fallbackRoute) {
      return (
        <div className="p-8 text-secondary font-mono text-sm">
          Access restricted for role: {role}
        </div>
      );
    }
    return <Navigate to={fallbackRoute} replace />;
  }

  return <>{children}</>;
};
