import React from 'react';
import { useTheme } from '../../contexts/ThemeContext';
import { cn } from '../../utils/cn';

const ProgressBar = ({
  progress = 0,
  total = 100,
  showPercentage = true,
  showLabel = true,
  label = '',
  size = 'md',
  variant = 'primary',
  className = '',
  animated = true
}) => {
  const { theme, isDark } = useTheme();
  
  const percentage = Math.min(Math.max((progress / total) * 100, 0), 100);
  
  const sizeClasses = {
    sm: 'h-1',
    md: 'h-2',
    lg: 'h-3',
    xl: 'h-4'
  };
  
  const variantClasses = {
    primary: isDark ? 'bg-blue-600' : 'bg-blue-500',
    secondary: isDark ? 'bg-gray-600' : 'bg-gray-500',
    success: isDark ? 'bg-green-600' : 'bg-green-500',
    warning: isDark ? 'bg-yellow-600' : 'bg-yellow-500',
    danger: isDark ? 'bg-red-600' : 'bg-red-500',
    info: isDark ? 'bg-cyan-600' : 'bg-cyan-500'
  };
  
  const bgClasses = {
    primary: isDark ? 'bg-blue-900/30' : 'bg-blue-100',
    secondary: isDark ? 'bg-gray-700' : 'bg-gray-200',
    success: isDark ? 'bg-green-900/30' : 'bg-green-100',
    warning: isDark ? 'bg-yellow-900/30' : 'bg-yellow-100',
    danger: isDark ? 'bg-red-900/30' : 'bg-red-100',
    info: isDark ? 'bg-cyan-900/30' : 'bg-cyan-100'
  };

  return (
    <div className={cn("space-y-2", className)}>
      {/* Label and Percentage */}
      {(showLabel || showPercentage) && (
        <div className="flex justify-between items-center">
          {showLabel && (
            <span className="text-sm font-medium"
              style={{
                color: theme.text.primary,
              }}
            >
              {label || 'Progresso'}
            </span>
          )}
          {showPercentage && (
            <span className="text-sm"
              style={{
                color: theme.text.secondary,
              }}
            >
              {Math.round(percentage)}%
            </span>
          )}
        </div>
      )}
      
      {/* Progress Bar */}
      <div className={cn(
        "w-full rounded-full overflow-hidden",
        sizeClasses[size],
        bgClasses[variant]
      )}
      style={{
        backgroundColor: theme.surface.secondary,
      }}
      >
        <div
          className={cn(
            "h-full rounded-full transition-all duration-300 ease-out",
            variantClasses[variant],
            animated && "animate-pulse"
          )}
          style={{
            width: `${percentage}%`,
            backgroundColor: variant === 'primary' ? theme.primary[500] : undefined,
          }}
        />
      </div>
      
      {/* Progress Details */}
      {showLabel && (
        <div className="flex justify-between text-xs"
          style={{
            color: theme.text.tertiary,
          }}
        >
          <span>{progress}</span>
          <span>{total}</span>
        </div>
      )}
    </div>
  );
};

export default ProgressBar;