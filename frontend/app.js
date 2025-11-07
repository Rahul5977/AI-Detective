// API Configuration
const API_URL = "http://localhost:5002/api";

// Game State
let sessionId = "user-session-" + Date.now();
let gameState = null;

// DOM Elements
const startGameBtn = document.getElementById("startGame");
const aiSuggestBtn = document.getElementById("aiSuggest");
const minimaxSuggestBtn = document.getElementById("minimaxSuggest");
const gameStatusDiv = document.getElementById("gameStatus");
const availableActionsDiv = document.getElementById("availableActions");
const currentDomainsDiv = document.getElementById("currentDomains");
const investigationHistoryDiv = document.getElementById("investigationHistory");
const accusationPanelDiv = document.getElementById("accusationPanel");
const makeAccusationBtn = document.getElementById("makeAccusation");
const resultModal = document.getElementById("resultModal");
const resultContent = document.getElementById("resultContent");
const aiSuggestionPanel = document.getElementById("aiSuggestionPanel");
const aiSuggestionDiv = document.getElementById("aiSuggestion");
const minimaxPanel = document.getElementById("minimaxPanel");
const minimaxSuggestionDiv = document.getElementById("minimaxSuggestion");
const cspVisualizationDiv = document.getElementById("cspVisualization");
const cspStepsDiv = document.getElementById("cspSteps");

// Event Listeners
startGameBtn.addEventListener("click", startNewGame);
aiSuggestBtn.addEventListener("click", getAISuggestion);
minimaxSuggestBtn.addEventListener("click", getMinimaxSuggestion);
makeAccusationBtn.addEventListener("click", makeAccusation);
document.querySelector(".close").addEventListener("click", () => {
  resultModal.classList.remove("show");
});

// API Functions
async function startNewGame() {
  try {
    showLoading(availableActionsDiv);
    const response = await fetch(`${API_URL}/game/start`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ session_id: sessionId }),
    });

    const data = await response.json();
    if (data.success) {
      gameState = data.game_state;
      updateUI(data);
      aiSuggestBtn.disabled = false;
      minimaxSuggestBtn.disabled = false;
      gameStatusDiv.classList.remove("hidden");
      accusationPanelDiv.classList.remove("hidden");
      populateAccusationForm();
      showNotification("Game started! Begin your investigation.", "success");
    }
  } catch (error) {
    console.error("Error starting game:", error);
    showNotification(
      "Failed to start game. Make sure the backend is running on port 5001.",
      "error"
    );
  }
}

async function takeAction(evidenceId) {
  try {
    const response = await fetch(`${API_URL}/game/action`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        session_id: sessionId,
        evidence_id: evidenceId,
      }),
    });

    const data = await response.json();
    if (data.success) {
      gameState = data.game_state;
      updateUI(data);
      updateCSPVisualization(data.csp_result.steps);
      showNotification(
        `Evidence discovered: ${data.evidence.action}`,
        "success"
      );

      // Check if solved
      if (gameState.possible_solutions === 1) {
        showNotification("🎉 You can now make your accusation!", "success");
      }
    }
  } catch (error) {
    console.error("Error taking action:", error);
    showNotification("Failed to take action.", "error");
  }
}

async function getAISuggestion() {
  try {
    const response = await fetch(`${API_URL}/ai/suggest`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ session_id: sessionId }),
    });

    const data = await response.json();
    if (data.success) {
      displayAISuggestion(data.suggestion, data.all_evaluations);
      aiSuggestionPanel.classList.remove("hidden");
      showNotification("AI suggestion generated using A* search!", "success");
    } else {
      showNotification(data.message, "info");
    }
  } catch (error) {
    console.error("Error getting AI suggestion:", error);
    showNotification("Failed to get AI suggestion.", "error");
  }
}

async function getMinimaxSuggestion() {
  try {
    const response = await fetch(`${API_URL}/ai/minimax`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    });

    const data = await response.json();
    if (data.success) {
      displayMinimaxSuggestion(
        data.best_question,
        data.all_evaluations,
        data.game_tree
      );
      minimaxPanel.classList.remove("hidden");
      showNotification(
        "Best interrogation question found using Minimax!",
        "success"
      );
    }
  } catch (error) {
    console.error("Error getting Minimax suggestion:", error);
    showNotification("Failed to get Minimax suggestion.", "error");
  }
}

async function makeAccusation() {
  const suspect = document.getElementById("accuseSuspect").value;
  const weapon = document.getElementById("accuseWeapon").value;
  const location = document.getElementById("accuseLocation").value;

  if (!suspect || !weapon || !location) {
    showNotification("Please select all three options!", "error");
    return;
  }

  try {
    const response = await fetch(`${API_URL}/game/accuse`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        session_id: sessionId,
        guess: { suspect, weapon, location },
      }),
    });

    const data = await response.json();
    if (data.success) {
      showResult(data.correct, data.solution);
    }
  } catch (error) {
    console.error("Error making accusation:", error);
    showNotification("Failed to make accusation.", "error");
  }
}

