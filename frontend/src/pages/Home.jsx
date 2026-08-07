import { useState } from "react";

import PredictionForm from "../components/PredictionForm";
import { predictYield } from "../services/api";
import Header from "../components/Header";
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
        <Header />

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