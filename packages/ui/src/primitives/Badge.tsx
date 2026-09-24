import React from 'react';

export type BadgeVariant =
  | 'default'
  | 'neutral'
  | 'success'
  | 'warning'
  | 'danger'
  | 'info'
  | 'priority-1'
  | 'priority-2'
  | 'priority-3'
  | 'priority-4';

export type BadgeSize = 'sm' | 'md';

export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: BadgeVariant;
  size?: BadgeSize;
  icon?: React.ReactNode;
  children: React.ReactNode;
  interactive?: boolean;
  onRemove?: () => void;
}

/**
 * Badge & Chip
 * Conforms to DESIGN.md §3.3 & §8:
 * - "radius-full (999px) - status chips ONLY — the one pill exception"
 * - "Text + icon + color always together, never color chip alone (§12)"
 * - single-hue Marker scale for priorities
 */
export const Badge: React.FC<BadgeProps> = ({
  variant = 'default',
  size = 'md',
  icon,
  children,
  className = '',
  interactive = false,
  onRemove,
  ...props
}) => {
  const sizeClasses = {
    sm: 'text-[11px] py-0.5 px-2 gap-1',
    md: 'text-xs py-1 px-2.5 gap-1.5',
  }[size];

  const variantClasses = {
    default: 'bg-surface-raised text-primary border border-border',
    neutral: 'bg-field-200 text-station-800 border border-field-300',
    success: 'bg-status-success/15 text-status-success border border-status-success/30',
    warning: 'bg-status-warning/15 text-station-900 border border-status-warning/40',
    danger: 'bg-status-danger/15 text-status-danger border border-status-danger/30',
    info: 'bg-status-info/15 text-status-info border border-status-info/30',
    'priority-1': 'bg-priority-1/20 text-station-800 border border-priority-1',
    'priority-2': 'bg-priority-2/20 text-station-900 border border-priority-2',
    'priority-3': 'bg-priority-3/20 text-station-900 border border-priority-3',
    'priority-4': 'bg-priority-4/20 text-text-inverse bg-priority-4 border border-priority-4',
  }[variant];

  return (
    <span
      className={`
        inline-flex items-center justify-center font-ui font-medium rounded-full select-none
        transition-colors duration-fast ease-standard
        ${sizeClasses}
        ${variantClasses}
        ${interactive ? 'cursor-pointer hover:brightness-95 active:scale-95' : ''}
        ${className}
      `}
      {...props}
    >
      {icon && <span className="flex-shrink-0 flex items-center">{icon}</span>}
      <span>{children}</span>
      {onRemove && (
        <button
          type="button"
          onClick={(e) => {
            e.stopPropagation();
            onRemove();
          }}
          className="ml-0.5 -mr-1 p-0.5 rounded-full hover:bg-black/10 dark:hover:bg-white/10 outline-none focus-visible:ring-1 focus-visible:ring-focus cursor-pointer"
          aria-label="Remove"
        >
          <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      )}
    </span>
  );
};

export const Chip = Badge;
