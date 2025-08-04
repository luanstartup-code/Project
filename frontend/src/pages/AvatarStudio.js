import React from 'react';

const AvatarStudio = () => {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-purple-600 to-indigo-600 rounded-xl p-6 text-white">
        <h1 className="text-2xl font-bold mb-2">🎭 Avatar Studio</h1>
        <p className="text-purple-100">Crie avatares realistas com IA</p>
      </div>

      {/* Em construção */}
      <div className="bg-white rounded-xl p-12 shadow-sm border border-gray-200 text-center">
        <div className="text-6xl mb-4">🚧</div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Em Desenvolvimento</h2>
        <p className="text-gray-600 mb-6">
          O Avatar Studio estará disponível em breve com integração HeyGen
        </p>
        <div className="bg-blue-50 rounded-lg p-4 text-left max-w-md mx-auto">
          <h3 className="font-semibold text-blue-900 mb-2">🔮 Funcionalidades previstas:</h3>
          <ul className="text-sm text-blue-700 space-y-1">
            <li>• Criação de avatares realistas</li>
            <li>• Upload de fotos personalizadas</li>
            <li>• Animação facial avançada</li>
            <li>• Sincronização labial</li>
            <li>• Múltiplos estilos e poses</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default AvatarStudio;