import React from 'react';
import { AlertCircle } from 'lucide-react';

export interface FieldProps {
  id?: string;
  label?: React.ReactNode;
  helperText?: React.ReactNode;
  errorMessage?: React.ReactNode;
  required?: boolean;
  disabled?: boolean;
  className?: string;
  children: React.ReactNode;
}

/**
 * Field
 * Structural form field wrapper providing label, helperText, and error messaging.
 * Conforms to DESIGN.md §8:
 * - Error states are never color-only (paired with icon and message)
 * - Required indicator
 */
export const Field: React.FC<FieldProps> = ({
  id,
  label,
  helperText,
  errorMessage,
  required,
  disabled,
  className = '',
  children,
}) => {
  const isInvalid = Boolean(errorMessage);

  return (
    <div className={`flex flex-col gap-1.5 w-full ${disabled ? 'opacity-disabled' : ''} ${className}`}>
      {label && (
        <label
          htmlFor={id}
          className="text-xs font-ui font-medium text-text-secondary select-none flex items-center justify-between"
        >
          <span>
            {label}
            {required && <span className="text-status-danger ml-1" aria-hidden="true">*</span>}
          </span>
        </label>
      )}

      {children}

      {isInvalid ? (
        <div
          id={id ? `${id}-error` : undefined}
          role="alert"
          className="flex items-center gap-1.5 text-xs text-status-danger font-ui mt-0.5"
        >
          <AlertCircle className="w-3.5 h-3.5 flex-shrink-0" aria-hidden="true" />
          <span>{errorMessage}</span>
        </div>
      ) : helperText ? (
        <p
          id={id ? `${id}-helper` : undefined}
          className="text-xs text-text-secondary font-ui mt-0.5"
        >
          {helperText}
        </p>
      ) : null}
    </div>
  );
};
