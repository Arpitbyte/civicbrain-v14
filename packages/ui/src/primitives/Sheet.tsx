import React from 'react';
import * as DialogPrimitive from '@radix-ui/react-dialog';
import { X } from 'lucide-react';

export interface SheetProps {
  open?: boolean;
  defaultOpen?: boolean;
  onOpenChange?: (open: boolean) => void;
  title: React.ReactNode;
  description?: React.ReactNode;
  children: React.ReactNode;
  footer?: React.ReactNode;
  className?: string;
  trigger?: React.ReactNode;
}

/**
 * Sheet
 * Bottom sheet on mobile with radius-xl top corners.
 * Conforms to DESIGN.md §8:
 * - "Bottom sheet on mobile (radius-xl top corners), replaces dialogs on Nagrik Setu/Karmi Sahayak"
 * - caller decides whether to use Dialog or Sheet based on workspace/breakpoint
 */
export const Sheet: React.FC<SheetProps> = ({
  open,
  defaultOpen,
  onOpenChange,
  title,
  description,
  children,
  footer,
  className = '',
  trigger,
}) => {
  return (
    <DialogPrimitive.Root open={open} defaultOpen={defaultOpen} onOpenChange={onOpenChange}>
      {trigger && <DialogPrimitive.Trigger asChild>{trigger}</DialogPrimitive.Trigger>}

      <DialogPrimitive.Portal>
        <DialogPrimitive.Overlay
          className="
            fixed inset-0 z-scrim bg-station-900/50 backdrop-blur-[1px]
            data-[state=open]:animate-in data-[state=closed]:animate-out
            data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0
            duration-fast ease-standard
          "
        />
        <DialogPrimitive.Content
          className={`
            fixed bottom-0 left-0 right-0 z-modal max-h-[90vh] overflow-y-auto
            w-full p-6 bg-surface text-primary rounded-t-xl border-t border-x border-border shadow-overlay
            data-[state=open]:animate-in data-[state=closed]:animate-out
            data-[state=closed]:slide-out-to-bottom data-[state=open]:slide-in-from-bottom
            duration-fast ease-standard outline-none
            ${className}
          `}
        >
          {/* Subtle drag handle aesthetic for touch ergonomics */}
          <div className="w-12 h-1 bg-border rounded-full mx-auto -mt-2 mb-4" aria-hidden="true" />

          <div className="flex items-start justify-between gap-4 mb-4">
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
              aria-label="Close sheet"
              className="p-1 text-text-secondary hover:text-primary rounded-sm outline-none focus-visible:ring-2 focus-visible:ring-focus"
            >
              <X className="w-4 h-4" />
            </DialogPrimitive.Close>
          </div>

          <div className="my-2">{children}</div>

          {footer && <div className="mt-6 flex flex-col sm:flex-row items-center justify-end gap-3">{footer}</div>}
        </DialogPrimitive.Content>
      </DialogPrimitive.Portal>
    </DialogPrimitive.Root>
  );
};
