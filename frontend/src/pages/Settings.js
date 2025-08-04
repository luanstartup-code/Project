import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';

const Settings = () => {
  const { user, updateProfile, changePassword } = useAuth();
  const [activeTab, setActiveTab] = useState('profile');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  
  // Profile form
  const [profileData, setProfileData] = useState({
    name: user?.name || '',
    email: user?.email || '',
    bio: user?.bio || ''
  });

  // Password form
  const [passwordData, setPasswordData] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  });

  // API Keys form
  const [apiKeys, setApiKeys] = useState({
    openai_api_key: '',
    gemini_api_key: '',
    heygen_api_key: '',
    runway_api_key: '',
    elevenlabs_api_key: ''
  });

  const [apiKeysStatus, setApiKeysStatus] = useState({});

  useEffect(() => {
    loadApiKeysStatus();
  }, []);

  const loadApiKeysStatus = async () => {
    try {
      const response = await axios.get('/api/settings/api-keys-status');
      if (response.data.success) {
        setApiKeysStatus(response.data.status);
      }
    } catch (error) {
      console.error('Erro ao carregar status das API keys:', error);
    }
  };

  const handleProfileSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    try {
      const result = await updateProfile(profileData);
      if (result.success) {
        setMessage('Perfil atualizado com sucesso!');
      } else {
        setMessage(result.error || 'Erro ao atualizar perfil');
      }
    } catch (error) {
      setMessage('Erro ao atualizar perfil');
    } finally {
      setLoading(false);
    }
  };

  const handlePasswordSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    if (passwordData.newPassword !== passwordData.confirmPassword) {
      setMessage('As senhas não coincidem');
      setLoading(false);
      return;
    }

    if (passwordData.newPassword.length < 6) {
      setMessage('A nova senha deve ter pelo menos 6 caracteres');
      setLoading(false);
      return;
    }

    try {
      const result = await changePassword(passwordData.currentPassword, passwordData.newPassword);
      if (result.success) {
        setMessage('Senha alterada com sucesso!');
        setPasswordData({ currentPassword: '', newPassword: '', confirmPassword: '' });
      } else {
        setMessage(result.error || 'Erro ao alterar senha');
      }
    } catch (error) {
      setMessage('Erro ao alterar senha');
    } finally {
      setLoading(false);
    }
  };

  const handleApiKeysSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    try {
      const response = await axios.post('/api/settings/api-keys', apiKeys);
      if (response.data.success) {
        setMessage('API Keys atualizadas com sucesso!');
        setApiKeys({
          openai_api_key: '',
          gemini_api_key: '',
          heygen_api_key: '',
          runway_api_key: '',
          elevenlabs_api_key: ''
        });
        loadApiKeysStatus();
      } else {
        setMessage(response.data.error || 'Erro ao atualizar API Keys');
      }
    } catch (error) {
      setMessage('Erro ao atualizar API Keys');
    } finally {
      setLoading(false);
    }
  };

  const testApiKey = async (service) => {
    try {
      setLoading(true);
      const response = await axios.post(`/api/settings/test-api-key/${service}`);
      if (response.data.success) {
        setMessage(`✅ ${service.toUpperCase()} API Key funcionando corretamente!`);
      } else {
        setMessage(`❌ Erro ao testar ${service.toUpperCase()}: ${response.data.error}`);
      }
    } catch (error) {
      setMessage(`❌ Erro ao testar ${service.toUpperCase()}`);
    } finally {
      setLoading(false);
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'active':
        return '✅';
      case 'invalid':
        return '❌';
      case 'not_configured':
        return '⚪';
      default:
        return '⚠️';
    }
  };

  const tabs = [
    { id: 'profile', name: 'Perfil', icon: '👤' },
    { id: 'password', name: 'Senha', icon: '🔒' },
    { id: 'api-keys', name: 'API Keys', icon: '🔑' },
    { id: 'environment', name: 'Ambiente', icon: '⚙️' }
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-gray-600 to-gray-800 rounded-xl p-6 text-white">
        <h1 className="text-2xl font-bold mb-2">⚙️ Configurações</h1>
        <p className="text-gray-100">Gerencie sua conta e configurações do sistema</p>
      </div>

      {/* Tabs */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
        <div className="border-b border-gray-200">
          <nav className="flex">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => {
                  setActiveTab(tab.id);
                  setMessage('');
                }}
                className={`px-6 py-4 text-sm font-medium border-b-2 transition-colors ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600 bg-blue-50'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:bg-gray-50'
                }`}
              >
                <span className="mr-2">{tab.icon}</span>
                {tab.name}
              </button>
            ))}
          </nav>
        </div>

        {/* Message */}
        {message && (
          <div className={`mx-6 mt-4 p-3 rounded-lg ${
            message.includes('sucesso') || message.includes('✅') 
              ? 'bg-green-50 text-green-700 border border-green-200'
              : 'bg-red-50 text-red-700 border border-red-200'
          }`}>
            {message}
          </div>
        )}

        {/* Tab Content */}
        <div className="p-6">
          {/* Profile Tab */}
          {activeTab === 'profile' && (
            <form onSubmit={handleProfileSubmit} className="space-y-6">
              <h3 className="text-lg font-semibold text-gray-900">Informações do Perfil</h3>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Nome</label>
                  <input
                    type="text"
                    value={profileData.name}
                    onChange={(e) => setProfileData({...profileData, name: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Email</label>
                  <input
                    type="email"
                    value={profileData.email}
                    onChange={(e) => setProfileData({...profileData, email: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Bio</label>
                <textarea
                  value={profileData.bio}
                  onChange={(e) => setProfileData({...profileData, bio: e.target.value})}
                  rows={3}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Conte um pouco sobre você..."
                />
              </div>

              <button
                type="submit"
                disabled={loading}
                className="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 disabled:opacity-50 transition-colors"
              >
                {loading ? 'Salvando...' : 'Salvar Alterações'}
              </button>
            </form>
          )}

          {/* Password Tab */}
          {activeTab === 'password' && (
            <form onSubmit={handlePasswordSubmit} className="space-y-6">
              <h3 className="text-lg font-semibold text-gray-900">Alterar Senha</h3>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Senha Atual</label>
                <input
                  type="password"
                  value={passwordData.currentPassword}
                  onChange={(e) => setPasswordData({...passwordData, currentPassword: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Nova Senha</label>
                <input
                  type="password"
                  value={passwordData.newPassword}
                  onChange={(e) => setPasswordData({...passwordData, newPassword: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                  minLength={6}
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Confirmar Nova Senha</label>
                <input
                  type="password"
                  value={passwordData.confirmPassword}
                  onChange={(e) => setPasswordData({...passwordData, confirmPassword: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                  minLength={6}
                />
              </div>

              <button
                type="submit"
                disabled={loading}
                className="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 disabled:opacity-50 transition-colors"
              >
                {loading ? 'Alterando...' : 'Alterar Senha'}
              </button>
            </form>
          )}

          {/* API Keys Tab */}
          {activeTab === 'api-keys' && (
            <div className="space-y-6">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-semibold text-gray-900">Configurar API Keys</h3>
                <button
                  onClick={loadApiKeysStatus}
                  className="text-sm text-blue-600 hover:text-blue-700"
                >
                  🔄 Atualizar Status
                </button>
              </div>

              <div className="bg-blue-50 rounded-lg p-4 mb-6">
                <h4 className="font-medium text-blue-900 mb-2">🔒 Segurança das API Keys</h4>
                <p className="text-sm text-blue-700">
                  Suas API keys são criptografadas e armazenadas com segurança. Nunca compartilhe suas chaves com terceiros.
                </p>
              </div>

              <form onSubmit={handleApiKeysSubmit} className="space-y-6">
                {/* OpenAI */}
                <div className="border border-gray-200 rounded-lg p-4">
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center space-x-2">
                      <span className="text-lg">🤖</span>
                      <h4 className="font-medium">OpenAI</h4>
                      <span className="text-sm">{getStatusIcon(apiKeysStatus.openai)}</span>
                    </div>
                    <button
                      type="button"
                      onClick={() => testApiKey('openai')}
                      className="text-sm text-blue-600 hover:text-blue-700"
                    >
                      Testar
                    </button>
                  </div>
                  <input
                    type="password"
                    value={apiKeys.openai_api_key}
                    onChange={(e) => setApiKeys({...apiKeys, openai_api_key: e.target.value})}
                    placeholder="sk-proj-..."
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  <p className="text-xs text-gray-500 mt-1">
                    Obtenha em: <a href="https://platform.openai.com/api-keys" target="_blank" rel="noopener noreferrer" className="text-blue-600">platform.openai.com</a>
                  </p>
                </div>

                {/* Gemini */}
                <div className="border border-gray-200 rounded-lg p-4">
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center space-x-2">
                      <span className="text-lg">🧠</span>
                      <h4 className="font-medium">Google Gemini</h4>
                      <span className="text-sm">{getStatusIcon(apiKeysStatus.gemini)}</span>
                    </div>
                    <button
                      type="button"
                      onClick={() => testApiKey('gemini')}
                      className="text-sm text-blue-600 hover:text-blue-700"
                    >
                      Testar
                    </button>
                  </div>
                  <input
                    type="password"
                    value={apiKeys.gemini_api_key}
                    onChange={(e) => setApiKeys({...apiKeys, gemini_api_key: e.target.value})}
                    placeholder="AIza..."
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  <p className="text-xs text-gray-500 mt-1">
                    Obtenha em: <a href="https://aistudio.google.com/app/apikey" target="_blank" rel="noopener noreferrer" className="text-blue-600">aistudio.google.com</a>
                  </p>
                </div>

                {/* HeyGen */}
                <div className="border border-gray-200 rounded-lg p-4">
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center space-x-2">
                      <span className="text-lg">🎭</span>
                      <h4 className="font-medium">HeyGen</h4>
                      <span className="text-sm">{getStatusIcon(apiKeysStatus.heygen)}</span>
                    </div>
                    <button
                      type="button"
                      onClick={() => testApiKey('heygen')}
                      className="text-sm text-blue-600 hover:text-blue-700"
                    >
                      Testar
                    </button>
                  </div>
                  <input
                    type="password"
                    value={apiKeys.heygen_api_key}
                    onChange={(e) => setApiKeys({...apiKeys, heygen_api_key: e.target.value})}
                    placeholder="Sua chave HeyGen..."
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  <p className="text-xs text-gray-500 mt-1">
                    Obtenha em: <a href="https://heygen.com" target="_blank" rel="noopener noreferrer" className="text-blue-600">heygen.com</a>
                  </p>
                </div>

                {/* Runway ML */}
                <div className="border border-gray-200 rounded-lg p-4">
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center space-x-2">
                      <span className="text-lg">🎬</span>
                      <h4 className="font-medium">Runway ML</h4>
                      <span className="text-sm">{getStatusIcon(apiKeysStatus.runway)}</span>
                    </div>
                    <button
                      type="button"
                      onClick={() => testApiKey('runway')}
                      className="text-sm text-blue-600 hover:text-blue-700"
                    >
                      Testar
                    </button>
                  </div>
                  <input
                    type="password"
                    value={apiKeys.runway_api_key}
                    onChange={(e) => setApiKeys({...apiKeys, runway_api_key: e.target.value})}
                    placeholder="key_..."
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  <p className="text-xs text-gray-500 mt-1">
                    Obtenha em: <a href="https://runwayml.com" target="_blank" rel="noopener noreferrer" className="text-blue-600">runwayml.com</a>
                  </p>
                </div>

                {/* ElevenLabs */}
                <div className="border border-gray-200 rounded-lg p-4">
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center space-x-2">
                      <span className="text-lg">🔊</span>
                      <h4 className="font-medium">ElevenLabs</h4>
                      <span className="text-sm">{getStatusIcon(apiKeysStatus.elevenlabs)}</span>
                    </div>
                    <button
                      type="button"
                      onClick={() => testApiKey('elevenlabs')}
                      className="text-sm text-blue-600 hover:text-blue-700"
                    >
                      Testar
                    </button>
                  </div>
                  <input
                    type="password"
                    value={apiKeys.elevenlabs_api_key}
                    onChange={(e) => setApiKeys({...apiKeys, elevenlabs_api_key: e.target.value})}
                    placeholder="sk_..."
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  <p className="text-xs text-gray-500 mt-1">
                    Obtenha em: <a href="https://elevenlabs.io" target="_blank" rel="noopener noreferrer" className="text-blue-600">elevenlabs.io</a>
                  </p>
                </div>

                <button
                  type="submit"
                  disabled={loading}
                  className="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 disabled:opacity-50 transition-colors"
                >
                  {loading ? 'Salvando...' : 'Salvar API Keys'}
                </button>
              </form>
            </div>
          )}

          {/* Environment Tab */}
          {activeTab === 'environment' && (
            <div className="space-y-6">
              <h3 className="text-lg font-semibold text-gray-900">Configuração do Ambiente</h3>
              
              <div className="bg-green-50 rounded-lg p-6">
                <h4 className="font-medium text-green-900 mb-3">🔧 Como Configurar Variáveis de Ambiente</h4>
                <div className="space-y-4 text-sm text-green-700">
                  <div>
                    <h5 className="font-medium mb-2">📁 Método 1: Usar setup_env.py (Recomendado)</h5>
                    <div className="bg-green-100 rounded p-3 font-mono text-xs">
                      <p>python3 setup_env.py</p>
                    </div>
                    <p className="mt-2">Este script interativo irá guiá-lo através da configuração de todas as variáveis.</p>
                  </div>

                  <div>
                    <h5 className="font-medium mb-2">✏️ Método 2: Editar .env manualmente</h5>
                    <div className="bg-green-100 rounded p-3 font-mono text-xs space-y-1">
                      <p>OPENAI_API_KEY=sk-proj-sua_chave_aqui</p>
                      <p>GEMINI_API_KEY=AIza_sua_chave_aqui</p>
                      <p>HEYGEN_API_KEY=sua_chave_heygen</p>
                      <p>RUNWAY_API_KEY=key_sua_chave_runway</p>
                      <p>ELEVENLABS_API_KEY=sk_sua_chave_elevenlabs</p>
                    </div>
                  </div>

                  <div>
                    <h5 className="font-medium mb-2">🌐 Método 3: Interface Web (Esta página)</h5>
                    <p>Use a aba "API Keys" acima para configurar suas chaves através da interface web.</p>
                  </div>
                </div>
              </div>

              <div className="bg-yellow-50 rounded-lg p-6">
                <h4 className="font-medium text-yellow-900 mb-3">⚠️ Importante</h4>
                <div className="space-y-2 text-sm text-yellow-700">
                  <p>• Nunca commite arquivos .env com chaves reais no Git</p>
                  <p>• Use o arquivo .env.example como modelo</p>
                  <p>• Em produção, use variáveis de ambiente do sistema</p>
                  <p>• Revogue chaves compromettidas imediatamente</p>
                </div>
              </div>

              <div className="bg-blue-50 rounded-lg p-6">
                <h4 className="font-medium text-blue-900 mb-3">🚀 Deploy em Produção</h4>
                <div className="space-y-2 text-sm text-blue-700">
                  <p><strong>Render:</strong> Configure as variáveis na aba Environment</p>
                  <p><strong>Vercel:</strong> Use vercel env add para cada variável</p>
                  <p><strong>Heroku:</strong> Use heroku config:set NOME_VAR=valor</p>
                  <p><strong>Docker:</strong> Use --env-file .env ou -e NOME_VAR=valor</p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Settings;