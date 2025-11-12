const DetectiveStats = ({ humanState, aiState, winner }) => {
  return (
    <div className="bg-white p-6 rounded-2xl shadow-lg mb-5 border-4 border-yellow-400">
      <h2 className="text-2xl font-bold text-center mb-4 text-gray-800">
        📊 Race Statistics
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Human Stats */}
        <div className={`p-6 rounded-xl border-4 ${winner === 'human' ? 'border-green-500 bg-green-50' : 'border-blue-500 bg-blue-50'}`}>
          <h3 className="text-xl font-bold text-blue-800 mb-4 flex items-center gap-2">
            🕵️ Human Detective
            {winner === 'human' && <span className="text-2xl">🏆</span>}
          </h3>
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="font-semibold">💰 Total Cost:</span>
              <span className="text-2xl font-bold text-blue-600">
                {humanState?.total_cost || 0}
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="font-semibold">🔍 Actions:</span>
              <span className="text-2xl font-bold text-blue-600">
                {humanState?.actions_taken?.length || 0}
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="font-semibold">🎯 Solutions Left:</span>
              <span className="text-2xl font-bold text-blue-600">
                {humanState?.possible_solutions || 27}
              </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-4 mt-3">
              <div
                className="bg-blue-500 h-4 rounded-full transition-all duration-500"
                style={{
                  width: `${humanState ? ((27 - (humanState.possible_solutions || 27)) / 27) * 100 : 0}%`
                }}
              ></div>
            </div>
          </div>
        </div>

        {/* AI Stats */}
        <div className={`p-6 rounded-xl border-4 ${winner === 'ai' ? 'border-green-500 bg-green-50' : 'border-purple-500 bg-purple-50'}`}>
          <h3 className="text-xl font-bold text-purple-800 mb-4 flex items-center gap-2">
            🤖 AI Detective
            {winner === 'ai' && <span className="text-2xl">🏆</span>}
          </h3>
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="font-semibold">💰 Total Cost:</span>
              <span className="text-2xl font-bold text-purple-600">
                {aiState?.total_cost || 0}
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="font-semibold">🔍 Actions:</span>
              <span className="text-2xl font-bold text-purple-600">
                {aiState?.actions_taken || 0}
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="font-semibold">🎯 Solutions Left:</span>
              <span className="text-2xl font-bold text-purple-600">
                {aiState?.possible_solutions || 27}
              </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-4 mt-3">
              <div
                className="bg-purple-500 h-4 rounded-full transition-all duration-500"
                style={{
                  width: `${aiState ? ((27 - (aiState.possible_solutions || 27)) / 27) * 100 : 0}%`
                }}
              ></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DetectiveStats;
