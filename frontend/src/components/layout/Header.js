import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useTheme } from '../../contexts/ThemeContext';
import { Sun, Moon, Menu, X, Bell, User } from 'lucide-react';
import Button from '../ui/Button';
import { cn } from '../../utils/cn';

const Header = () => {
  const { theme, isDark, toggleTheme } = useTheme();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const location = useLocation();

  const navigation = [
    { name: 'Chat', href: '/chat' },
    { name: 'Dashboard', href: '/dashboard' },
    { name: 'Videos', href: '/videos' },
    { name: 'Analytics', href: '/analytics' },
  ];

  const isActive = (path) => location.pathname === path;

  return (
    <header
      className={cn(
        'sticky top-0 z-50 border-b transition-colors duration-200',
        isDark 
          ? 'bg-gray-800 border-gray-700' 
          : 'bg-white border-gray-200'
      )}
      style={{
        backgroundColor: theme.surface.primary,
        borderColor: theme.border.primary,
      }}
    >
      <div className="px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center">
            <Link to="/dashboard" className="flex-shrink-0">
              <h1 className="text-xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                AI Video Studio
              </h1>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            {navigation.map((item) => (
              <Link
                key={item.name}
                to={item.href}
                className={cn(
                  'text-sm font-medium transition-colors duration-200',
                  isActive(item.href)
                    ? isDark 
                      ? 'text-white border-b-2 border-blue-500' 
                      : 'text-gray-900 border-b-2 border-blue-500'
                    : isDark 
                      ? 'text-gray-300 hover:text-white' 
                      : 'text-gray-700 hover:text-gray-900'
                )}
                style={{
                  color: isActive(item.href) 
                    ? theme.text.primary 
                    : theme.text.secondary,
                }}
              >
                {item.name}
              </Link>
            ))}
          </nav>

          {/* Right side actions */}
          <div className="flex items-center space-x-4">
            {/* Theme toggle */}
            <Button
              variant="ghost"
              size="sm"
              onClick={toggleTheme}
              icon={isDark ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
              aria-label="Toggle theme"
            />

            {/* Notifications */}
            <Button
              variant="ghost"
              size="sm"
              icon={<Bell className="w-4 h-4" />}
              aria-label="Notifications"
            />

            {/* User menu */}
            <Button
              variant="ghost"
              size="sm"
              icon={<User className="w-4 h-4" />}
              aria-label="User menu"
            />

            {/* Mobile menu button */}
            <Button
              variant="ghost"
              size="sm"
              className="md:hidden"
              icon={isMobileMenuOpen ? <X className="w-4 h-4" /> : <Menu className="w-4 h-4" />}
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              aria-label="Toggle mobile menu"
            />
          </div>
        </div>

        {/* Mobile menu */}
        {isMobileMenuOpen && (
          <div className="md:hidden">
            <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3 border-t"
              style={{
                borderColor: theme.border.primary,
              }}
            >
              {navigation.map((item) => (
                <Link
                  key={item.name}
                  to={item.href}
                  className={cn(
                    'block px-3 py-2 rounded-md text-base font-medium transition-colors duration-200',
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
                  onClick={() => setIsMobileMenuOpen(false)}
                >
                  {item.name}
                </Link>
              ))}
            </div>
          </div>
        )}
      </div>
    </header>
  );
};

export default Header;