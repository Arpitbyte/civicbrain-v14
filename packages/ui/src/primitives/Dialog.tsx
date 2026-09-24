import React from 'react';
import * as DialogPrimitive from '@radix-ui/react-dialog';
import { X } from 'lucide-react';

export interface DialogProps {
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
 * Dialog
 * Built on Radix UI Dialog.
 * Conforms to DESIGN.md §8:
 * - "Center-modal, shadow-overlay, radius-lg (12px), used only for genuinely blocking decisions (adjudication, destructive confirm)"
 * - Scrim: z-scrim, opacity-scrim
 * - Modal: z-modal
 * - Motion: duration-fast ease-standard
 */
export const Dialog: React.FC<DialogProps> = ({
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
            fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 z-modal
            w-full max-w-lg p-6 bg-surface text-primary rounded-lg border border-border shadow-overlay
            data-[state=open]:animate-in data-[state=closed]:animate-out
            data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0
            data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95
            data-[state=closed]:slide-out-to-left-1/2 data-[state=closed]:slide-out-to-top-[48%]
            data-[state=open]:slide-in-from-left-1/2 data-[state=open]:slide-in-from-top-[48%]
            duration-fast ease-standard outline-none
            ${className}
          `}
        >
          <div className="flex items-start justify-between gap-4 mb-4">
            <div className="flex flex-col gap-1">
              <DialogPrimitive.Title className="text-lg font-ui font-semibold text-primary">
                {title}
              </DialogPrimitive.Title>
              {description && (
                <DialogPrimitive.Description className="text-xs font-ui text-text-secondary">
                  {description}
                </DialogPrimitive.Description>
              )}
            </div>

            <DialogPrimitive.Close
              aria-label="Close dialog"
              className="p-1 text-text-secondary hover:text-primary rounded-sm outline-none focus-visible:ring-2 focus-visible:ring-focus"
            >
              <X className="w-4 h-4" />
            </DialogPrimitive.Close>
          </div>

          <div className="my-2">{children}</div>

          {footer && <div className="mt-6 flex items-center justify-end gap-3">{footer}</div>}
        </DialogPrimitive.Content>
      </DialogPrimitive.Portal>
    </DialogPrimitive.Root>
  );
};
