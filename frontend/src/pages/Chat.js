import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';

const Chat = () => {
  const { user } = useAuth();
  const [sessions, setSessions] = useState([]);
  const [currentSession, setCurrentSession] = useState(null);
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionsLoading, setSessionsLoading] = useState(true);

  // Carregar sessões do usuário
  useEffect(() => {
    loadSessions();
  }, []);

  // Carregar mensagens quando sessão mudar
  useEffect(() => {
    if (currentSession) {
      loadMessages(currentSession.id);
    }
  }, [currentSession]);

  const loadSessions = async () => {
    try {
      setSessionsLoading(true);
      const response = await axios.get('/api/chat/sessions');
      setSessions(response.data.sessions || []);
      
      // Se não há sessão atual e há sessões, selecionar a primeira
      if (!currentSession && response.data.sessions?.length > 0) {
        setCurrentSession(response.data.sessions[0]);
      }
    } catch (error) {
      console.error('Erro ao carregar sessões:', error);
    } finally {
      setSessionsLoading(false);
    }
  };

  const loadMessages = async (sessionId) => {
    try {
      const response = await axios.get(`/api/chat/sessions/${sessionId}/messages`);
      setMessages(response.data.messages || []);
    } catch (error) {
      console.error('Erro ao carregar mensagens:', error);
      setMessages([]);
    }
  };

  const createNewSession = async () => {
    try {
      const response = await axios.post('/api/chat/sessions', {
        title: 'Nova Conversa'
      });
      
      const newSession = response.data.session;
      setSessions(prev => [newSession, ...prev]);
      setCurrentSession(newSession);
      setMessages([]);
    } catch (error) {
      console.error('Erro ao criar sessão:', error);
    }
  };

  const sendMessage = async () => {
    if (!inputMessage.trim() || isLoading || !currentSession) return;

    // Se não há sessão, criar uma nova
    if (!currentSession) {
      await createNewSession();
      return;
    }

    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: inputMessage,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    const messageToSend = inputMessage;
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await axios.post(`/api/chat/sessions/${currentSession.id}/messages`, {
        content: messageToSend
      });

      if (response.data.success) {
        // Adicionar mensagem do assistente
        const assistantMessage = {
          id: Date.now() + 1,
          role: 'assistant',
          content: response.data.response,
          timestamp: new Date().toISOString()
        };
        setMessages(prev => [...prev, assistantMessage]);
      }
    } catch (error) {
      console.error('Erro ao enviar mensagem:', error);
      
      // Mensagem de erro se API falhar
      const errorMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: 'Desculpe, ocorreu um erro ao processar sua mensagem. Tente novamente.',
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const deleteSession = async (sessionId) => {
    if (!window.confirm('Deseja deletar esta conversa?')) return;

    try {
      await axios.delete(`/api/chat/sessions/${sessionId}`);
      setSessions(prev => prev.filter(s => s.id !== sessionId));
      
      if (currentSession?.id === sessionId) {
        const remainingSessions = sessions.filter(s => s.id !== sessionId);
        setCurrentSession(remainingSessions[0] || null);
        setMessages([]);
      }
    } catch (error) {
      console.error('Erro ao deletar sessão:', error);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const formatTime = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString([], {
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="flex h-[calc(100vh-8rem)] bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
      {/* Sidebar com sessões */}
      <div className="w-80 border-r border-gray-200 flex flex-col">
        {/* Header da sidebar */}
        <div className="p-4 border-b border-gray-200 bg-gray-50">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold text-gray-900">Conversas</h2>
            <button
              onClick={createNewSession}
              className="bg-blue-500 text-white px-3 py-1 rounded-lg text-sm hover:bg-blue-600 transition-colors"
            >
              + Nova
            </button>
          </div>
        </div>

        {/* Lista de sessões */}
        <div className="flex-1 overflow-y-auto p-2">
          {sessionsLoading ? (
            <div className="flex items-center justify-center p-4">
              <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-500"></div>
            </div>
          ) : sessions.length === 0 ? (
            <div className="text-center p-4 text-gray-500">
              <div className="text-4xl mb-2">💬</div>
              <p className="text-sm">Nenhuma conversa ainda</p>
              <button
                onClick={createNewSession}
                className="mt-2 text-blue-500 text-sm hover:underline"
              >
                Criar primeira conversa
              </button>
            </div>
          ) : (
            <div className="space-y-1">
              {sessions.map((session) => (
                <div
                  key={session.id}
                  className={`p-3 rounded-lg cursor-pointer group transition-colors ${
                    currentSession?.id === session.id
                      ? 'bg-blue-50 border border-blue-200'
                      : 'hover:bg-gray-50'
                  }`}
                  onClick={() => setCurrentSession(session)}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex-1 min-w-0">
                      <h3 className="text-sm font-medium text-gray-900 truncate">
                        {session.title || 'Conversa sem título'}
                      </h3>
                      <p className="text-xs text-gray-500 mt-1">
                        {session.message_count || 0} mensagens
                      </p>
                    </div>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        deleteSession(session.id);
                      }}
                      className="opacity-0 group-hover:opacity-100 p-1 text-red-500 hover:bg-red-50 rounded transition-all"
                    >
                      🗑️
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Área principal do chat */}
      <div className="flex-1 flex flex-col">
        {/* Header do chat */}
        <div className="p-4 border-b border-gray-200 bg-gray-50">
          {currentSession ? (
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center">
                <span className="text-white text-lg">🤖</span>
              </div>
              <div>
                <h3 className="font-semibold text-gray-900">
                  {currentSession.title || 'Assistente CineAI'}
                </h3>
                <p className="text-sm text-gray-500">Online - Pronto para ajudar</p>
              </div>
            </div>
          ) : (
            <div className="text-center">
              <h3 className="font-semibold text-gray-900">Selecione uma conversa</h3>
              <p className="text-sm text-gray-500">Ou crie uma nova para começar</p>
            </div>
          )}
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50">
          {!currentSession ? (
            <div className="flex items-center justify-center h-full">
              <div className="text-center">
                <div className="text-6xl mb-4">💬</div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Bem-vindo ao Chat IA</h3>
                <p className="text-gray-600 mb-4">
                  Converse com nossa IA para criar conteúdo incrível
                </p>
                <button
                  onClick={createNewSession}
                  className="bg-gradient-to-r from-blue-500 to-purple-500 text-white px-6 py-3 rounded-lg font-medium hover:from-blue-600 hover:to-purple-600 transition-all"
                >
                  Iniciar Conversa
                </button>
              </div>
            </div>
          ) : messages.length === 0 ? (
            <div className="flex items-center justify-center h-full">
              <div className="text-center">
                <div className="text-4xl mb-4">🤖</div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Conversa vazia</h3>
                <p className="text-gray-600">Envie uma mensagem para começar</p>
              </div>
            </div>
          ) : (
            <>
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                      message.role === 'user'
                        ? 'bg-gradient-to-r from-blue-500 to-purple-500 text-white'
                        : 'bg-white text-gray-900 border border-gray-200'
                    }`}
                  >
                    <p className="text-sm">{message.content}</p>
                    <p className={`text-xs mt-1 ${
                      message.role === 'user' ? 'text-blue-100' : 'text-gray-500'
                    }`}>
                      {formatTime(message.timestamp)}
                    </p>
                  </div>
                </div>
              ))}

              {/* Loading indicator */}
              {isLoading && (
                <div className="flex justify-start">
                  <div className="bg-white text-gray-900 border border-gray-200 max-w-xs lg:max-w-md px-4 py-2 rounded-lg">
                    <div className="flex items-center space-x-2">
                      <div className="animate-pulse">🤖</div>
                      <div className="flex space-x-1">
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </>
          )}
        </div>

        {/* Input */}
        {currentSession && (
          <div className="p-4 border-t border-gray-200 bg-white">
            <div className="flex space-x-3">
              <textarea
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Digite sua mensagem... (Enter para enviar)"
                className="flex-1 resize-none border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                rows="2"
                disabled={isLoading}
              />
              <button
                onClick={sendMessage}
                disabled={!inputMessage.trim() || isLoading}
                className="bg-gradient-to-r from-blue-500 to-purple-500 text-white px-6 py-2 rounded-lg font-medium hover:from-blue-600 hover:to-purple-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
              >
                {isLoading ? (
                  <div className="w-5 h-5 animate-spin rounded-full border-2 border-white border-t-transparent"></div>
                ) : (
                  'Enviar'
                )}
              </button>
            </div>
            
            {/* Quick Actions */}
            <div className="flex flex-wrap gap-2 mt-3">
              <button
                onClick={() => setInputMessage('Como criar um vídeo promocional?')}
                className="text-xs bg-gray-100 hover:bg-gray-200 text-gray-700 px-3 py-1 rounded-full transition-colors"
              >
                💡 Vídeo promocional
              </button>
              <button
                onClick={() => setInputMessage('Quais estilos de avatar estão disponíveis?')}
                className="text-xs bg-gray-100 hover:bg-gray-200 text-gray-700 px-3 py-1 rounded-full transition-colors"
              >
                🎭 Estilos de avatar
              </button>
              <button
                onClick={() => setInputMessage('Como melhorar meus prompts?')}
                className="text-xs bg-gray-100 hover:bg-gray-200 text-gray-700 px-3 py-1 rounded-full transition-colors"
              >
                ✨ Melhorar prompts
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Chat;