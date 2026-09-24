import React, { createContext, useContext, useState, useEffect } from 'react';
import { StaffRole } from './roles';

export interface UserProfile {
  id: string;
  email: string;
  role: StaffRole;
  department?: string;
  zone?: string;
  ward?: string;
}

export interface AuthContextType {
  user: UserProfile | null;
  role: StaffRole;
  isLoading: boolean;
  setRole: (role: StaffRole) => void;
  setUser: (user: UserProfile | null) => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export interface AuthProviderProps {
  children: React.ReactNode;
  initialRole?: StaffRole;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({
  children,
  initialRole = 'admin',
}) => {
  const [role, setRoleState] = useState<StaffRole>(initialRole);
  const [user, setUser] = useState<UserProfile | null>({
    id: 'usr-mock-1',
    email: 'staff@civicbrain.gov.in',
    role: initialRole,
  });
  const [isLoading, setIsLoading] = useState<boolean>(true);

  useEffect(() => {
    // Attempt to read from /v1/auth/me or hydrate session
    const fetchMe = async () => {
      try {
        const token = typeof window !== 'undefined' ? localStorage.getItem('civicbrain_token') : null;
        if (token) {
          const res = await fetch('/v1/auth/me', {
            headers: { Authorization: `Bearer ${token}` },
          });
          if (res.ok) {
            const data = await res.json();
            if (data.role) {
              setRoleState(data.role as StaffRole);
              setUser(data);
            }
          }
        }
      } catch (err) {
        // Fall back gracefully to initial role in local/development environments
      } finally {
        setIsLoading(false);
      }
    };

    fetchMe();
  }, []);

  const setRole = (newRole: StaffRole) => {
    setRoleState(newRole);
    setUser(prev => (prev ? { ...prev, role: newRole } : { id: 'usr-mock-1', email: 'staff@civicbrain.gov.in', role: newRole }));
  };

  return (
    <AuthContext.Provider value={{ user, role, isLoading, setRole, setUser }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
