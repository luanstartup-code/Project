import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useTheme } from '../../contexts/ThemeContext';
import { 
  Home, 
  Video, 
  BarChart3, 
  Settings, 
  Plus,
  Clock,
  CheckCircle,
  AlertCircle,
  MessageSquare,
  Film,
  User
} from 'lucide-react';
import { cn } from '../../utils/cn';

const Sidebar = () => {
  const { theme, isDark } = useTheme();
  const location = useLocation();

  const navigation = [
    { name: 'Chat', href: '/chat', icon: MessageSquare },
    { name: 'Dashboard', href: '/dashboard', icon: Home },
    { name: 'Videos', href: '/videos', icon: Video },
    { name: 'Video Studio', href: '/video-studio', icon: Film },
    { name: 'Avatar Studio', href: '/avatar-studio', icon: User },
    { name: 'Analytics', href: '/analytics', icon: BarChart3 },
    { name: 'Settings', href: '/settings', icon: Settings },
  ];

  const quickActions = [
    { name: 'Create Video', href: '/videos/create', icon: Plus },
    { name: 'Recent Videos', href: '/videos?filter=recent', icon: Clock },
    { name: 'Completed', href: '/videos?filter=completed', icon: CheckCircle },
    { name: 'Failed', href: '/videos?filter=failed', icon: AlertCircle },
  ];

  const isActive = (path) => location.pathname === path;

  return (
    <div
      className={cn(
        'fixed left-0 top-16 h-full w-64 border-r transition-colors duration-200',
        isDark ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'
      )}
      style={{
        backgroundColor: theme.surface.primary,
        borderColor: theme.border.primary,
      }}
    >
      <div className="flex flex-col h-full">
        {/* Main Navigation */}
        <nav className="flex-1 px-4 py-6 space-y-2">
          <div className="mb-6">
            <h3 className={cn(
              'text-xs font-semibold uppercase tracking-wider',
              isDark ? 'text-gray-400' : 'text-gray-500'
            )}
            style={{
              color: theme.text.tertiary,
            }}
            >
              Navigation
            </h3>
          </div>
          
          {navigation.map((item) => {
            const Icon = item.icon;
            return (
              <Link
                key={item.name}
                to={item.href}
                className={cn(
                  'group flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors duration-200',
                  isActive(item.href)
                    ? isDark 
                      ? 'text-white bg-gray-700' 
                      : 'text-gray-900 bg-gray-100'
                    : isDark 
                      ? 'text-gray-300 hover:text-white hover:bg-gray-700' 
                      : 'text-gray-700 hover:text-gray-900 hover:bg-gray-100'
                )}
                style={{
                  color: isActive(item.href) 
                    ? theme.text.primary 
                    : theme.text.secondary,
                }}
              >
                <Icon className={cn(
                  'mr-3 h-5 w-5',
                  isActive(item.href)
                    ? isDark ? 'text-white' : 'text-gray-900'
                    : isDark ? 'text-gray-400 group-hover:text-gray-300' : 'text-gray-400 group-hover:text-gray-500'
                )} />
                {item.name}
              </Link>
            );
          })}
        </nav>

        {/* Quick Actions */}
        <div className="px-4 py-6 border-t"
          style={{
            borderColor: theme.border.primary,
          }}
        >
          <div className="mb-4">
            <h3 className={cn(
              'text-xs font-semibold uppercase tracking-wider',
              isDark ? 'text-gray-400' : 'text-gray-500'
            )}
            style={{
              color: theme.text.tertiary,
            }}
            >
              Quick Actions
            </h3>
          </div>
          
          {quickActions.map((item) => {
            const Icon = item.icon;
            return (
              <Link
                key={item.name}
                to={item.href}
                className={cn(
                  'group flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors duration-200',
                  isActive(item.href)
                    ? isDark 
                      ? 'text-white bg-gray-700' 
                      : 'text-gray-900 bg-gray-100'
                    : isDark 
                      ? 'text-gray-300 hover:text-white hover:bg-gray-700' 
                      : 'text-gray-700 hover:text-gray-900 hover:bg-gray-100'
                )}
                style={{
                  color: isActive(item.href) 
                    ? theme.text.primary 
                    : theme.text.secondary,
                }}
              >
                <Icon className={cn(
                  'mr-3 h-5 w-5',
                  isActive(item.href)
                    ? isDark ? 'text-white' : 'text-gray-900'
                    : isDark ? 'text-gray-400 group-hover:text-gray-300' : 'text-gray-400 group-hover:text-gray-500'
                )} />
                {item.name}
              </Link>
            );
          })}
        </div>

        {/* Stats */}
        <div className="px-4 py-6 border-t"
          style={{
            borderColor: theme.border.primary,
          }}
        >
          <div className="mb-4">
            <h3 className={cn(
              'text-xs font-semibold uppercase tracking-wider',
              isDark ? 'text-gray-400' : 'text-gray-500'
            )}
            style={{
              color: theme.text.tertiary,
            }}
            >
              Stats
            </h3>
          </div>
          
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span className={cn(
                'text-sm',
                isDark ? 'text-gray-400' : 'text-gray-600'
              )}
              style={{
                color: theme.text.tertiary,
              }}
              >
                Total Videos
              </span>
              <span className={cn(
                'text-sm font-semibold',
                isDark ? 'text-white' : 'text-gray-900'
              )}
              style={{
                color: theme.text.primary,
              }}
              >
                1,234
              </span>
            </div>
            
            <div className="flex justify-between items-center">
              <span className={cn(
                'text-sm',
                isDark ? 'text-gray-400' : 'text-gray-600'
              )}
              style={{
                color: theme.text.tertiary,
              }}
              >
                Processing
              </span>
              <span className={cn(
                'text-sm font-semibold',
                isDark ? 'text-yellow-400' : 'text-yellow-600'
              )}
              >
                5
              </span>
            </div>
            
            <div className="flex justify-between items-center">
              <span className={cn(
                'text-sm',
                isDark ? 'text-gray-400' : 'text-gray-600'
              )}
              style={{
                color: theme.text.tertiary,
              }}
              >
                Completed
              </span>
              <span className={cn(
                'text-sm font-semibold',
                isDark ? 'text-green-400' : 'text-green-600'
              )}
              >
                1,229
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;