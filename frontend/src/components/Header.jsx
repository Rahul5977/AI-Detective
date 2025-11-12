const Header = ({ raceMode, winner }) => {
  return (
    <header className="bg-white p-8 rounded-2xl shadow-lg mb-5 text-center border-4 border-yellow-400">
      <h1 className="text-5xl font-bold text-gray-800 mb-2">
        🕵️‍♂️ AI vs Human Detective Challenge 🤖
      </h1>
      <p className="text-gray-600 text-xl mb-2">Who can solve the mystery faster?</p>
      <div className="flex justify-center gap-8 mt-4">
        <div className="flex items-center gap-2">
          <span className="text-2xl">🧠</span>
          <span className="font-semibold text-blue-600">Human Intuition</span>
        </div>
        <div className="text-3xl font-bold text-yellow-500">VS</div>
        <div className="flex items-center gap-2">
          <span className="text-2xl">⚙️</span>
          <span className="font-semibold text-purple-600">AI Algorithms</span>
        </div>
      </div>
      {winner && (
        <div className="mt-4 p-4 bg-yellow-100 rounded-xl border-2 border-yellow-500">
          <p className="text-2xl font-bold text-yellow-800">
            🏆 Winner: {winner === 'human' ? 'Human Detective!' : 'AI Detective!'}
          </p>
        </div>
      )}
    </header>
  );
};

export default Header;
