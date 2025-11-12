const CurrentDomains = ({ domains, title = "🧩 Current CSP Domains" }) => {
  if (!domains) {
    return (
      <div className="bg-white p-6 rounded-xl shadow-md">
        <h2 className="text-xl font-bold text-gray-800 mb-4">{title}</h2>
        <p className="text-center text-gray-400 italic p-5">No active game</p>
      </div>
    );
  }

  const isSolved = Object.values(domains).every((vals) => vals.length === 1);

  return (
    <div className="bg-white p-6 rounded-xl shadow-md">
      <h2 className="text-xl font-bold text-gray-800 mb-4">{title}</h2>
      <div className="flex flex-col gap-4">
        {Object.entries(domains).map(([category, values]) => (
          <div
            key={category}
            className="bg-gray-50 p-4 rounded-xl border-l-4 border-green-500"
          >
            <div className="font-semibold text-gray-800 mb-2 text-lg capitalize">
              {category}
            </div>
            <div className="flex flex-wrap gap-2">
              {values.map((val, idx) => (
                <span
                  key={idx}
                  className={`px-4 py-1.5 rounded-full border-2 font-medium text-sm ${
                    values.length === 1
                      ? "bg-green-500 text-white border-green-500 animate-pulse"
                      : "bg-white text-blue-500 border-blue-500"
                  }`}
                >
                  {val}
                </span>
              ))}
            </div>
          </div>
        ))}
        {isSolved && (
          <div className="text-center mt-5 p-5 bg-green-100 rounded-xl text-green-800">
            <h3 className="text-xl font-bold mb-2">🎉 Mystery Solved!</h3>
            <p>All domains narrowed to single values. Make your accusation!</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default CurrentDomains;