import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Dashboard = () => {
  const [crops, setCrops] = useState([]);
  const [counties, setCounties] = useState([]);
  const [selectedCrop, setSelectedCrop] = useState('Maize');
  const [selectedCounty, setSelectedCounty] = useState('Uasin Gishu');
  const [predictionData, setPredictionData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Fetch initial data for crops and counties
    const fetchInitialData = async () => {
      try {
        const cropsRes = await axios.get('http://127.0.0.1:8000/crops');
        const countiesRes = await axios.get('http://127.0.0.1:8000/counties');
        setCrops(cropsRes.data.crops);
        setCounties(countiesRes.data.counties);
      } catch (err) {
        console.error("Error fetching initial data", err);
      }
    };
    fetchInitialData();
  }, []);

  const handlePredict = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post('http://127.0.0.1:8000/predict', {
        crop: selectedCrop,
        county: selectedCounty,
        start_date: '2022-01-01',
        end_date: '2022-12-31'
      });
      setPredictionData(response.data);
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || "An error occurred during prediction.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-8 font-manrope">
      <div className="mb-8 flex justify-between items-end">
        <div>
          <p className="text-sm text-gray-500 font-inter uppercase tracking-wider mb-1">{selectedCounty} • KENYA</p>
          <h2 className="text-3xl font-bold text-on-background">{selectedCounty} County Insights</h2>
        </div>
        <button 
          onClick={handlePredict}
          className="bg-primary-container text-white px-6 py-2 rounded-md hover:bg-primary transition-colors flex items-center space-x-2"
        >
          {loading ? 'Predicting...' : 'Run Prediction'}
        </button>
      </div>

      {error && (
        <div className="bg-error-container text-on-error-container p-4 rounded-md mb-8">
          {error}
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm">
          <p className="text-xs text-gray-500 font-inter font-semibold uppercase mb-2">Predicted Yield</p>
          <p className="text-3xl font-bold text-on-background">
            {predictionData ? predictionData.predicted_yield.value : '--'}
            <span className="text-sm font-normal text-gray-500 ml-1">
              {predictionData ? predictionData.predicted_yield.unit : ''}
            </span>
          </p>
        </div>

        <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm">
          <p className="text-xs text-gray-500 font-inter font-semibold uppercase mb-2">Crop</p>
          <select 
            className="w-full text-xl font-bold text-primary bg-transparent outline-none cursor-pointer"
            value={selectedCrop}
            onChange={(e) => setSelectedCrop(e.target.value)}
          >
            {crops.map(c => <option key={c} value={c}>{c}</option>)}
          </select>
        </div>

        <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm">
          <p className="text-xs text-gray-500 font-inter font-semibold uppercase mb-2">County</p>
          <select 
            className="w-full text-xl font-bold text-on-background bg-transparent outline-none cursor-pointer"
            value={selectedCounty}
            onChange={(e) => setSelectedCounty(e.target.value)}
          >
            {counties.map(c => <option key={c} value={c}>{c}</option>)}
          </select>
        </div>
      </div>

      {predictionData && (
        <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm mb-8">
          <h3 className="text-lg font-semibold mb-4 border-b pb-2">Environmental Data (2022)</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {Object.entries(predictionData.environmental_variables).map(([key, data]) => (
              <div key={key} className="p-4 bg-surface-container rounded-md">
                <p className="text-xs text-gray-500 uppercase font-inter">{key.replace(/_/g, ' ')}</p>
                <p className="text-xl font-semibold mt-1">
                  {data.value} <span className="text-sm text-gray-500">{data.unit}</span>
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="bg-primary-container text-white p-6 rounded-lg">
        <div className="flex items-center space-x-2 mb-2">
          <span className="w-2 h-2 bg-secondary-fixed rounded-full"></span>
          <p className="text-xs uppercase font-inter text-primary-fixed-dim">Agricultural Insight</p>
        </div>
        <h3 className="text-xl font-bold mb-2">Prediction Model Ready</h3>
        <p className="text-sm text-gray-300 max-w-2xl">
          The Random Forest Regressor is standing by. Select a crop and county above, and click 'Run Prediction' to fetch historical environmental data from Google Earth Engine and estimate the crop yield.
        </p>
      </div>

    </div>
  );
};

export default Dashboard;
