function EnvironmentalVariables({ variables }) {
  if (!variables) return null;

  return (
    <div className="bg-white rounded-xl shadow-md p-6 mt-6">
      <h2 className="text-2xl font-semibold text-green-700 mb-4">
        Environmental Variables
      </h2>

      <div className="space-y-3">
        {Object.entries(variables).map(([name, data]) => (
          <div
            key={name}
            className="flex justify-between items-center border-b pb-2 last:border-b-0"
          >
            <span className="font-medium text-gray-700">
              {name.replace(/_/g, " ")}
            </span>

            <span className="font-semibold text-gray-900">
              {data.value} {data.unit}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

export default EnvironmentalVariables;