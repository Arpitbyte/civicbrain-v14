import React from 'react';
import * as SelectPrimitive from '@radix-ui/react-select';
import { ChevronDown, Check } from 'lucide-react';

export interface SelectOption {
  value: string;
  label: string;
  disabled?: boolean;
}

export interface SelectProps {
  value?: string;
  defaultValue?: string;
  onValueChange?: (value: string) => void;
  options: SelectOption[];
  placeholder?: string;
  disabled?: boolean;
  isInvalid?: boolean;
  className?: string;
  name?: string;
  'aria-label'?: string;
}

/**
 * Select
 * Built on Radix UI Select.
 * Conforms to DESIGN.md §8:
 * - radius-sm (4px)
 * - 1px color-border
 * - focus: 2px color-focus ring offset 2px
 * - shadow-lifted dropdown
 */
export const Select: React.FC<SelectProps> = ({
  value,
  defaultValue,
  onValueChange,
  options,
  placeholder = 'Select an option...',
  disabled = false,
  isInvalid = false,
  className = '',
  name,
  'aria-label': ariaLabel,
}) => {
  return (
    <SelectPrimitive.Root
      value={value}
      defaultValue={defaultValue}
      onValueChange={onValueChange}
      disabled={disabled}
      name={name}
    >
      <SelectPrimitive.Trigger
        aria-label={ariaLabel}
        className={`
          flex items-center justify-between w-full h-10 px-3 bg-surface text-primary border rounded-sm font-ui text-sm
          outline-none transition-colors duration-fast ease-standard cursor-pointer
          ${
            isInvalid
              ? 'border-status-danger focus-visible:ring-2 focus-visible:ring-status-danger focus-visible:ring-offset-2'
              : 'border-border focus-visible:border-transparent focus-visible:ring-2 focus-visible:ring-focus focus-visible:ring-offset-2 focus-visible:ring-offset-background'
          }
          disabled:opacity-disabled disabled:cursor-not-allowed disabled:bg-surface-raised
          ${className}
        `}
      >
        <SelectPrimitive.Value placeholder={placeholder} />
        <SelectPrimitive.Icon asChild>
          <ChevronDown className="w-4 h-4 text-text-secondary transition-transform duration-fast" />
        </SelectPrimitive.Icon>
      </SelectPrimitive.Trigger>

      <SelectPrimitive.Portal>
        <SelectPrimitive.Content
          position="popper"
          sideOffset={4}
          className="z-dropdown min-w-[8rem] overflow-hidden bg-surface text-primary rounded-sm border border-border shadow-lifted animate-in fade-in-80"
        >
          <SelectPrimitive.Viewport className="p-1">
            {options.map((option) => (
              <SelectPrimitive.Item
                key={option.value}
                value={option.value}
                disabled={option.disabled}
                className="relative flex items-center justify-between px-3 py-2 text-sm font-ui rounded-sm select-none cursor-pointer outline-none hover:bg-surface-raised focus:bg-surface-raised data-[disabled]:opacity-disabled data-[disabled]:pointer-events-none"
              >
                <SelectPrimitive.ItemText>{option.label}</SelectPrimitive.ItemText>
                <SelectPrimitive.ItemIndicator>
                  <Check className="w-4 h-4 text-action-primary ml-2" />
                </SelectPrimitive.ItemIndicator>
              </SelectPrimitive.Item>
            ))}
          </SelectPrimitive.Viewport>
        </SelectPrimitive.Content>
      </SelectPrimitive.Portal>
    </SelectPrimitive.Root>
  );
};
