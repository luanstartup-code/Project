import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTheme } from '../contexts/ThemeContext';
import Layout from '../components/layout/Layout';
import { Loader2 } from 'lucide-react';

const VideoCreate = () => {
  const { theme } = useTheme();
  const navigate = useNavigate();

  useEffect(() => {
    // Redirecionar para o Video Studio após um breve delay
    const timer = setTimeout(() => {
      navigate('/video-studio');
    }, 1000);

    return () => clearTimeout(timer);
  }, [navigate]);

  return (
    <Layout>
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <Loader2 className="mx-auto h-8 w-8 animate-spin mb-4"
            style={{ color: theme.text.primary }}
          />
          <h3 className="text-lg font-medium mb-2"
            style={{ color: theme.text.primary }}
          >
            Redirecionando para o Video Studio...
          </h3>
          <p className="text-sm"
            style={{ color: theme.text.secondary }}
          >
            Aguarde um momento
          </p>
        </div>
      </div>
    </Layout>
  );
};

export default VideoCreate;