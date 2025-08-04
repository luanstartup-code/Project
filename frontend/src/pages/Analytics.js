import React from 'react';

const Analytics = () => {
  return (
    <div className="space-y-6">
      <div className="bg-gradient-to-r from-orange-600 to-red-600 rounded-xl p-6 text-white">
        <h1 className="text-2xl font-bold mb-2">📈 Analytics</h1>
        <p className="text-orange-100">Métricas e relatórios</p>
      </div>

      <div className="bg-white rounded-xl p-12 shadow-sm border border-gray-200 text-center">
        <div className="text-6xl mb-4">📊</div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Dashboard em Construção</h2>
        <p className="text-gray-600">Métricas detalhadas em breve</p>
      </div>
    </div>
  );
};

export default Analytics;