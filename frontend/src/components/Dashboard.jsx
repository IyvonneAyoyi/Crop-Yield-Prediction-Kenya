import { useState, useEffect } from "react";
import {
  getCrops,
  getCounties,
  predictYield,
} from "../services/api";

const Dashboard = () => {
  const [crops, setCrops] = useState([]);
  const [counties, setCounties] = useState([]);
  const [selectedCrop, setSelectedCrop] = useState("Maize");
  const [selectedCounty, setSelectedCounty] = useState("Uasin Gishu");
  const [selectedYear, setSelectedYear] = useState("2022");
  const [predictionData, setPredictionData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchInitialData = async () => {
      try {
        const [cropsData, countiesData] = await Promise.all([
          getCrops(),
          getCounties(),
        ]);

        setCrops(cropsData);
        setCounties(countiesData);
      } catch (err) {
        console.error("Error fetching initial data - Dashboard.jsx:28", err);
        setError("Unable to load crops and counties.");
      }
    };

    fetchInitialData();
  }, []);

  const handlePredict = async () => {
    setLoading(true);
    setError(null);

    try {
      const data = await predictYield({
        crop: selectedCrop,
        county: selectedCounty,
        start_date: `${selectedYear}-01-01`,
        end_date: `${selectedYear}-12-31`,
      });

      setPredictionData(data);
    } catch (err) {
      console.error(err);
      setError(
        err.response?.data?.detail ||
        "An error occurred during prediction."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="mb-8">
        <p className="text-sm text-gray-500">
          {selectedCounty} • KENYA
        </p>

        <h2 className="text-2xl font-bold">
          {selectedCounty} County Insights
        </h2>
      </div>

      {error && (
        <div className="bg-error-container text-on-error-container p-4 rounded-md mb-8">
          {error}
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm">
          <p className="text-xs text-gray-500 font-inter font-semibold uppercase mb-2">
            Predicted Yield
          </p>

          <p className="text-3xl font-bold text-on-background">
            {predictionData
              ? predictionData.predicted_yield.value
              : "--"}

            <span className="text-sm font-normal text-gray-500 ml-1">
              {predictionData
                ? predictionData.predicted_yield.unit
                : ""}
            </span>
          </p>
        </div>

        <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm">
          <p className="text-xs text-gray-500 font-inter font-semibold uppercase mb-2">
            Crop
          </p>

          <select
            className="w-full text-xl font-bold text-primary bg-transparent outline-none cursor-pointer"
            value={selectedCrop}
            onChange={(e) => setSelectedCrop(e.target.value)}
          >
            {crops.map((crop) => (
              <option key={crop} value={crop}>
                {crop}
              </option>
            ))}
          </select>
        </div>

        <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm">
          <p className="text-xs text-gray-500 font-inter font-semibold uppercase mb-2">
            County
          </p>

          <select
            className="w-full text-xl font-bold text-on-background bg-transparent outline-none cursor-pointer"
            value={selectedCounty}
            onChange={(e) => setSelectedCounty(e.target.value)}
          >
            {counties.map((county) => (
              <option key={county} value={county}>
                {county}
              </option>
            ))}
          </select>
        </div>

        <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm">
          <p className="text-xs text-gray-500 font-inter font-semibold uppercase mb-2">
            Year
          </p>

          <select
            className="w-full text-xl font-bold text-on-background bg-transparent outline-none cursor-pointer"
            value={selectedYear}
            onChange={(e) => setSelectedYear(e.target.value)}
          >
            {[2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027].map((year) => (
              <option key={year} value={year}>
                {year}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="flex justify-end mb-8">
        <button
          onClick={handlePredict}
          disabled={loading}
          className="bg-primary hover:opacity-90 text-white font-bold py-3 px-8 rounded-full shadow-md transition duration-200 ease-in-out disabled:opacity-50"
        >
          {loading ? "Predicting..." : "Run Prediction"}
        </button>
      </div>

      {predictionData && (
        <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm mb-8">
          <h3 className="text-lg font-semibold mb-4 border-b pb-2">
            Environmental Data ({selectedYear})
          </h3>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {Object.entries(
              predictionData.environmental_variables
            ).map(([key, data]) => (
              <div
                key={key}
                className="p-4 bg-surface-container rounded-md"
              >
                <p className="text-xs text-gray-500 uppercase font-inter">
                  {key.replace(/_/g, " ")}
                </p>

                <p className="text-xl font-semibold mt-1">
                  {data.value}{" "}
                  <span className="text-sm text-gray-500">
                    {data.unit}
                  </span>
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="bg-primary-container text-white p-6 rounded-lg">
        <div className="flex items-center space-x-2 mb-2">
          <span className="w-2 h-2 bg-secondary-fixed rounded-full"></span>

          <p className="text-xs uppercase font-inter text-primary-fixed-dim">
            Agricultural Insight
          </p>
        </div>

        <h3 className="text-xl font-bold mb-2">
          Prediction Model Ready
        </h3>
      </div>
    </div>
  );
};

export default Dashboard;
