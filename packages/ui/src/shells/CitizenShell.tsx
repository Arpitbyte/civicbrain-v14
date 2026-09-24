import React from 'react';

export interface CitizenShellProps {
  children: React.ReactNode;
  bottomNavSlot?: React.ReactNode;
  headerSlot?: React.ReactNode;
  className?: string;
}

/**
 * CitizenShell
 * Layout: Bottom tab bar + content-width-narrow (720px) column, mobile-first.
 * Workspace: Nagrik Setu (warm daylight Field paper, low density).
 * Accessibility: Skip-to-content link, landmarks (header, main, nav).
 */
export const CitizenShell: React.FC<CitizenShellProps> = ({
  children,
  bottomNavSlot,
  headerSlot,
  className = '',
}) => {
  return (
    <div
      data-workspace="nagrik-setu"
      className={`min-h-screen flex flex-col bg-background text-primary font-ui antialiased ${className}`}
    >
      {/* Skip to Content Link */}
      <a
        href="#main-content"
        className="sr-only focus:not-sr-only focus:fixed focus:top-4 focus:left-4 focus:z-50 focus:px-4 focus:py-2 focus:bg-surface focus:text-primary focus:border focus:border-border focus:shadow-lifted focus:outline-none focus:ring-2 focus:ring-focus font-ui text-sm font-medium"
      >
        Skip to main content
      </a>

      {/* Top Header Bar */}
      <header
        role="banner"
        className="w-full border-b border-border bg-surface sticky top-0 z-20"
      >
        <div className="max-w-[720px] mx-auto px-4 h-14 flex items-center justify-between">
          <span className="font-ui font-semibold text-base text-primary">
            नागरिक सेतु <span className="text-secondary font-normal text-xs ml-1 font-mono">Nagrik Setu</span>
          </span>
          {headerSlot && <div>{headerSlot}</div>}
        </div>
      </header>

      {/* Main Content Column (720px narrow column) */}
      <main
        id="main-content"
        role="main"
        className="flex-1 max-w-[720px] mx-auto w-full px-4 pt-6 pb-24"
      >
        {children}
      </main>

      {/* Bottom Tab Bar (Mobile-first persistent bottom navigation) */}
      <nav
        aria-label="Citizen bottom navigation"
        className="fixed bottom-0 left-0 right-0 z-30 border-t border-border bg-surface shadow-lifted"
      >
        <div className="max-w-[720px] mx-auto px-4 h-16 flex items-center justify-around">
          {bottomNavSlot || (
            <div className="text-xs text-secondary font-mono">
              Bottom Nav Slot Placeholder
            </div>
          )}
        </div>
      </nav>
    </div>
  );
};
