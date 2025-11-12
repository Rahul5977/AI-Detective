import React, { useState } from "react";
import Header from "./components/Header";
import GameControls from "./components/GameControls";
import DetectiveStats from "./components/DetectiveStats";
import AvailableActions from "./components/AvailableActions";
import CurrentDomains from "./components/CurrentDomains";
import InvestigationHistory from "./components/InvestigationHistory";
import AIDetectivePanel from "./components/AIDetectivePanel";
import AccusationPanel from "./components/AccusationPanel";
import ResultModal from "./components/ResultModal";
import AlgorithmVisualization from "./components/AlgorithmVisualization";
import { gameService, aiService } from "./services/api";

function App() {
  const [sessionId] = useState("user-session-" + Date.now());
  const [gameState, setGameState] = useState(null);
  const [availableActions, setAvailableActions] = useState([]);
  const [humanHistory, setHumanHistory] = useState([]);
  const [aiHistory, setAIHistory] = useState([]);
  const [aiProgress, setAIProgress] = useState(null);
  const [algorithmSteps, setAlgorithmSteps] = useState([]);
  const [modalResult, setModalResult] = useState(null);
  const [gameStarted, setGameStarted] = useState(false);
  const [raceMode, setRaceMode] = useState(true);
  const [winner, setWinner] = useState(null);

  const handleStartGame = async () => {
    try {
      const data = await gameService.startGame(sessionId);
      if (data.success) {
        setGameState(data.game_state);
        setAvailableActions(data.available_actions);
        setHumanHistory([]);
        setAIHistory([]);
        setAIProgress(null);
        setAlgorithmSteps([]);
        setGameStarted(true);
        setWinner(null);
      }
    } catch (error) {
      console.error("Error starting game:", error);
      alert("Failed to start game. Make sure the backend is running on port 5002.");
    }
  };

  const handleTakeAction = async (evidenceId) => {
    try {
      const data = await gameService.takeAction(sessionId, evidenceId);
      if (data.success) {
        setGameState(data.game_state);
        setAvailableActions(data.available_actions);
        setHumanHistory((prev) => [data.evidence, ...prev]);
        setAlgorithmSteps(data.csp_result?.steps || []);
      }
    } catch (error) {
      console.error("Error taking action:", error);
    }
  };

  const handleAIMakeMove = async () => {
    try {
      const data = await aiService.makeAIMove(sessionId);
      if (data.success) {
        setAIProgress(data.ai_state);
        setAIHistory((prev) => [data.action_taken, ...prev]);
        setAlgorithmSteps(data.algorithm_explanation || []);
        
        // Check if AI solved it
        if (data.ai_state.solved) {
          setWinner('ai');
          setTimeout(() => {
            setModalResult({
              correct: false,
              winner: 'AI Detective',
              solution: data.ai_state.solution,
              message: 'The AI Detective solved the case first!'
            });
          }, 500);
        }
      }
    } catch (error) {
      console.error("Error making AI move:", error);
    }
  };

  const handleMakeAccusation = async (guess) => {
    try {
      const data = await gameService.makeAccusation(sessionId, guess);
      if (data.success) {
        if (data.correct) {
          setWinner('human');
        }
        setModalResult({
          ...data,
          winner: data.correct ? 'Human Detective' : null
        });
      }
    } catch (error) {
      console.error("Error making accusation:", error);
    }
  };

  const handleAutoSolve = async () => {
    try {
      const data = await aiService.autoSolve(sessionId);
      if (data.success) {
        setAlgorithmSteps(data.solution_path || []);
        setWinner('ai');
        setTimeout(() => {
          setModalResult({
            correct: false,
            winner: 'AI Detective',
            solution: data.solution,
            message: `AI auto-solved in ${data.steps_taken} steps with cost ${data.total_cost}`
          });
        }, 500);
      }
    } catch (error) {
      console.error("Error auto-solving:", error);
      alert("Failed to auto-solve. Please check the backend.");
    }
  };

  return (
    <div className="min-h-screen bg-linear-to-br from-purple-500 to-purple-800 p-5">
      <div className="max-w-[1600px] mx-auto">
        <Header raceMode={raceMode} winner={winner} />
        <GameControls
          onStartGame={handleStartGame}
          onAIMakeMove={handleAIMakeMove}
          onAutoSolve={handleAutoSolve}
          gameStarted={gameStarted}
          winner={winner}
        />
        
        {gameStarted && (
          <DetectiveStats 
            humanState={gameState} 
            aiState={aiProgress}
            winner={winner}
          />
        )}

        <div className="grid grid-cols-1 xl:grid-cols-2 gap-5 mb-5">
          {/* Human Detective Side */}
          <div className="space-y-5">
            <div className="bg-blue-100 border-4 border-blue-500 rounded-2xl p-4">
              <h2 className="text-2xl font-bold text-blue-800 mb-3 flex items-center gap-2">
                🕵️ Human Detective (You)
              </h2>
              <AvailableActions
                actions={availableActions}
                onTakeAction={handleTakeAction}
                disabled={!!winner}
              />
              <div className="mt-5">
                <CurrentDomains 
                  domains={gameState?.current_domains}
                  title="Your Deductions"
                />
              </div>
              <div className="mt-5">
                <InvestigationHistory 
                  history={humanHistory}
                  title="Your Investigation"
                  color="blue"
                />
              </div>
            </div>
          </div>

          {/* AI Detective Side */}
          <div className="space-y-5">
            <div className="bg-purple-100 border-4 border-purple-500 rounded-2xl p-4">
              <h2 className="text-2xl font-bold text-purple-800 mb-3 flex items-center gap-2">
                🤖 AI Detective (Assistant)
              </h2>
              <AIDetectivePanel
                aiState={aiProgress}
                aiHistory={aiHistory}
                onMakeMove={handleAIMakeMove}
                disabled={!!winner}
              />
            </div>
          </div>
        </div>

        {/* Algorithm Visualization */}
        {algorithmSteps.length > 0 && (
          <AlgorithmVisualization steps={algorithmSteps} />
        )}

        {/* Accusation Panel */}
        {gameStarted && !winner && (
          <AccusationPanel onMakeAccusation={handleMakeAccusation} />
        )}

        <ResultModal
          isOpen={!!modalResult}
          onClose={() => setModalResult(null)}
          result={modalResult}
          humanState={gameState}
          aiState={aiProgress}
        />
      </div>
    </div>
  );
}

export default App;