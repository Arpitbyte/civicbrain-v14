import React from 'react';
import * as RadioGroupPrimitive from '@radix-ui/react-radio-group';

export interface RadioOption {
  value: string;
  label: React.ReactNode;
  description?: React.ReactNode;
  disabled?: boolean;
}

export interface RadioGroupProps {
  value?: string;
  defaultValue?: string;
  onValueChange?: (value: string) => void;
  options: RadioOption[];
  disabled?: boolean;
  name?: string;
  className?: string;
  orientation?: 'horizontal' | 'vertical';
  'aria-label'?: string;
}

/**
 * Radio / RadioGroup
 * Built on Radix UI RadioGroup.
 * Note: Radio circle uses rounded-full strictly as the standard form indicator,
 * or standard circular radio. Per DESIGN.md §3.3 radio dots are classic form controls.
 */
export const RadioGroup: React.FC<RadioGroupProps> = ({
  value,
  defaultValue,
  onValueChange,
  options,
  disabled = false,
  name,
  className = '',
  orientation = 'vertical',
  'aria-label': ariaLabel,
}) => {
  return (
    <RadioGroupPrimitive.Root
      value={value}
      defaultValue={defaultValue}
      onValueChange={onValueChange}
      disabled={disabled}
      name={name}
      aria-label={ariaLabel}
      className={`flex ${orientation === 'horizontal' ? 'flex-row gap-6' : 'flex-col gap-3'} ${className}`}
    >
      {options.map((option) => (
        <div
          key={option.value}
          className={`flex items-start gap-2.5 ${option.disabled || disabled ? 'opacity-disabled' : ''}`}
        >
          <RadioGroupPrimitive.Item
            value={option.value}
            id={`radio-${option.value}`}
            disabled={option.disabled || disabled}
            className="
              flex items-center justify-center w-4 h-4 mt-0.5 rounded-full border border-border bg-surface
              outline-none cursor-pointer transition-colors duration-fast ease-standard
              focus-visible:ring-2 focus-visible:ring-focus focus-visible:ring-offset-2 focus-visible:ring-offset-background
              data-[state=checked]:border-action-primary
              disabled:cursor-not-allowed
            "
          >
            <RadioGroupPrimitive.Indicator className="flex items-center justify-center">
              <span className="w-2 h-2 rounded-full bg-action-primary" />
            </RadioGroupPrimitive.Indicator>
          </RadioGroupPrimitive.Item>

          <div className="flex flex-col select-none">
            <label
              htmlFor={`radio-${option.value}`}
              className="text-sm font-ui font-medium text-primary cursor-pointer disabled:cursor-not-allowed"
            >
              {option.label}
            </label>
            {option.description && (
              <span className="text-xs font-ui text-text-secondary">
                {option.description}
              </span>
            )}
          </div>
        </div>
      ))}
    </RadioGroupPrimitive.Root>
  );
};
