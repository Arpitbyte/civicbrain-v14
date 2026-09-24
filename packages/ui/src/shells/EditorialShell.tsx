import React from 'react';

export interface EditorialShellProps {
  children: React.ReactNode;
  topNavSlot?: React.ReactNode;
  footerSlot?: React.ReactNode;
  className?: string;
}

/**
 * EditorialShell
 * Layout: Top nav + content-width-narrow (720px) column.
 * Workspace: Transparency Board / Jan Sunwai (editorial stamped-ledger, Seal-green motifs).
 * Accessibility: Skip-to-content link, landmarks (header, nav, main, footer).
 */
export const EditorialShell: React.FC<EditorialShellProps> = ({
  children,
  topNavSlot,
  footerSlot,
  className = '',
}) => {
  return (
    <div
      data-workspace="transparency-board"
      className={`min-h-screen flex flex-col bg-background text-primary font-ui antialiased ${className}`}
    >
      {/* Skip to Content Link */}
      <a
        href="#main-content"
        className="sr-only focus:not-sr-only focus:fixed focus:top-4 focus:left-4 focus:z-50 focus:px-4 focus:py-2 focus:bg-surface focus:text-primary focus:border focus:border-border focus:shadow-lifted focus:outline-none focus:ring-2 focus:ring-focus font-ui text-sm font-medium"
      >
        Skip to main content
      </a>

      {/* Top Navigation Header */}
      <header
        role="banner"
        className="w-full border-b border-border bg-surface sticky top-0 z-20"
      >
        <div className="max-w-[720px] mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <span className="font-display font-semibold text-lg text-primary tracking-tight">
              Jan Sunwai
            </span>
            <span className="font-mono text-xs text-secondary px-1.5 py-0.5 border border-border rounded-sm">
              Public Ledger
            </span>
          </div>

          <nav aria-label="Public navigation">
            {topNavSlot || (
              <div className="text-xs text-secondary font-mono">
                Top Nav Slot
              </div>
            )}
          </nav>
        </div>
      </header>

      {/* Main Content Column (720px narrow column) */}
      <main
        id="main-content"
        role="main"
        className="flex-1 max-w-[720px] mx-auto w-full px-4 py-8"
      >
        {children}
      </main>

      {/* Footer */}
      {footerSlot && (
        <footer className="w-full border-t border-border bg-surface py-6">
          <div className="max-w-[720px] mx-auto px-4">
            {footerSlot}
          </div>
        </footer>
      )}
    </div>
  );
};
