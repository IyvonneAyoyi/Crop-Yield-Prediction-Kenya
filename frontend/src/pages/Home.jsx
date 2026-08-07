function Home() {
  return (
    <main className="min-h-screen flex items-center justify-center bg-slate-100">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-green-700">
          Crop Yield Prediction System
        </h1>

        <p className="mt-4 text-gray-600">
          Predict county-level crop yield using satellite-derived environmental
          variables and Machine Learning.
        </p>
      </div>
    </main>
  );
}

export default Home;