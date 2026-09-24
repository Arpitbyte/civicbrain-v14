import React from 'react';
import * as DialogPrimitive from '@radix-ui/react-dialog';
import { X } from 'lucide-react';

export interface DrawerProps {
  open?: boolean;
  defaultOpen?: boolean;
  onOpenChange?: (open: boolean) => void;
  title: React.ReactNode;
  description?: React.ReactNode;
  children: React.ReactNode;
  footer?: React.ReactNode;
  width?: string;
  className?: string;
  trigger?: React.ReactNode;
}

/**
 * Drawer
 * Built on Radix UI Dialog.
 * Conforms to DESIGN.md §8:
 * - "Right-side, for 'more detail without leaving the list' (incident quick-view from Command Deck queue)"
 * - shadow-overlay, border-l, z-modal
 * - Motion: slide in from right, duration-fast ease-standard
 */
export const Drawer: React.FC<DrawerProps> = ({
  open,
  defaultOpen,
  onOpenChange,
  title,
  description,
  children,
  footer,
  width = 'w-full sm:max-w-md md:max-w-lg',
  className = '',
  trigger,
}) => {
  return (
    <DialogPrimitive.Root open={open} defaultOpen={defaultOpen} onOpenChange={onOpenChange}>
      {trigger && <DialogPrimitive.Trigger asChild>{trigger}</DialogPrimitive.Trigger>}

      <DialogPrimitive.Portal>
        <DialogPrimitive.Overlay
          className="
            fixed inset-0 z-scrim bg-station-900/40 backdrop-blur-[1px]
            data-[state=open]:animate-in data-[state=closed]:animate-out
            data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0
            duration-fast ease-standard
          "
        />
        <DialogPrimitive.Content
          className={`
            fixed top-0 right-0 bottom-0 z-modal h-full flex flex-col
            ${width} p-6 bg-surface text-primary border-l border-border shadow-overlay
            data-[state=open]:animate-in data-[state=closed]:animate-out
            data-[state=closed]:slide-out-to-right data-[state=open]:slide-in-from-right
            duration-fast ease-standard outline-none
            ${className}
          `}
        >
          <div className="flex items-start justify-between gap-4 mb-4 pb-3 border-b border-border">
            <div className="flex flex-col gap-1">
              <DialogPrimitive.Title className="text-base font-ui font-semibold text-primary">
                {title}
              </DialogPrimitive.Title>
              {description && (
                <DialogPrimitive.Description className="text-xs font-ui text-text-secondary">
                  {description}
                </DialogPrimitive.Description>
              )}
            </div>

            <DialogPrimitive.Close
              aria-label="Close drawer"
              className="p-1 text-text-secondary hover:text-primary rounded-sm outline-none focus-visible:ring-2 focus-visible:ring-focus"
            >
              <X className="w-4 h-4" />
            </DialogPrimitive.Close>
          </div>

          <div className="flex-1 overflow-y-auto my-2 pr-1">{children}</div>

          {footer && (
            <div className="mt-4 pt-3 border-t border-border flex items-center justify-end gap-3">
              {footer}
            </div>
          )}
        </DialogPrimitive.Content>
      </DialogPrimitive.Portal>
    </DialogPrimitive.Root>
  );
};
