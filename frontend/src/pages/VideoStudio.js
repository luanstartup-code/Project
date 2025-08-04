import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';

const VideoStudio = () => {
  const { user } = useAuth();
  const [prompt, setPrompt] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [selectedStyle, setSelectedStyle] = useState('realistic');
  const [duration, setDuration] = useState('10');
  const [quality, setQuality] = useState('1080p');
  const [recentVideos, setRecentVideos] = useState([]);
  const [loading, setLoading] = useState(true);

  const styles = [
    { id: 'realistic', name: 'Realista', icon: '📸', description: 'Vídeos com aparência fotográfica' },
    { id: 'cartoon', name: 'Cartoon', icon: '🎨', description: 'Estilo animado e divertido' },
    { id: 'cinematic', name: 'Cinemático', icon: '🎬', description: 'Qualidade de filme profissional' },
    { id: 'artistic', name: 'Artístico', icon: '🖼️', description: 'Estilo criativo e expressivo' }
  ];

  const templates = [
    { id: 'promo', name: 'Vídeo Promocional', icon: '📢', prompt: 'Criar um vídeo promocional moderno e impactante para um produto inovador' },
    { id: 'education', name: 'Educativo', icon: '📚', prompt: 'Produzir um vídeo educativo claro e didático sobre tecnologia' },
    { id: 'social', name: 'Redes Sociais', icon: '📱', prompt: 'Gerar conteúdo viral para redes sociais com alta engajamento' },
    { id: 'corporate', name: 'Corporativo', icon: '🏢', prompt: 'Criar apresentação corporativa profissional e elegante' }
  ];

  useEffect(() => {
    loadRecentVideos();
  }, []);

  const loadRecentVideos = async () => {
    try {
      setLoading(true);
      const response = await axios.get('/api/videos/recent');
      setRecentVideos(response.data.videos || []);
    } catch (error) {
      console.error('Erro ao carregar vídeos recentes:', error);
    } finally {
      setLoading(false);
    }
  };

  const enhancePrompt = async () => {
    if (!prompt.trim()) return;

    try {
      const response = await axios.post('/api/ai/enhance-prompt', {
        prompt: prompt,
        style: selectedStyle,
        type: 'video'
      });

      if (response.data.success) {
        setPrompt(response.data.enhanced_prompt);
      }
    } catch (error) {
      console.error('Erro ao melhorar prompt:', error);
    }
  };

  const handleGenerate = async () => {
    if (!prompt.trim()) {
      alert('Por favor, descreva o vídeo que deseja criar');
      return;
    }

    setIsGenerating(true);
    
    try {
      const response = await axios.post('/api/videos/generate', {
        prompt: prompt,
        style: selectedStyle,
        duration: parseInt(duration),
        quality: quality,
        model: 'runway-ml' // ou 'openai-sora' dependendo da disponibilidade
      });

      if (response.data.success) {
        alert('Vídeo enviado para geração! Você pode acompanhar o progresso na seção "Meus Vídeos".');
        setPrompt('');
        loadRecentVideos(); // Recarregar lista
      } else {
        alert(`Erro: ${response.data.error}`);
      }
    } catch (error) {
      console.error('Erro ao gerar vídeo:', error);
      alert('Erro ao enviar vídeo para geração. Tente novamente.');
    } finally {
      setIsGenerating(false);
    }
  };

  const formatDuration = (seconds) => {
    if (!seconds) return '0:00';
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed':
        return '✅';
      case 'processing':
        return '⏳';
      case 'failed':
        return '❌';
      default:
        return '📝';
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-purple-600 to-pink-600 rounded-xl p-6 text-white">
        <h1 className="text-2xl font-bold mb-2">🎬 Video Studio</h1>
        <p className="text-purple-100">Crie vídeos incríveis com IA em segundos</p>
      </div>

      {/* Main Content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Form Panel */}
        <div className="lg:col-span-2 space-y-6">
          {/* Prompt Input */}
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Descreva seu vídeo</h3>
            <textarea
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Descreva o vídeo que você quer criar... Ex: Um gato fofo brincando em um jardim ensolarado"
              className="w-full h-32 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none"
            />
            <div className="flex items-center justify-between mt-4">
              <span className="text-sm text-gray-500">{prompt.length}/500 caracteres</span>
              <button 
                onClick={enhancePrompt}
                disabled={!prompt.trim()}
                className="text-sm text-purple-600 hover:text-purple-700 font-medium disabled:opacity-50"
              >
                ✨ Melhorar com IA
              </button>
            </div>
          </div>

          {/* Style Selection */}
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Estilo do vídeo</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {styles.map((style) => (
                <button
                  key={style.id}
                  onClick={() => setSelectedStyle(style.id)}
                  className={`p-4 rounded-lg border-2 transition-all duration-200 ${
                    selectedStyle === style.id
                      ? 'border-purple-500 bg-purple-50 text-purple-700'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <div className="text-2xl mb-2">{style.icon}</div>
                  <div className="font-medium text-sm">{style.name}</div>
                  <div className="text-xs text-gray-500 mt-1">{style.description}</div>
                </button>
              ))}
            </div>
          </div>

          {/* Advanced Options */}
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Opções avançadas</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Duração</label>
                <select 
                  value={duration}
                  onChange={(e) => setDuration(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                >
                  <option value="5">5 segundos</option>
                  <option value="10">10 segundos</option>
                  <option value="15">15 segundos</option>
                  <option value="30">30 segundos</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Qualidade</label>
                <select 
                  value={quality}
                  onChange={(e) => setQuality(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                >
                  <option value="720p">HD (720p)</option>
                  <option value="1080p">Full HD (1080p)</option>
                  <option value="4k">4K</option>
                </select>
              </div>
            </div>
          </div>

          {/* Generate Button */}
          <button
            onClick={handleGenerate}
            disabled={!prompt.trim() || isGenerating}
            className="w-full bg-gradient-to-r from-purple-600 to-pink-600 text-white py-4 px-6 rounded-xl font-semibold hover:from-purple-700 hover:to-pink-700 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
          >
            {isGenerating ? (
              <div className="flex items-center justify-center">
                <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-white mr-3"></div>
                Enviando para geração... ⏳
              </div>
            ) : (
              '🎬 Gerar Vídeo'
            )}
          </button>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Templates */}
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Templates rápidos</h3>
            <div className="space-y-3">
              {templates.map((template) => (
                <button
                  key={template.id}
                  onClick={() => setPrompt(template.prompt)}
                  className="w-full text-left p-3 rounded-lg border border-gray-200 hover:border-purple-300 hover:bg-purple-50 transition-colors duration-200"
                >
                  <div className="flex items-center space-x-3">
                    <span className="text-xl">{template.icon}</span>
                    <div>
                      <div className="font-medium text-sm">{template.name}</div>
                      <div className="text-xs text-gray-500 mt-1">Usar template</div>
                    </div>
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* Recent Videos */}
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Vídeos recentes</h3>
            <div className="space-y-3">
              {loading ? (
                <div className="flex items-center justify-center p-4">
                  <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-purple-500"></div>
                </div>
              ) : recentVideos.length === 0 ? (
                <div className="text-center p-4 text-gray-500">
                  <div className="text-2xl mb-2">📹</div>
                  <p className="text-sm">Nenhum vídeo ainda</p>
                </div>
              ) : (
                recentVideos.map((video) => (
                  <div key={video.id} className="p-3 bg-gray-50 rounded-lg">
                    <div className="flex items-center space-x-3">
                      <div className="w-12 h-8 bg-gradient-to-r from-blue-400 to-blue-600 rounded flex items-center justify-center">
                        <span className="text-white text-xs">{getStatusIcon(video.status)}</span>
                      </div>
                      <div className="flex-1">
                        <div className="text-sm font-medium truncate">{video.title || 'Vídeo sem título'}</div>
                        <div className="text-xs text-gray-500">
                          {formatDuration(video.duration)} • {video.created_at ? new Date(video.created_at).toLocaleDateString() : 'Hoje'}
                        </div>
                      </div>
                    </div>
                  </div>
                ))
              )}
            </div>
            <button 
              onClick={() => window.location.href = '/videos'}
              className="w-full mt-4 text-sm text-purple-600 hover:text-purple-700 font-medium"
            >
              Ver todos →
            </button>
          </div>

          {/* Tips */}
          <div className="bg-gradient-to-br from-blue-50 to-purple-50 rounded-xl p-6 border border-blue-200">
            <h3 className="text-lg font-semibold text-gray-900 mb-3">💡 Dicas</h3>
            <div className="space-y-2 text-sm text-gray-700">
              <p>• Seja específico na descrição</p>
              <p>• Use detalhes visuais (cores, iluminação)</p>
              <p>• Mencione movimento e ação</p>
              <p>• Experimente diferentes estilos</p>
              <p>• Use o botão "Melhorar com IA" para otimizar seu prompt</p>
            </div>
          </div>
        </div>
      </div>

      {/* Information about processing */}
      <div className="bg-blue-50 rounded-xl p-6 border border-blue-200">
        <div className="flex items-start space-x-3">
          <span className="text-2xl">ℹ️</span>
          <div>
            <h3 className="font-semibold text-blue-900 mb-2">Como funciona a geração de vídeos</h3>
            <div className="text-sm text-blue-700 space-y-1">
              <p>• Os vídeos são processados em nossos servidores usando IA avançada</p>
              <p>• O tempo de processamento varia de 2-10 minutos dependendo da duração e qualidade</p>
              <p>• Você receberá uma notificação quando o vídeo estiver pronto</p>
              <p>• Acesse a seção "Meus Vídeos" para acompanhar o progresso</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default VideoStudio;