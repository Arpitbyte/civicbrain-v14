import React from 'react';

export type ButtonVariant = 'primary' | 'secondary' | 'destructive' | 'ghost';
export type ButtonSize = 'sm' | 'md' | 'lg';

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  size?: ButtonSize;
  isLoading?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
}

/**
 * Button
 * Conforms to DESIGN.md §8:
 * - radius-md (8px)
 * - heights: sm (32px), md (40px), lg (48px)
 * - primary: filled action-primary
 * - secondary: 1px border-border, transparent fill
 * - destructive: status-danger
 * - motion: active:scale-[0.98] duration-fast
 * - focus: 2px focus ring offset 2px
 */
export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      variant = 'primary',
      size = 'md',
      isLoading = false,
      leftIcon,
      rightIcon,
      children,
      className = '',
      disabled,
      ...props
    },
    ref
  ) => {
    const sizeClasses = {
      sm: 'h-8 px-3 text-xs gap-1.5',
      md: 'h-10 px-4 text-sm gap-2',
      lg: 'h-12 px-6 text-base gap-2.5',
    }[size];

    const variantClasses = {
      primary:
        'bg-action-primary text-text-inverse hover:brightness-105 active:scale-[0.98] border border-transparent shadow-flat',
      secondary:
        'bg-transparent text-primary border border-border hover:bg-surface-raised active:scale-[0.98]',
      destructive:
        'bg-status-danger text-text-inverse hover:brightness-105 active:scale-[0.98] border border-transparent',
      ghost:
        'bg-transparent text-primary hover:bg-surface-raised active:scale-[0.98] border border-transparent',
    }[variant];

    return (
      <button
        ref={ref}
        disabled={disabled || isLoading}
        className={`
          inline-flex items-center justify-center font-ui font-medium rounded-md
          outline-none focus-visible:ring-2 focus-visible:ring-focus focus-visible:ring-offset-2 focus-visible:ring-offset-background
          transition-transform duration-fast ease-standard cursor-pointer
          disabled:opacity-disabled disabled:cursor-not-allowed disabled:pointer-events-none
          ${sizeClasses}
          ${variantClasses}
          ${className}
        `}
        {...props}
      >
        {isLoading ? (
          <span className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin" />
        ) : (
          leftIcon
        )}
        <span>{children}</span>
        {!isLoading && rightIcon}
      </button>
    );
  }
);

Button.displayName = 'Button';

export interface IconButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  'aria-label': string;
  variant?: ButtonVariant;
  size?: ButtonSize;
  icon: React.ReactNode;
}

/**
 * IconButton
 * Requires aria-label for accessibility.
 */
export const IconButton = React.forwardRef<HTMLButtonElement, IconButtonProps>(
  (
    {
      'aria-label': ariaLabel,
      variant = 'secondary',
      size = 'md',
      icon,
      className = '',
      disabled,
      ...props
    },
    ref
  ) => {
    const sizeClasses = {
      sm: 'h-8 w-8 text-xs',
      md: 'h-10 w-10 text-sm',
      lg: 'h-12 w-12 text-base',
    }[size];

    const variantClasses = {
      primary:
        'bg-action-primary text-text-inverse hover:brightness-105 active:scale-[0.98] border border-transparent shadow-flat',
      secondary:
        'bg-transparent text-primary border border-border hover:bg-surface-raised active:scale-[0.98]',
      destructive:
        'bg-status-danger text-text-inverse hover:brightness-105 active:scale-[0.98] border border-transparent',
      ghost:
        'bg-transparent text-primary hover:bg-surface-raised active:scale-[0.98] border border-transparent',
    }[variant];

    return (
      <button
        ref={ref}
        aria-label={ariaLabel}
        disabled={disabled}
        className={`
          inline-flex items-center justify-center font-ui rounded-md
          outline-none focus-visible:ring-2 focus-visible:ring-focus focus-visible:ring-offset-2 focus-visible:ring-offset-background
          transition-transform duration-fast ease-standard cursor-pointer
          disabled:opacity-disabled disabled:cursor-not-allowed disabled:pointer-events-none
          ${sizeClasses}
          ${variantClasses}
          ${className}
        `}
        {...props}
      >
        {icon}
      </button>
    );
  }
);

IconButton.displayName = 'IconButton';
