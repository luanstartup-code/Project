import React from 'react';
import { useTheme } from '../../contexts/ThemeContext';
import Header from './Header';
import Sidebar from './Sidebar';
import { cn } from '../../utils/cn';

const Layout = ({ children, showSidebar = true }) => {
  const { theme, isDark } = useTheme();

  return (
    <div
      className={cn(
        'min-h-screen transition-colors duration-200',
        isDark ? 'bg-gray-900 text-white' : 'bg-gray-50 text-gray-900'
      )}
      style={{
        backgroundColor: theme.background.primary,
        color: theme.text.primary,
      }}
    >
      <Header />
      
      <div className="flex">
        {showSidebar && <Sidebar />}
        
        <main
          className={cn(
            'flex-1 transition-all duration-200',
            showSidebar ? 'ml-64' : 'ml-0'
          )}
        >
          <div className="p-6">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
};

export default Layout;