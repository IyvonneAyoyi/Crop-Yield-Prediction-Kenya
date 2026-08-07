import { useState } from "react";

import PredictionForm from "../components/PredictionForm";
import { predictYield } from "../services/api";

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

        {/* Temporary Prediction Output */}
        {prediction && (
          <div className="mt-8 bg-white rounded-xl shadow p-6">
            <h2 className="text-2xl font-semibold mb-4">
              Prediction Response
            </h2>

            <pre className="overflow-x-auto text-sm">
              {JSON.stringify(prediction, null, 2)}
            </pre>
          </div>
        )}
      </div>
    </main>
  );
}

export default Home;