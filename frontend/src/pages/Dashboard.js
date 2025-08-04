import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import axios from 'axios';

const Dashboard = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState({
    totalVideos: 0,
    totalAvatars: 0,
    totalChats: 0,
    timeSpent: '0h'
  });
  const [recentActivity, setRecentActivity] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      
      // Carregar estatísticas do dashboard
      const statsResponse = await axios.get('/api/dashboard/stats');
      if (statsResponse.data.success) {
        setStats(statsResponse.data.stats);
      }

      // Carregar atividade recente
      const activityResponse = await axios.get('/api/dashboard/activity');
      if (activityResponse.data.success) {
        setRecentActivity(activityResponse.data.activities);
      }
    } catch (error) {
      console.error('Erro ao carregar dados do dashboard:', error);
      // Manter dados padrão em caso de erro
    } finally {
      setLoading(false);
    }
  };

  const quickActions = [
    {
      name: 'Novo Vídeo',
      description: 'Criar vídeo com IA',
      href: '/video-studio',
      icon: '🎬',
      color: 'bg-gradient-to-r from-blue-500 to-blue-600'
    },
    {
      name: 'Chat IA',
      description: 'Conversar com assistente',
      href: '/chat',
      icon: '💬',
      color: 'bg-gradient-to-r from-green-500 to-green-600'
    },
    {
      name: 'Criar Avatar',
      description: 'Gerar novo avatar',
      href: '/avatar-studio',
      icon: '🎭',
      color: 'bg-gradient-to-r from-purple-500 to-purple-600'
    },
    {
      name: 'Ver Vídeos',
      description: 'Biblioteca de vídeos',
      href: '/videos',
      icon: '📹',
      color: 'bg-gradient-to-r from-orange-500 to-orange-600'
    }
  ];

  const formatActivityTime = (timestamp) => {
    if (!timestamp) return 'agora';
    
    const now = new Date();
    const activityTime = new Date(timestamp);
    const diffInMs = now - activityTime;
    const diffInMinutes = Math.floor(diffInMs / (1000 * 60));
    const diffInHours = Math.floor(diffInMs / (1000 * 60 * 60));
    const diffInDays = Math.floor(diffInMs / (1000 * 60 * 60 * 24));

    if (diffInMinutes < 60) {
      return `${diffInMinutes} min atrás`;
    } else if (diffInHours < 24) {
      return `${diffInHours}h atrás`;
    } else {
      return `${diffInDays} dia${diffInDays > 1 ? 's' : ''} atrás`;
    }
  };

  const getActivityIcon = (type) => {
    switch (type) {
      case 'video_created':
        return '🎬';
      case 'chat_session':
        return '💬';
      case 'avatar_created':
        return '🎭';
      case 'video_completed':
        return '✅';
      default:
        return '📝';
    }
  };

  const getStatusBadge = (status) => {
    switch (status) {
      case 'completed':
        return (
          <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
            ✓ Concluído
          </span>
        );
      case 'processing':
        return (
          <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
            ⏳ Processando
          </span>
        );
      case 'failed':
        return (
          <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800">
            ❌ Falhou
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
            📝 Pendente
          </span>
        );
    }
  };

  if (loading) {
    return (
      <div className="space-y-6">
        {/* Loading skeleton */}
        <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl p-6 text-white">
          <div className="animate-pulse">
            <div className="h-8 bg-white/20 rounded w-64 mb-2"></div>
            <div className="h-4 bg-white/20 rounded w-48"></div>
          </div>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
              <div className="animate-pulse">
                <div className="h-4 bg-gray-200 rounded w-24 mb-2"></div>
                <div className="h-8 bg-gray-200 rounded w-16 mb-2"></div>
                <div className="h-3 bg-gray-200 rounded w-20"></div>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Welcome Header */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl p-6 text-white">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold">Bem-vindo de volta, {user?.name}! 👋</h1>
            <p className="text-blue-100 mt-1">
              Pronto para criar conteúdo incrível com IA hoje?
            </p>
          </div>
          <div className="hidden md:block">
            <div className="text-6xl opacity-20">🎬</div>
          </div>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Vídeos Criados</p>
              <p className="text-2xl font-bold text-gray-900 mt-1">{stats.totalVideos}</p>
              <p className="text-sm text-gray-500 mt-1">Total de vídeos</p>
            </div>
            <div className="w-12 h-12 bg-blue-500 rounded-lg flex items-center justify-center text-2xl">
              🎬
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Avatares</p>
              <p className="text-2xl font-bold text-gray-900 mt-1">{stats.totalAvatars}</p>
              <p className="text-sm text-gray-500 mt-1">Criados por você</p>
            </div>
            <div className="w-12 h-12 bg-purple-500 rounded-lg flex items-center justify-center text-2xl">
              🎭
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Chats IA</p>
              <p className="text-2xl font-bold text-gray-900 mt-1">{stats.totalChats}</p>
              <p className="text-sm text-gray-500 mt-1">Conversas realizadas</p>
            </div>
            <div className="w-12 h-12 bg-green-500 rounded-lg flex items-center justify-center text-2xl">
              💬
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Tempo Economizado</p>
              <p className="text-2xl font-bold text-gray-900 mt-1">{stats.timeSpent}</p>
              <p className="text-sm text-gray-500 mt-1">vs método tradicional</p>
            </div>
            <div className="w-12 h-12 bg-orange-500 rounded-lg flex items-center justify-center text-2xl">
              ⏱️
            </div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div>
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Ações Rápidas</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {quickActions.map((action) => (
            <Link
              key={action.name}
              to={action.href}
              className="block group"
            >
              <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200 hover:shadow-md transition-shadow duration-200">
                <div className={`w-12 h-12 ${action.color} rounded-lg flex items-center justify-center text-2xl mb-4 group-hover:scale-110 transition-transform duration-200`}>
                  {action.icon}
                </div>
                <h3 className="font-semibold text-gray-900">{action.name}</h3>
                <p className="text-sm text-gray-600 mt-1">{action.description}</p>
              </div>
            </Link>
          ))}
        </div>
      </div>

      {/* Recent Activity & Tips */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Activity */}
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Atividade Recente</h3>
          <div className="space-y-4">
            {recentActivity.length === 0 ? (
              <div className="text-center p-4 text-gray-500">
                <div className="text-2xl mb-2">📝</div>
                <p className="text-sm">Nenhuma atividade recente</p>
                <p className="text-xs mt-1">Comece criando um vídeo ou conversando com a IA</p>
              </div>
            ) : (
              recentActivity.map((activity) => (
                <div key={activity.id} className="flex items-center space-x-3">
                  <div className="flex-shrink-0">
                    <span className="text-2xl">{getActivityIcon(activity.type)}</span>
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900">{activity.title}</p>
                    <p className="text-xs text-gray-500">{formatActivityTime(activity.created_at)}</p>
                  </div>
                  <div className="flex-shrink-0">
                    {activity.status && getStatusBadge(activity.status)}
                  </div>
                </div>
              ))
            )}
          </div>
          <div className="mt-4 pt-4 border-t border-gray-200">
            <Link 
              to="/analytics" 
              className="text-sm text-blue-600 hover:text-blue-700 font-medium"
            >
              Ver todas as atividades →
            </Link>
          </div>
        </div>

        {/* Tips & Features */}
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Dicas & Recursos</h3>
          <div className="space-y-4">
            <div className="bg-blue-50 rounded-lg p-4">
              <div className="flex items-start space-x-3">
                <span className="text-2xl">💡</span>
                <div>
                  <h4 className="font-medium text-blue-900">Prompt Enhancement</h4>
                  <p className="text-sm text-blue-700 mt-1">
                    Use nosso sistema de melhoria de prompts para resultados mais precisos
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-purple-50 rounded-lg p-4">
              <div className="flex items-start space-x-3">
                <span className="text-2xl">🎭</span>
                <div>
                  <h4 className="font-medium text-purple-900">Avatares Realistas</h4>
                  <p className="text-sm text-purple-700 mt-1">
                    Crie avatares ultra-realistas com nossa integração HeyGen
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-green-50 rounded-lg p-4">
              <div className="flex items-start space-x-3">
                <span className="text-2xl">🤖</span>
                <div>
                  <h4 className="font-medium text-green-900">IA Dupla</h4>
                  <p className="text-sm text-green-700 mt-1">
                    Sistema com OpenAI + Gemini para máxima disponibilidade
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom CTA */}
      <div className="bg-gradient-to-r from-orange-500 to-pink-500 rounded-xl p-6 text-white">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-xl font-bold">Pronto para o próximo nível?</h3>
            <p className="text-orange-100 mt-1">
              Explore todas as funcionalidades da plataforma CineAI
            </p>
          </div>
          <Link
            to="/video-studio"
            className="bg-white text-orange-500 px-6 py-3 rounded-lg font-medium hover:bg-orange-50 transition-colors duration-200"
          >
            Começar Agora
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;