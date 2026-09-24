import React from 'react';
import * as ToastPrimitive from '@radix-ui/react-toast';
import { X, CheckCircle2, AlertTriangle, AlertCircle, Info } from 'lucide-react';

export type ToastVariant = 'info' | 'success' | 'warning' | 'danger';

export interface ToastItem {
  id: string;
  title?: string;
  description: string;
  variant?: ToastVariant;
  duration?: number;
  action?: {
    label: string;
    onClick: () => void;
  };
}

export interface ToastContextType {
  toast: (toast: Omit<ToastItem, 'id'>) => string;
  dismiss: (id: string) => void;
}

const ToastContext = React.createContext<ToastContextType | undefined>(undefined);

export const useToast = () => {
  const context = React.useContext(ToastContext);
  if (!context) {
    throw new Error('useToast must be used within a ToastProvider');
  }
  return context;
};

/**
 * ToastProvider
 * Conforms to DESIGN.md §8:
 * - "Bottom-center on mobile, bottom-right on desktop"
 * - duration-slow (360ms) auto-dismiss for info, manual dismiss for actionable items
 * - radius-md, shadow-lifted, z-toast (50)
 */
export const ToastProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [toasts, setToasts] = React.useState<ToastItem[]>([]);

  const toast = React.useCallback((item: Omit<ToastItem, 'id'>) => {
    const id = Math.random().toString(36).substring(2, 9);
    setToasts((prev) => [...prev, { ...item, id }]);
    return id;
  }, []);

  const dismiss = React.useCallback((id: string) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  }, []);

  const icons = {
    info: <Info className="w-4 h-4 text-status-info flex-shrink-0" />,
    success: <CheckCircle2 className="w-4 h-4 text-status-success flex-shrink-0" />,
    warning: <AlertTriangle className="w-4 h-4 text-status-warning flex-shrink-0" />,
    danger: <AlertCircle className="w-4 h-4 text-status-danger flex-shrink-0" />,
  };

  return (
    <ToastContext.Provider value={{ toast, dismiss }}>
      <ToastPrimitive.Provider swipeDirection="right">
        {children}

        {toasts.map(({ id, title, description, variant = 'info', duration = 5000, action }) => (
          <ToastPrimitive.Root
            key={id}
            duration={action ? Infinity : duration}
            onOpenChange={(open) => {
              if (!open) dismiss(id);
            }}
            className="
              flex items-start gap-3 p-4 bg-surface text-primary rounded-md border border-border shadow-lifted
              data-[state=open]:animate-in data-[state=closed]:animate-out data-[swipe=end]:animate-out
              data-[state=closed]:fade-out-80 data-[state=closed]:slide-out-to-right-full
              data-[state=open]:slide-in-from-bottom-full md:data-[state=open]:slide-in-from-bottom-5
              transition-all duration-slow ease-standard
            "
          >
            {icons[variant]}

            <div className="flex flex-col flex-1 min-w-0">
              {title && (
                <ToastPrimitive.Title className="text-sm font-ui font-semibold text-primary">
                  {title}
                </ToastPrimitive.Title>
              )}
              <ToastPrimitive.Description className="text-xs font-ui text-text-secondary mt-0.5">
                {description}
              </ToastPrimitive.Description>

              {action && (
                <ToastPrimitive.Action asChild altText={action.label}>
                  <button
                    onClick={action.onClick}
                    className="self-start mt-2 px-2.5 py-1 text-xs font-ui font-medium rounded-sm border border-border bg-surface-raised hover:bg-surface text-primary cursor-pointer outline-none focus-visible:ring-2 focus-visible:ring-focus"
                  >
                    {action.label}
                  </button>
                </ToastPrimitive.Action>
              )}
            </div>

            <ToastPrimitive.Close
              aria-label="Dismiss toast"
              className="p-1 text-text-secondary hover:text-primary rounded-sm outline-none focus-visible:ring-2 focus-visible:ring-focus"
            >
              <X className="w-3.5 h-3.5" />
            </ToastPrimitive.Close>
          </ToastPrimitive.Root>
        ))}

        <ToastPrimitive.Viewport
          className="
            fixed bottom-4 left-1/2 -translate-x-1/2 md:translate-x-0 md:left-auto md:right-4
            flex flex-col gap-2 w-[calc(100vw-2rem)] md:w-96 max-w-full z-toast outline-none
          "
        />
      </ToastPrimitive.Provider>
    </ToastContext.Provider>
  );
};
