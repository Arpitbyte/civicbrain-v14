import React from 'react';
import { AlertTriangle, RefreshCw } from 'lucide-react';

export interface ErrorStateProps {
  /**
   * Required, plain-language error message explaining what happened.
   * Per DESIGN.md §8:
   * "Plain language + the actual next step, never a raw API error string surfaced to citizens"
   */
  message: string;
  /**
   * Required next step instructions for the user.
   */
  nextStep: string;
  title?: string;
  onRetry?: () => void;
  retryLabel?: string;
  className?: string;
}

/**
 * ErrorState
 * Conforms to DESIGN.md §8 & PROMPT 3:
 * - Requires explicit message and nextStep props (no raw unhandled exceptions)
 * - Clear recovery affordance
 */
export const ErrorState: React.FC<ErrorStateProps> = ({
  message,
  nextStep,
  title = 'Something went wrong',
  onRetry,
  retryLabel = 'Try again',
  className = '',
}) => {
  return (
    <div
      role="alert"
      className={`
        flex flex-col items-center justify-center text-center p-8 sm:p-12
        border border-status-danger/30 rounded-md bg-status-danger/5
        ${className}
      `}
    >
      <div className="p-3 mb-3 rounded-md bg-surface-raised border border-status-danger/30 text-status-danger">
        <AlertTriangle className="w-8 h-8 stroke-[1.5]" />
      </div>

      <h3 className="text-base font-ui font-semibold text-primary mb-1">
        {title}
      </h3>

      <p className="text-sm font-ui text-primary max-w-sm mb-1 font-medium">
        {message}
      </p>

      <p className="text-xs font-ui text-text-secondary max-w-sm mb-4">
        {nextStep}
      </p>

      {onRetry && (
        <button
          type="button"
          onClick={onRetry}
          className="
            inline-flex items-center justify-center gap-2 h-9 px-4 text-xs font-ui font-medium rounded-md
            bg-surface text-primary border border-border hover:bg-surface-raised active:scale-[0.98]
            transition-transform duration-fast ease-standard cursor-pointer outline-none
            focus-visible:ring-2 focus-visible:ring-focus focus-visible:ring-offset-2
          "
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>{retryLabel}</span>
        </button>
      )}
    </div>
  );
};
