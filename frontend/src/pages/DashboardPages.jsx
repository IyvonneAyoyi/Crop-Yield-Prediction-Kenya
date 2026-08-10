import React from 'react';

export const Overview = () => (
  <div className="p-8 font-manrope">
    <h2 className="text-3xl font-bold mb-6">System Overview</h2>
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
        <h3 className="text-lg font-semibold mb-2">Total Predictions</h3>
        <p className="text-4xl font-bold text-primary">1,245</p>
      </div>
      <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
        <h3 className="text-lg font-semibold mb-2">Active Models</h3>
        <p className="text-4xl font-bold text-primary">4</p>
      </div>
      <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
        <h3 className="text-lg font-semibold mb-2">System Status</h3>
        <p className="text-4xl font-bold text-secondary">Healthy</p>
      </div>
    </div>
  </div>
);

export const PredictProduction = () => (
  <div className="p-8 font-manrope">
    <h2 className="text-3xl font-bold mb-6">Predict Production</h2>
    <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
      <p className="text-gray-600 mb-4">Select parameters to run a custom yield simulation based on projected environmental data.</p>
      {/* Form placeholders */}
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium mb-1">Target Crop</label>
          <select className="w-full border p-2 rounded"><option>Maize</option><option>Wheat</option></select>
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Target County</label>
          <select className="w-full border p-2 rounded"><option>Uasin Gishu</option><option>Trans Nzoia</option></select>
        </div>
        <button className="bg-primary text-white px-4 py-2 rounded mt-4">Run Simulation</button>
      </div>
    </div>
  </div>
);

export const CropAnalytics = () => (
  <div className="p-8 font-manrope">
    <h2 className="text-3xl font-bold mb-6">Crop Analytics</h2>
    <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 h-64 flex items-center justify-center">
      <p className="text-gray-400">Yield Comparison Charts will render here</p>
    </div>
  </div>
);

export const EnvironmentalData = () => (
  <div className="p-8 font-manrope">
    <h2 className="text-3xl font-bold mb-6">Environmental Data Explorer</h2>
    <div className="grid grid-cols-2 gap-6">
      <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 h-48 flex items-center justify-center text-gray-400">Precipitation Map</div>
      <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 h-48 flex items-center justify-center text-gray-400">NDVI Satellite Imagery</div>
    </div>
  </div>
);

export const ModelPerformance = () => (
  <div className="p-8 font-manrope">
    <h2 className="text-3xl font-bold mb-6">Model Performance Metrics</h2>
    <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
      <ul className="space-y-3">
        <li className="flex justify-between border-b pb-2"><span>R-Squared (R²)</span> <span className="font-bold">0.87</span></li>
        <li className="flex justify-between border-b pb-2"><span>Mean Absolute Error (MAE)</span> <span className="font-bold">0.15 t/ha</span></li>
        <li className="flex justify-between"><span>Root Mean Square Error (RMSE)</span> <span className="font-bold">0.22 t/ha</span></li>
      </ul>
    </div>
  </div>
);

export const PredictionHistory = () => (
  <div className="p-8 font-manrope">
    <h2 className="text-3xl font-bold mb-6">Prediction History Logs</h2>
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
      <table className="w-full text-left">
        <thead className="bg-gray-50 border-b">
          <tr><th className="p-4">Date</th><th className="p-4">County</th><th className="p-4">Crop</th><th className="p-4">Result</th></tr>
        </thead>
        <tbody>
          <tr className="border-b"><td className="p-4">2024-05-12</td><td className="p-4">Uasin Gishu</td><td className="p-4">Maize</td><td className="p-4">4.2 t/ha</td></tr>
          <tr><td className="p-4">2024-05-11</td><td className="p-4">Narok</td><td className="p-4">Wheat</td><td className="p-4">2.8 t/ha</td></tr>
        </tbody>
      </table>
    </div>
  </div>
);

export const About = () => (
  <div className="p-8 font-manrope">
    <h2 className="text-3xl font-bold mb-6">About CropYield Kenya</h2>
    <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 max-w-2xl">
      <p className="text-gray-700 leading-relaxed mb-4">
        CropYield Kenya is a precision agriculture platform designed to forecast crop production using Machine Learning and satellite imagery from Google Earth Engine.
      </p>
      <p className="text-gray-700 leading-relaxed">
        Version 1.0.0
      </p>
    </div>
  </div>
);