// UI Update Functions
function updateUI(data) {
  // Update status
  if (data.game_state) {
    document.getElementById("totalCost").textContent =
      data.game_state.total_cost;
    document.getElementById("actionsTaken").textContent =
      data.game_state.actions_taken.length;
    document.getElementById("possibleSolutions").textContent =
      data.game_state.possible_solutions;
    document.getElementById("constraintsCount").textContent =
      data.game_state.constraints_count;
  }

  // Update available actions
  if (data.available_actions) {
    displayAvailableActions(data.available_actions);
  }

  // Update current domains
  if (data.game_state && data.game_state.current_domains) {
    displayCurrentDomains(data.game_state.current_domains);
  }

  // Update history
  if (data.evidence) {
    addToHistory(data.evidence);
  } else if (data.game_state && data.game_state.actions_taken.length === 0) {
    investigationHistoryDiv.innerHTML =
      '<p class="empty-state">No actions taken yet</p>';
  }
}

function displayAvailableActions(actions) {
  if (actions.length === 0) {
    availableActionsDiv.innerHTML =
      '<p class="empty-state">No more actions available</p>';
    return;
  }

  availableActionsDiv.innerHTML = actions
    .map(
      (action) => `
        <div class="action-item">
            <div class="action-header">
                <span class="action-title">${action.action}</span>
                <span class="action-cost">💰 ${action.cost}</span>
            </div>
            <button class="btn btn-action" onclick="takeAction(${action.id})">
                🔍 Investigate
            </button>
        </div>
    `
    )
    .join("");
}

function displayCurrentDomains(domains) {
  const isSolved = Object.values(domains).every((vals) => vals.length === 1);

  currentDomainsDiv.innerHTML = Object.entries(domains)
    .map(
      ([category, values]) => `
        <div class="domain-item">
            <div class="domain-header">${capitalizeFirst(category)}</div>
            <div class="domain-values">
                ${values
                  .map(
                    (val) => `
                    <span class="domain-value ${
                      values.length === 1 ? "solved" : ""
                    }">${val}</span>
                `
                  )
                  .join("")}
            </div>
        </div>
    `
    )
    .join("");

  if (isSolved) {
    currentDomainsDiv.innerHTML += `
            <div style="text-align: center; margin-top: 20px; padding: 20px; background: #d4edda; border-radius: 10px; color: #155724;">
                <h3>🎉 Mystery Solved!</h3>
                <p>All domains narrowed to single values. Make your accusation!</p>
            </div>
        `;
  }
}

function addToHistory(evidence) {
  if (investigationHistoryDiv.querySelector(".empty-state")) {
    investigationHistoryDiv.innerHTML = "";
  }

  const historyItem = document.createElement("div");
  historyItem.className = "history-item";
  historyItem.innerHTML = `
        <div class="history-action">🔍 ${evidence.action}</div>
        <div class="history-clue">"${evidence.clue}"</div>
        <div style="margin-top: 8px; font-size: 0.85rem; color: #e67e22;">
            💰 Cost: ${evidence.cost}
        </div>
    `;
  investigationHistoryDiv.insertBefore(
    historyItem,
    investigationHistoryDiv.firstChild
  );
}

function displayAISuggestion(suggestion, evaluations) {
  aiSuggestionDiv.innerHTML = `
        <div class="ai-recommendation">
            <h4>🌟 Recommended Action</h4>
            <p><strong>${suggestion.action}</strong></p>
            <p style="margin-top: 10px; color: #7f8c8d; font-size: 0.9rem;">${
              suggestion.explanation
            }</p>
        </div>
        <div style="margin-top: 15px;">
            <h4 style="margin-bottom: 10px;">📊 All Evaluations (A* f-cost)</h4>
            <div class="evaluations-list">
                ${evaluations
                  .map(
                    (ev) => `
                    <div class="evaluation-item">
                        <span>${ev.action}</span>
                        <span class="evaluation-score">f=${ev.f_cost.toFixed(
                          1
                        )}</span>
                    </div>
                `
                  )
                  .join("")}
            </div>
        </div>
    `;
}

function displayMinimaxSuggestion(bestQuestion, evaluations, gameTree) {
  minimaxSuggestionDiv.innerHTML = `
        <div class="ai-recommendation">
            <h4>💡 Best Question</h4>
            <p><strong>${bestQuestion.question}</strong></p>
        </div>
        <div style="margin-top: 15px;">
            <h4 style="margin-bottom: 10px;">📊 All Questions (Expected Utility)</h4>
            <div class="evaluations-list">
                ${evaluations
                  .map(
                    (ev) => `
                    <div class="evaluation-item">
                        <span>${ev.question}</span>
                        <span class="evaluation-score">${ev.expected_utility}</span>
                    </div>
                `
                  )
                  .join("")}
            </div>
        </div>
        <div style="margin-top: 15px;">
            <button class="btn btn-secondary" onclick="askQuestion(${
              bestQuestion.id
            })" style="width: 100%;">
                ❓ Ask This Question
            </button>
        </div>
    `;
}

