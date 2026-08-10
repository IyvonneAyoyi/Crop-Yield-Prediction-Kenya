function Header() {
  return (
    <div className="text-center mb-10">
      <h1 className="text-4xl font-bold text-green-700">
        Crop Yield Prediction System
      </h1>

      <p className="mt-3 text-gray-600 max-w-2xl mx-auto">
        Predict county-level crop yield using satellite-derived
        environmental variables and Machine Learning.
      </p>
    </div>
  );
}

export default Header;