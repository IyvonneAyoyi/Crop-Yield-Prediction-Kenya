function PredictionResult({ prediction }) {
  if (!prediction) return null;

  return (
    <div className="bg-white rounded-xl shadow-md p-6 mt-8">
      <h2 className="text-2xl font-semibold text-green-700 mb-4">
        Predicted Yield
      </h2>

      <div className="text-center">
       <p className="text-5xl font-bold text-green-700">
  {prediction.value.toFixed(3)}
  <span className="ml-2 text-2xl font-medium text-gray-600">
    {prediction.unit}
  </span>
</p>
      </div>
    </div>
  );
}

export default PredictionResult;