import React from 'react';

export type StaffWorkspace = 'command-deck' | 'ops-board' | 'city-pulse' | 'control-room';

export interface StaffConsoleShellProps {
  workspace?: StaffWorkspace;
  children: React.ReactNode;
  navSlot?: React.ReactNode;
  headerSlot?: React.ReactNode;
  userSlot?: React.ReactNode;
  className?: string;
}

/**
 * StaffConsoleShell
 * Layout: 280px persistent left rail + fluid main, min-width 1280px on desktop.
 * Responsive: Collapsible rail on tablet, top sheet/nav on mobile per DESIGN.md §11.
 * Accessibility: Skip-to-content link, landmarks (aside, nav, header, main).
 */
export const StaffConsoleShell: React.FC<StaffConsoleShellProps> = ({
  workspace = 'command-deck',
  children,
  navSlot,
  headerSlot,
  userSlot,
  className = '',
}) => {
  return (
    <div
      data-workspace={workspace}
      className={`min-h-screen flex flex-col lg:flex-row bg-background text-primary font-ui antialiased ${className}`}
    >
      {/* Skip to Content Link */}
      <a
        href="#main-content"
        className="sr-only focus:not-sr-only focus:fixed focus:top-4 focus:left-4 focus:z-50 focus:px-4 focus:py-2 focus:bg-surface focus:text-primary focus:border focus:border-border focus:shadow-lifted focus:outline-none focus:ring-2 focus:ring-focus font-ui text-sm font-medium"
      >
        Skip to main content
      </a>

      {/* 280px Left Rail Landmark */}
      <aside
        role="complementary"
        aria-label="Staff navigation rail"
        className="w-full lg:w-[280px] shrink-0 border-b lg:border-b-0 lg:border-r border-border bg-surface flex flex-col justify-between"
      >
        <div className="flex flex-col flex-1">
          {/* Brand & Workspace Indicator */}
          <div className="h-14 border-b border-border px-5 flex items-center justify-between">
            <span className="font-ui font-semibold text-base tracking-normal text-primary">
              CivicBrain
            </span>
            <span className="font-mono text-xs text-secondary capitalize">
              {workspace.replace('-', ' ')}
            </span>
          </div>

          {/* Navigation Slot */}
          <nav aria-label="Console navigation" className="flex-1 p-3">
            {navSlot || (
              <div className="p-3 text-secondary text-sm border border-dashed border-border rounded-sm">
                Nav Slot Placeholder
              </div>
            )}
          </nav>
        </div>

        {/* User Slot / Footer inside Rail */}
        {userSlot && (
          <div className="p-4 border-t border-border">
            {userSlot}
          </div>
        )}
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0 xl:min-w-[1280px]">
        {/* Header Bar */}
        {headerSlot && (
          <header
            role="banner"
            className="h-14 border-b border-border bg-surface px-6 flex items-center justify-between"
          >
            {headerSlot}
          </header>
        )}

        {/* Main Landmark */}
        <main
          id="main-content"
          role="main"
          className="flex-1 p-6 overflow-y-auto"
        >
          {children}
        </main>
      </div>
    </div>
  );
};
