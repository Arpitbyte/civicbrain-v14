import React from 'react';

export interface FieldShellProps {
  children: React.ReactNode;
  syncBadgeSlot?: React.ReactNode;
  bottomActionSlot?: React.ReactNode;
  className?: string;
}

/**
 * FieldShell
 * Layout: Single column, bottom-anchored action slot, no top chrome beyond a persistent OfflineSyncBadge slot.
 * Workspace: Karmi Sahayak (high-visibility outdoor mode, >=7:1 contrast, Station-950 dark base).
 * Accessibility: Skip-to-content link, landmarks (header, main, footer).
 */
export const FieldShell: React.FC<FieldShellProps> = ({
  children,
  syncBadgeSlot,
  bottomActionSlot,
  className = '',
}) => {
  return (
    <div
      data-workspace="karmi-sahayak"
      className={`min-h-screen flex flex-col bg-background text-primary font-ui antialiased ${className}`}
    >
      {/* Skip to Content Link */}
      <a
        href="#main-content"
        className="sr-only focus:not-sr-only focus:fixed focus:top-4 focus:left-4 focus:z-50 focus:px-4 focus:py-2 focus:bg-surface focus:text-primary focus:border focus:border-border focus:shadow-lifted focus:outline-none focus:ring-2 focus:ring-focus font-ui text-sm font-medium"
      >
        Skip to main content
      </a>

      {/* Top Slot: Persistent OfflineSyncBadge slot only (no decorative top chrome) */}
      <header
        role="banner"
        className="w-full max-w-md mx-auto px-4 py-3 border-b border-border bg-surface flex items-center justify-between"
      >
        <span className="font-ui font-bold text-sm uppercase tracking-wider text-primary">
          कर्मी सहायक
        </span>
        <div>
          {syncBadgeSlot || (
            <span className="font-mono text-xs text-secondary px-2 py-0.5 border border-dashed border-border rounded-sm">
              OfflineSyncBadge Slot
            </span>
          )}
        </div>
      </header>

      {/* Main Single Column */}
      <main
        id="main-content"
        role="main"
        className="flex-1 max-w-md mx-auto w-full p-4 flex flex-col"
      >
        {children}
      </main>

      {/* Bottom-Anchored Action Slot */}
      {bottomActionSlot && (
        <footer className="sticky bottom-0 left-0 right-0 border-t border-border bg-surface p-4 shadow-lifted">
          <div className="max-w-md mx-auto w-full">
            {bottomActionSlot}
          </div>
        </footer>
      )}
    </div>
  );
};
