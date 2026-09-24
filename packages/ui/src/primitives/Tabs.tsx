import React from 'react';
import * as TabsPrimitive from '@radix-ui/react-tabs';

export interface TabItem {
  value: string;
  label: React.ReactNode;
  icon?: React.ReactNode;
  badge?: React.ReactNode;
  disabled?: boolean;
}

export interface TabsProps {
  value?: string;
  defaultValue?: string;
  onValueChange?: (value: string) => void;
  items: TabItem[];
  children?: React.ReactNode;
  className?: string;
  'aria-label'?: string;
}

export const TabsList = TabsPrimitive.List;
export const TabsTrigger = TabsPrimitive.Trigger;
export const TabsContent = TabsPrimitive.Content;
export const TabsRoot = TabsPrimitive.Root;

/**
 * Tabs
 * Built on Radix UI Tabs.
 * Conforms to DESIGN.md §8:
 * - "Underline-indicator style, not pill/segmented-control unless genuinely 2-option toggle"
 * - Motion Quiet tier: opacity change, instant/fast duration, no slide/bounce
 */
export const Tabs: React.FC<TabsProps> = ({
  value,
  defaultValue,
  onValueChange,
  items,
  children,
  className = '',
  'aria-label': ariaLabel,
}) => {
  return (
    <TabsPrimitive.Root
      value={value}
      defaultValue={defaultValue || items[0]?.value}
      onValueChange={onValueChange}
      className={`flex flex-col w-full ${className}`}
    >
      <TabsPrimitive.List
        aria-label={ariaLabel}
        className="flex items-center gap-6 border-b border-border w-full overflow-x-auto no-scrollbar"
      >
        {items.map((item) => (
          <TabsPrimitive.Trigger
            key={item.value}
            value={item.value}
            disabled={item.disabled}
            className="
              group relative flex items-center gap-2 py-3 px-1 text-sm font-ui font-medium text-text-secondary
              outline-none cursor-pointer select-none transition-colors duration-fast ease-standard
              hover:text-primary
              focus-visible:ring-2 focus-visible:ring-focus focus-visible:ring-offset-2 focus-visible:ring-offset-background
              data-[state=active]:text-primary
              disabled:opacity-disabled disabled:cursor-not-allowed
            "
          >
            {item.icon && <span className="w-4 h-4 flex items-center justify-center">{item.icon}</span>}
            <span>{item.label}</span>
            {item.badge && <span className="ml-1">{item.badge}</span>}
            
            {/* Underline indicator */}
            <span
              className="
                absolute bottom-0 left-0 right-0 h-0.5 bg-transparent transition-colors duration-fast
                group-data-[state=active]:bg-action-primary
              "
              aria-hidden="true"
            />
          </TabsPrimitive.Trigger>
        ))}
      </TabsPrimitive.List>

      {children}
    </TabsPrimitive.Root>
  );
};
