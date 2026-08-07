import PredictionForm from "../components/PredictionForm";

function Home() {
  return (
    <main className="min-h-screen bg-slate-100 py-10">
      <div className="max-w-5xl mx-auto px-6">

        <div className="text-center mb-10">
          <h1 className="text-4xl font-bold text-green-700">
            Crop Yield Prediction System
          </h1>

          <p className="mt-3 text-gray-600">
            Predict county-level crop yield using satellite-derived
            environmental variables and Machine Learning.
          </p>
        </div>

        <PredictionForm />

      </div>
    </main>
  );
}

export default Home;