const ResultModal = ({ isOpen, onClose, result, humanState, aiState }) => {
  if (!isOpen || !result) return null;

  return (
    <div
      className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50 animate-fadeIn"
      onClick={onClose}
    >
      <div
        className="bg-white p-10 rounded-2xl shadow-2xl max-w-md text-center animate-slideUp relative"
        onClick={(e) => e.stopPropagation()}
      >
        <button
          onClick={onClose}
          className="absolute right-5 top-4 text-3xl text-gray-400 hover:text-black"
        >
          &times;
        </button>
        {result.winner === "AI Detective" ? (
          <>
            <div className="text-purple-600 text-4xl mb-5">🤖 AI WINS!</div>
            <h2 className="text-2xl font-bold mb-5">
              AI Detective Solved It First!
            </h2>
            <p className="text-lg mb-5">
              It was <strong>{result.solution.suspect}</strong> with the{" "}
              <strong>{result.solution.weapon}</strong> in the{" "}
              <strong>{result.solution.location}</strong>!
            </p>
            <p className="text-gray-600 mb-5">
              AI Cost: {aiState?.total_cost || 0} | AI Actions:{" "}
              {aiState?.actions_taken || 0}
            </p>
            <button
              onClick={() => window.location.reload()}
              className="bg-purple-500 text-white px-6 py-3 rounded-lg font-semibold hover:bg-purple-600"
            >
              Play Again
            </button>
          </>
        ) : result.correct ? (
          <>
            <div className="text-green-600 text-4xl mb-5">🎉 YOU WIN!</div>
            <h2 className="text-2xl font-bold mb-5">Case Solved!</h2>
            <p className="text-lg mb-5">
              It was <strong>{result.solution.suspect}</strong> with the{" "}
              <strong>{result.solution.weapon}</strong> in the{" "}
              <strong>{result.solution.location}</strong>!
            </p>
            <p className="text-gray-600 mb-5">
              Your Cost: {humanState?.total_cost || 0} | Your Actions:{" "}
              {humanState?.actions_taken?.length || 0}
            </p>
            <button
              onClick={() => window.location.reload()}
              className="bg-blue-500 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-600"
            >
              Play Again
            </button>
          </>
        ) : (
          <>
            <div className="text-red-600 text-4xl mb-5">❌ INCORRECT!</div>
            <h2 className="text-2xl font-bold mb-5">Wrong Accusation</h2>
            <p className="mb-5">Keep investigating to find more evidence!</p>
            <button
              onClick={onClose}
              className="bg-blue-500 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-600"
            >
              Continue Investigation
            </button>
          </>
        )}
      </div>
    </div>
  );
};

export default ResultModal;