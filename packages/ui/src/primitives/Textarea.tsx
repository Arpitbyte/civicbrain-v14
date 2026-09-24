import React from 'react';
import { AlertCircle } from 'lucide-react';

export interface TextareaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  isInvalid?: boolean;
}

/**
 * Textarea
 * Conforms to DESIGN.md §8:
 * - radius-sm (4px)
 * - 1px color-border
 * - focus: 2px color-focus ring offset 2px
 * - never color-only invalid state
 */
export const Textarea = React.forwardRef<HTMLTextAreaElement, TextareaProps>(
  (
    {
      isInvalid = false,
      disabled,
      className = '',
      rows = 4,
      ...props
    },
    ref
  ) => {
    return (
      <div className="relative w-full">
        <textarea
          ref={ref}
          rows={rows}
          disabled={disabled}
          aria-invalid={isInvalid ? 'true' : undefined}
          className={`
            w-full p-3 bg-surface text-primary border rounded-sm font-ui text-sm placeholder:text-text-secondary/60
            outline-none transition-colors duration-fast ease-standard resize-y
            ${
              isInvalid
                ? 'border-status-danger focus-visible:ring-2 focus-visible:ring-status-danger focus-visible:ring-offset-2 focus-visible:ring-offset-background'
                : 'border-border focus-visible:border-transparent focus-visible:ring-2 focus-visible:ring-focus focus-visible:ring-offset-2 focus-visible:ring-offset-background'
            }
            disabled:opacity-disabled disabled:cursor-not-allowed disabled:bg-surface-raised
            ${className}
          `}
          {...props}
        />
        {isInvalid && (
          <div className="absolute top-3 right-3 pointer-events-none">
            <AlertCircle className="w-4 h-4 text-status-danger" aria-hidden="true" />
          </div>
        )}
      </div>
    );
  }
);

Textarea.displayName = 'Textarea';
