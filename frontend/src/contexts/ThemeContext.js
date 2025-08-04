import React, { createContext, useContext, useState, useEffect } from 'react';
import { theme } from '../design-system/theme';

const ThemeContext = createContext();

export const ThemeProvider = ({ children }) => {
  const [isDark, setIsDark] = useState(() => {
    // Verificar preferência salva no localStorage
    const saved = localStorage.getItem('theme');
    if (saved) {
      return saved === 'dark';
    }
    // Verificar preferência do sistema
    return window.matchMedia('(prefers-color-scheme: dark)').matches;
  });

  const currentTheme = isDark ? theme.colors.dark : theme.colors.light;

  const toggleTheme = () => {
    setIsDark(!isDark);
  };

  const setTheme = (theme) => {
    setIsDark(theme === 'dark');
  };

  // Salvar preferência no localStorage
  useEffect(() => {
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
    
    // Aplicar classe no body
    document.body.classList.toggle('dark', isDark);
    document.body.classList.toggle('light', !isDark);
  }, [isDark]);

  // Escutar mudanças na preferência do sistema
  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    
    const handleChange = (e) => {
      if (!localStorage.getItem('theme')) {
        setIsDark(e.matches);
      }
    };

    mediaQuery.addEventListener('change', handleChange);
    return () => mediaQuery.removeEventListener('change', handleChange);
  }, []);

  const value = {
    isDark,
    theme: currentTheme,
    fullTheme: theme,
    toggleTheme,
    setTheme,
  };

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
};

export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
};