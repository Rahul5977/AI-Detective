const AlgorithmVisualization = ({ steps }) => {
  if (!steps || steps.length === 0) return null;

  return (
    <div className="bg-white p-6 rounded-2xl shadow-lg mb-5 border-4 border-indigo-400">
      <h2 className="text-2xl font-bold text-indigo-800 mb-4 flex items-center gap-2">
        🔬 Algorithm Execution Trace
      </h2>
      <p className="text-gray-600 mb-4">
        Watch how the algorithms work in real-time:
      </p>
      <div className="space-y-3 max-h-96 overflow-y-auto">
        {steps.map((step, idx) => (
          <div
            key={idx}
            className={`p-4 rounded-lg border-l-4 animate-slideIn ${
              step.type === 'elimination'
                ? 'bg-red-50 border-red-500'
                : step.type === 'confirmation'
                ? 'bg-green-50 border-green-500'
                : step.type === 'search'
                ? 'bg-blue-50 border-blue-500'
                : 'bg-gray-50 border-gray-400'
            }`}
            style={{ animationDelay: `${idx * 0.1}s` }}
          >
            <div className="flex items-start gap-3">
              <span className="text-2xl">
                {step.type === 'elimination' ? '❌' : 
                 step.type === 'confirmation' ? '✅' : 
                 step.type === 'search' ? '🔍' : '📝'}
              </span>
              <div className="flex-1">
                <div className="font-semibold text-gray-800 mb-1">
                  Step {idx + 1}: {step.algorithm || 'CSP'}
                </div>
                <div className="text-sm text-gray-700">{step.message || step.description}</div>
                {step.details && (
                  <div className="mt-2 text-xs text-gray-600 bg-white p-2 rounded">
                    {step.details}
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default AlgorithmVisualization;
