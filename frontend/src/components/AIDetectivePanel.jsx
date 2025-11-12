const AIDetectivePanel = ({ aiState, aiHistory, onMakeMove, disabled }) => {
  return (
    <div className="space-y-4">
      {/* AI Status */}
      {aiState ? (
        <div className="bg-white p-4 rounded-xl shadow-md">
          <h3 className="font-bold text-lg mb-3 text-purple-800">
            🧠 AI's Current Strategy
          </h3>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span className="font-semibold">Algorithm:</span>
              <span className="text-purple-600">{aiState.algorithm || 'A* Search + CSP'}</span>
            </div>
            <div className="flex justify-between">
              <span className="font-semibold">Confidence:</span>
              <span className="text-purple-600">
                {aiState.confidence ? `${(aiState.confidence * 100).toFixed(1)}%` : 'Analyzing...'}
              </span>
            </div>
            {aiState.next_best_action && (
              <div className="mt-3 p-3 bg-purple-50 rounded-lg border-2 border-purple-300">
                <p className="font-semibold text-purple-800 mb-1">Next Move:</p>
                <p className="text-sm">{aiState.next_best_action}</p>
              </div>
            )}
          </div>
        </div>
      ) : (
        <div className="bg-white p-6 rounded-xl text-center text-gray-400">
          <p>AI is ready to start investigating...</p>
          <button
            onClick={onMakeMove}
            disabled={disabled}
            className="mt-4 px-6 py-3 bg-purple-500 text-white rounded-lg font-semibold hover:bg-purple-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            🤖 Let AI Start
          </button>
        </div>
      )}

      {/* AI Deductions */}
      {aiState?.current_domains && (
        <div className="bg-white p-4 rounded-xl shadow-md">
          <h3 className="font-bold text-lg mb-3 text-purple-800">
            🎯 AI's Deductions
          </h3>
          <div className="space-y-3">
            {Object.entries(aiState.current_domains).map(([category, values]) => (
              <div key={category} className="bg-purple-50 p-3 rounded-lg">
                <div className="font-semibold text-purple-800 mb-2 capitalize">
                  {category}:
                </div>
                <div className="flex flex-wrap gap-2">
                  {values.map((val, idx) => (
                    <span
                      key={idx}
                      className={`px-3 py-1 rounded-full text-sm font-medium ${
                        values.length === 1
                          ? 'bg-green-500 text-white'
                          : 'bg-white text-purple-600 border-2 border-purple-400'
                      }`}
                    >
                      {val}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* AI Investigation History */}
      {aiHistory.length > 0 && (
        <div className="bg-white p-4 rounded-xl shadow-md">
          <h3 className="font-bold text-lg mb-3 text-purple-800">
            📜 AI's Investigation Log
          </h3>
          <div className="space-y-2 max-h-80 overflow-y-auto">
            {aiHistory.map((item, idx) => (
              <div
                key={idx}
                className="bg-purple-50 p-3 rounded-lg border-l-4 border-purple-500 text-sm"
              >
                <div className="font-semibold text-purple-800">
                  Step {aiHistory.length - idx}: {item.action}
                </div>
                <div className="text-gray-600 text-xs mt-1">
                  Reasoning: {item.reasoning || 'Optimal path selected by A*'}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default AIDetectivePanel;
