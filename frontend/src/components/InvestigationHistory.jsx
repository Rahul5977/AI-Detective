const InvestigationHistory = ({ history, title = "Investigation History", color = "blue" }) => {
  const colorClasses = {
    blue: 'border-blue-500 bg-blue-50',
    purple: 'border-purple-500 bg-purple-50'
  };

  return (
    <div className="bg-white p-6 rounded-xl shadow-md">
      <h2 className="text-xl font-bold text-gray-800 mb-4">
        📜 {title}
      </h2>
      <div className="flex flex-col gap-3 max-h-96 overflow-y-auto">
        {history.length === 0 ? (
          <p className="text-center text-gray-400 italic p-5">No actions taken yet</p>
        ) : (
          history.map((item, idx) => (
            <div
              key={idx}
              className={`${colorClasses[color]} p-3 rounded-lg border-l-4 animate-slideIn`}
            >
              <div className="font-semibold text-gray-800 mb-1 text-sm">
                🔍 {item.action}
              </div>
              <div className="text-gray-600 text-xs italic">"{item.clue}"</div>
              <div className="mt-2 text-xs text-orange-600">💰 Cost: {item.cost}</div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default InvestigationHistory;