async function askQuestion(questionId) {
  try {
    const response = await fetch(`${API_URL}/interrogation/ask`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question_id: questionId }),
    });

    const data = await response.json();
    if (data.success) {
      const result = data.result;
      showModal(`
                <h2>💬 Interrogation Result</h2>
                <div style="text-align: left; margin: 20px 0;">
                    <p><strong>Question:</strong> ${result.question}</p>
                    <p style="margin-top: 15px;"><strong>Response:</strong></p>
                    <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin-top: 10px;">
                        "${result.response}"
                    </div>
                    <p style="margin-top: 15px;">
                        <strong>Type:</strong> 
                        <span style="color: ${
                          result.response_type === "truth"
                            ? "#27ae60"
                            : result.response_type === "lie"
                            ? "#e74c3c"
                            : "#f39c12"
                        }">
                            ${result.response_type.toUpperCase()}
                        </span>
                    </p>
                    <p><strong>Utility Gained:</strong> ${
                      result.utility_gained
                    }</p>
                    <p><strong>Reveals Info:</strong> ${
                      result.reveals_info ? "✅ Yes" : "❌ No"
                    }</p>
                </div>
            `);
    }
  } catch (error) {
    console.error("Error asking question:", error);
    showNotification("Failed to ask question.", "error");
  }
}

function updateCSPVisualization(steps) {
  if (!steps || steps.length === 0) return;

  cspVisualizationDiv.classList.remove("hidden");
  cspStepsDiv.innerHTML = steps
    .map((step) => {
      let className = "csp-step";
      if (step.step === "Elimination") className += " elimination";
      if (step.step === "Confirmation") className += " confirmation";

      return `
            <div class="${className}">
                <strong>${step.step}:</strong> ${step.message}
            </div>
        `;
    })
    .join("");
}

function populateAccusationForm() {
  const suspects = ["Butler", "Chef", "Gardener"];
  const weapons = ["Knife", "Poison", "Rope"];
  const locations = ["Kitchen", "Library", "Garden"];

  document.getElementById("accuseSuspect").innerHTML =
    '<option value="">Select Suspect</option>' +
    suspects.map((s) => `<option value="${s}">${s}</option>`).join("");

  document.getElementById("accuseWeapon").innerHTML =
    '<option value="">Select Weapon</option>' +
    weapons.map((w) => `<option value="${w}">${w}</option>`).join("");

  document.getElementById("accuseLocation").innerHTML =
    '<option value="">Select Location</option>' +
    locations.map((l) => `<option value="${l}">${l}</option>`).join("");
}

function showResult(correct, solution) {
  if (correct) {
    resultContent.innerHTML = `
            <div class="result-success">🎉 CORRECT!</div>
            <h2>Case Solved!</h2>
            <p style="margin-top: 20px; font-size: 1.1rem;">
                It was <strong>${solution.suspect}</strong> with the <strong>${solution.weapon}</strong> in the <strong>${solution.location}</strong>!
            </p>
            <p style="margin-top: 20px; color: #7f8c8d;">
                Total Cost: ${gameState.total_cost} | Actions: ${gameState.actions_taken.length}
            </p>
            <button class="btn btn-primary" onclick="location.reload()" style="margin-top: 20px;">
                Play Again
            </button>
        `;
  } else {
    resultContent.innerHTML = `
            <div class="result-failure">❌ INCORRECT!</div>
            <h2>Wrong Accusation</h2>
            <p style="margin-top: 20px;">
                Keep investigating to find more evidence!
            </p>
            <button class="btn btn-primary" onclick="resultModal.classList.remove('show')" style="margin-top: 20px;">
                Continue Investigation
            </button>
        `;
  }
  resultModal.classList.add("show");
}

function showModal(content) {
  resultContent.innerHTML = content;
  resultModal.classList.add("show");
}

function showLoading(element) {
  element.innerHTML = '<p class="empty-state">Loading...</p>';
}

function showNotification(message, type) {
  // Simple console notification - can be enhanced with toast notifications
  console.log(`[${type.toUpperCase()}] ${message}`);
}

function capitalizeFirst(str) {
  return str.charAt(0).toUpperCase() + str.slice(1);
}

// Close modal when clicking outside
window.onclick = function (event) {
  if (event.target == resultModal) {
    resultModal.classList.remove("show");
  }
};
