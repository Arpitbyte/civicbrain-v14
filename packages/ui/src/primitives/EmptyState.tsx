import React from 'react';
import { Inbox } from 'lucide-react';

export interface EmptyStateProps {
  /**
   * Required, specific message describing what is missing.
   * Per DESIGN.md §8 & ANTIGRAVITY_PROMPTS.md PROMPT 3:
   * "Specific to what's missing ('No incidents in this ward yet' not 'No data'),
   * never a generic illustration, no default generic text allowed to ship."
   */
  message: string;
  title?: string;
  icon?: React.ReactNode;
  action?: {
    label: string;
    onClick: () => void;
  };
  className?: string;
}

/**
 * EmptyState
 * Conforms to DESIGN.md §8 & PROMPT 3 rules:
 * - Requires a specific message prop (no generic placeholder strings)
 * - Typographic / line-icon treatment, never stock illustrations
 * - Quiet motion, honest presentation
 */
export const EmptyState: React.FC<EmptyStateProps> = ({
  message,
  title,
  icon = <Inbox className="w-8 h-8 text-text-secondary stroke-[1.5]" />,
  action,
  className = '',
}) => {
  return (
    <div
      className={`
        flex flex-col items-center justify-center text-center p-8 sm:p-12
        border border-dashed border-border rounded-md bg-surface/50
        ${className}
      `}
    >
      <div className="p-3 mb-3 rounded-md bg-surface-raised border border-border text-text-secondary">
        {icon}
      </div>

      {title && (
        <h3 className="text-base font-ui font-semibold text-primary mb-1">
          {title}
        </h3>
      )}

      <p className="text-sm font-ui text-text-secondary max-w-sm mb-4">
        {message}
      </p>

      {action && (
        <button
          type="button"
          onClick={action.onClick}
          className="
            inline-flex items-center justify-center h-9 px-4 text-xs font-ui font-medium rounded-md
            bg-action-primary text-text-inverse hover:brightness-105 active:scale-[0.98]
            transition-transform duration-fast ease-standard cursor-pointer outline-none
            focus-visible:ring-2 focus-visible:ring-focus focus-visible:ring-offset-2
          "
        >
          {action.label}
        </button>
      )}
    </div>
  );
};
