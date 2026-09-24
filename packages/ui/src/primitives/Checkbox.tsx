import React from 'react';
import * as CheckboxPrimitive from '@radix-ui/react-checkbox';
import { Check } from 'lucide-react';

export interface CheckboxProps {
  id?: string;
  checked?: boolean;
  defaultChecked?: boolean;
  onCheckedChange?: (checked: boolean) => void;
  disabled?: boolean;
  required?: boolean;
  name?: string;
  value?: string;
  label?: React.ReactNode;
  description?: React.ReactNode;
  className?: string;
  'aria-label'?: string;
}

/**
 * Checkbox
 * Built on Radix UI Checkbox.
 * Conforms to DESIGN.md §8:
 * - radius-sm (4px)
 * - 1px color-border
 * - active fill: action-primary
 * - focus: 2px color-focus ring offset 2px
 */
export const Checkbox: React.FC<CheckboxProps> = ({
  id,
  checked,
  defaultChecked,
  onCheckedChange,
  disabled = false,
  required = false,
  name,
  value,
  label,
  description,
  className = '',
  'aria-label': ariaLabel,
}) => {
  const generatedId = React.useId();
  const checkboxId = id || generatedId;

  return (
    <div className={`flex items-start gap-2.5 ${disabled ? 'opacity-disabled' : ''} ${className}`}>
      <CheckboxPrimitive.Root
        id={checkboxId}
        checked={checked}
        defaultChecked={defaultChecked}
        onCheckedChange={onCheckedChange}
        disabled={disabled}
        required={required}
        name={name}
        value={value}
        aria-label={ariaLabel}
        className="
          flex items-center justify-center w-4 h-4 mt-0.5 rounded-sm border border-border bg-surface
          outline-none cursor-pointer transition-colors duration-fast ease-standard
          focus-visible:ring-2 focus-visible:ring-focus focus-visible:ring-offset-2 focus-visible:ring-offset-background
          data-[state=checked]:bg-action-primary data-[state=checked]:border-action-primary data-[state=checked]:text-text-inverse
          disabled:cursor-not-allowed
        "
      >
        <CheckboxPrimitive.Indicator className="flex items-center justify-center text-current">
          <Check className="w-3 h-3 stroke-[3]" />
        </CheckboxPrimitive.Indicator>
      </CheckboxPrimitive.Root>

      {(label || description) && (
        <div className="flex flex-col select-none">
          {label && (
            <label
              htmlFor={checkboxId}
              className="text-sm font-ui font-medium text-primary cursor-pointer disabled:cursor-not-allowed"
            >
              {label}
            </label>
          )}
          {description && (
            <span className="text-xs font-ui text-text-secondary">
              {description}
            </span>
          )}
        </div>
      )}
    </div>
  );
};
