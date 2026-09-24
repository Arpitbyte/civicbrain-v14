import React from 'react';
import { NavLink } from 'react-router-dom';
import { Home, Search } from 'lucide-react';

export interface NavTabBarProps {
  className?: string;
}

/**
 * NavTabBar
 * Bottom tab bar for CitizenShell (Nagrik Setu).
 * Strictly contains 2 items: Home / Report and Track per Prompt 2 requirements.
 * Motion: Quiet — instant state change.
 * Accessibility: aria-current="page", keyboard navigable.
 */
export const NavTabBar: React.FC<NavTabBarProps> = ({ className = '' }) => {
  const tabs = [
    {
      to: '/',
      label: 'Home / Report',
      icon: Home,
      end: true,
    },
    {
      to: '/track',
      label: 'Track',
      icon: Search,
      end: false,
    },
  ];

  return (
    <div className={`w-full flex items-center justify-around h-full ${className}`}>
      {tabs.map(tab => {
        const Icon = tab.icon;

        return (
          <NavLink
            key={tab.to}
            to={tab.to}
            end={tab.end}
            className={({ isActive }) => `
              flex flex-col items-center justify-center gap-1 flex-1 py-1 h-full
              font-ui text-xs font-medium transition-none outline-none focus:ring-2 focus:ring-focus
              ${
                isActive
                  ? 'text-action-primary font-semibold'
                  : 'text-secondary hover:text-primary'
              }
            `}
          >
            {({ isActive }) => (
              <>
                <Icon className={`w-5 h-5 shrink-0 ${isActive ? 'stroke-[2.5]' : 'stroke-2'}`} />
                <span>{tab.label}</span>
              </>
            )}
          </NavLink>
        );
      })}
    </div>
  );
};
