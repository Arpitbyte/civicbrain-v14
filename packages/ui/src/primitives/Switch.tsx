import React from 'react';
import * as SwitchPrimitive from '@radix-ui/react-switch';

export interface SwitchProps {
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
 * Switch
 * Built on Radix UI Switch.
 * Conforms to DESIGN.md §8:
 * - Rounded track, action-primary active state
 * - focus: 2px color-focus ring offset 2px
 */
export const Switch: React.FC<SwitchProps> = ({
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
  const switchId = id || generatedId;

  return (
    <div className={`flex items-start gap-3 ${disabled ? 'opacity-disabled' : ''} ${className}`}>
      <SwitchPrimitive.Root
        id={switchId}
        checked={checked}
        defaultChecked={defaultChecked}
        onCheckedChange={onCheckedChange}
        disabled={disabled}
        required={required}
        name={name}
        value={value}
        aria-label={ariaLabel}
        className="
          relative inline-flex h-5 w-9 shrink-0 cursor-pointer rounded-full border border-border bg-surface
          transition-colors duration-fast ease-standard outline-none
          focus-visible:ring-2 focus-visible:ring-focus focus-visible:ring-offset-2 focus-visible:ring-offset-background
          data-[state=checked]:bg-action-primary data-[state=checked]:border-action-primary
          disabled:cursor-not-allowed
        "
      >
        <SwitchPrimitive.Thumb
          className="
            pointer-events-none block h-4 w-4 rounded-full bg-surface-raised shadow-flat ring-0
            transition-transform duration-fast ease-standard
            data-[state=checked]:translate-x-4 data-[state=unchecked]:translate-x-0.5
          "
        />
      </SwitchPrimitive.Root>

      {(label || description) && (
        <div className="flex flex-col select-none">
          {label && (
            <label
              htmlFor={switchId}
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
