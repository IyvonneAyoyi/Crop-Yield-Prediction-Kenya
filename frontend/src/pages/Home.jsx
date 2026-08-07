import { useState } from "react";

import PredictionForm from "../components/PredictionForm";
import { predictYield } from "../services/api";
import PredictionResult from "../components/PredictionResult";
import EnvironmentalVariables from "../components/EnvironmentalVariables";

function Home() {
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handlePrediction(formData) {
    try {
      setLoading(true);
      setError("");
      setPrediction(null);

      const result = await predictYield(formData);

      setPrediction(result);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Prediction failed. Please try again."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-slate-100 py-12 px-4">
      <div className="max-w-4xl mx-auto">
        {/* Page Header */}
        <div className="text-center mb-10">
          <h1 className="text-4xl font-bold text-green-700">
            Crop Yield Prediction System
          </h1>

          <p className="mt-3 text-gray-600">
            Predict county-level crop yield using satellite-derived
            environmental variables and Machine Learning.
          </p>
        </div>

        {/* Prediction Form */}
        <PredictionForm onSubmit={handlePrediction} />

        {/* Loading */}
        {loading && (
          <p className="mt-6 text-center text-blue-600 font-medium">
            Predicting...
          </p>
        )}

        {/* Error */}
        {error && (
          <div className="mt-6 rounded-lg bg-red-100 border border-red-300 p-4 text-red-700">
            {error}
          </div>
        )}

    {/* Prediction Results */}
    {prediction && (
      <div className="mt-8 space-y-6">
        <PredictionResult
          prediction={prediction.predicted_yield}
        />

        <EnvironmentalVariables
          variables={prediction.environmental_variables}
        />
      </div>
    )}
      </div>
    </main>
  );
}

export default Home;