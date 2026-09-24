import React from 'react';

export interface SkeletonProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'rect' | 'circle' | 'text';
  width?: string | number;
  height?: string | number;
}

/**
 * Skeleton
 * Conforms to DESIGN.md §8 & §10:
 * - Honest, content-shaped loading states
 * - Opacity pulse on surface-raised, never decorative glitter/theater
 * - radius-sm or radius-md depending on role
 */
export const Skeleton: React.FC<SkeletonProps> = ({
  variant = 'rect',
  width,
  height,
  className = '',
  style,
  ...props
}) => {
  const variantClasses = {
    rect: 'rounded-md',
    text: 'rounded-sm h-4',
    circle: 'rounded-full',
  }[variant];

  return (
    <div
      className={`
        bg-field-300/40 animate-pulse
        ${variantClasses}
        ${className}
      `}
      style={{
        width: typeof width === 'number' ? `${width}px` : width,
        height: typeof height === 'number' ? `${height}px` : height,
        ...style,
      }}
      aria-hidden="true"
      {...props}
    />
  );
};
