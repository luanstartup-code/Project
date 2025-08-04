import React from 'react';

const Videos = () => {
  return (
    <div className="space-y-6">
      <div className="bg-gradient-to-r from-green-600 to-teal-600 rounded-xl p-6 text-white">
        <h1 className="text-2xl font-bold mb-2">📹 Meus Vídeos</h1>
        <p className="text-green-100">Biblioteca de vídeos criados</p>
      </div>

      <div className="bg-white rounded-xl p-12 shadow-sm border border-gray-200 text-center">
        <div className="text-6xl mb-4">📹</div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Em Breve</h2>
        <p className="text-gray-600">Sua biblioteca de vídeos aparecerá aqui</p>
      </div>
    </div>
  );
};

export default Videos;