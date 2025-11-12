const GameControls = ({ onStartGame, onAIMakeMove, onAutoSolve, gameStarted, winner }) => {
  return (
    <div className="flex gap-4 justify-center mb-5 flex-wrap">
      <button
        onClick={onStartGame}
        className="px-8 py-4 bg-green-500 text-white rounded-xl font-bold text-lg shadow-lg hover:bg-green-600 hover:-translate-y-1 hover:shadow-xl transition-all duration-300"
      >
        🎮 Start New Race
      </button>
      <button
        onClick={onAIMakeMove}
        disabled={!gameStarted || !!winner}
        className="px-8 py-4 bg-purple-500 text-white rounded-xl font-bold text-lg shadow-lg hover:bg-purple-600 hover:-translate-y-1 hover:shadow-xl transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        🤖 AI Make Move
      </button>
      <button
        onClick={onAutoSolve}
        disabled={!gameStarted || !!winner}
        className="px-8 py-4 bg-orange-500 text-white rounded-xl font-bold text-lg shadow-lg hover:bg-orange-600 hover:-translate-y-1 hover:shadow-xl transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        ⚡ Watch AI Auto-Solve
      </button>
    </div>
  );
};

export default GameControls;