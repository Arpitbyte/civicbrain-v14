import React from 'react';
import { AlertCircle } from 'lucide-react';

export type InputSize = 'sm' | 'md' | 'lg';

export interface InputProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'size'> {
  size?: InputSize;
  isInvalid?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
}

/**
 * Input
 * Conforms to DESIGN.md §8:
 * - radius-sm (4px)
 * - 1px color-border
 * - focus: 2px color-focus ring offset 2px
 * - never color-only invalid state (can show AlertCircle icon when invalid)
 * - mono variant for coordinates, tokens, numeric codes
 */
export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  (
    {
      size = 'md',
      isInvalid = false,
      leftIcon,
      rightIcon,
      disabled,
      className = '',
      type = 'text',
      ...props
    },
    ref
  ) => {
    const sizeClasses = {
      sm: 'h-8 px-2.5 text-xs',
      md: 'h-10 px-3 text-sm',
      lg: 'h-12 px-4 text-base',
    }[size];

    return (
      <div className="relative flex items-center w-full">
        {leftIcon && (
          <div className="absolute left-3 flex items-center pointer-events-none text-text-secondary">
            {leftIcon}
          </div>
        )}

        <input
          ref={ref}
          type={type}
          disabled={disabled}
          aria-invalid={isInvalid ? 'true' : undefined}
          className={`
            w-full bg-surface text-primary border rounded-sm font-ui placeholder:text-text-secondary/60
            outline-none transition-colors duration-fast ease-standard
            ${
              isInvalid
                ? 'border-status-danger focus-visible:ring-2 focus-visible:ring-status-danger focus-visible:ring-offset-2 focus-visible:ring-offset-background'
                : 'border-border focus-visible:border-transparent focus-visible:ring-2 focus-visible:ring-focus focus-visible:ring-offset-2 focus-visible:ring-offset-background'
            }
            disabled:opacity-disabled disabled:cursor-not-allowed disabled:bg-surface-raised
            ${leftIcon ? 'pl-9' : ''}
            ${rightIcon || isInvalid ? 'pr-9' : ''}
            ${sizeClasses}
            ${className}
          `}
          {...props}
        />

        <div className="absolute right-3 flex items-center pointer-events-none text-text-secondary">
          {isInvalid ? (
            <AlertCircle className="w-4 h-4 text-status-danger" aria-hidden="true" />
          ) : (
            rightIcon
          )}
        </div>
      </div>
    );
  }
);

Input.displayName = 'Input';
