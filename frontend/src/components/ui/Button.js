import React from 'react';
import { cn } from '../../utils/cn';

const Button = React.forwardRef(({
  children,
  variant = 'primary',
  size = 'md',
  disabled = false,
  loading = false,
  icon,
  iconPosition = 'left',
  className,
  ...props
}, ref) => {
  // const { theme } = useTheme(); // Removido para evitar warning

  const baseStyles = `
    inline-flex items-center justify-center
    font-medium rounded-lg
    transition-all duration-200
    focus:outline-none focus:ring-2 focus:ring-offset-2
    disabled:opacity-50 disabled:cursor-not-allowed
    active:scale-95
  `;

  const variants = {
    primary: `
      bg-blue-600 hover:bg-blue-700
      text-white
      focus:ring-blue-500
      shadow-sm hover:shadow-md
    `,
    secondary: `
      bg-gray-100 hover:bg-gray-200
      text-gray-900
      focus:ring-gray-500
      dark:bg-gray-800 dark:hover:bg-gray-700
      dark:text-gray-100
    `,
    outline: `
      border border-gray-300
      bg-transparent hover:bg-gray-50
      text-gray-700 hover:text-gray-900
      focus:ring-gray-500
      dark:border-gray-600 dark:hover:bg-gray-800
      dark:text-gray-300 dark:hover:text-gray-100
    `,
    ghost: `
      bg-transparent hover:bg-gray-100
      text-gray-700 hover:text-gray-900
      focus:ring-gray-500
      dark:hover:bg-gray-800
      dark:text-gray-300 dark:hover:text-gray-100
    `,
    danger: `
      bg-red-600 hover:bg-red-700
      text-white
      focus:ring-red-500
      shadow-sm hover:shadow-md
    `,
    success: `
      bg-green-600 hover:bg-green-700
      text-white
      focus:ring-green-500
      shadow-sm hover:shadow-md
    `,
  };

  const sizes = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-sm',
    lg: 'px-6 py-3 text-base',
    xl: 'px-8 py-4 text-lg',
  };

  const iconSizes = {
    sm: 'w-4 h-4',
    md: 'w-4 h-4',
    lg: 'w-5 h-5',
    xl: 'w-6 h-6',
  };

  return (
    <button
      ref={ref}
      className={cn(
        baseStyles,
        variants[variant],
        sizes[size],
        className
      )}
      disabled={disabled || loading}
      {...props}
    >
      {loading && (
        <svg
          className={cn('animate-spin -ml-1 mr-2', iconSizes[size])}
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
        >
          <circle
            className="opacity-25"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            strokeWidth="4"
          />
          <path
            className="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
          />
        </svg>
      )}
      
      {!loading && icon && iconPosition === 'left' && (
        <span className={cn('mr-2', iconSizes[size])}>
          {icon}
        </span>
      )}
      
      {children}
      
      {!loading && icon && iconPosition === 'right' && (
        <span className={cn('ml-2', iconSizes[size])}>
          {icon}
        </span>
      )}
    </button>
  );
});

Button.displayName = 'Button';

export default Button;