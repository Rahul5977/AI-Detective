import React, { useState } from "react";

const AccusationPanel = ({ onMakeAccusation }) => {
  const [suspect, setSuspect] = useState("");
  const [weapon, setWeapon] = useState("");
  const [location, setLocation] = useState("");

  const suspects = ["Butler", "Chef", "Gardener"];
  const weapons = ["Knife", "Poison", "Rope"];
  const locations = ["Kitchen", "Library", "Garden"];

  const handleAccuse = () => {
    if (!suspect || !weapon || !location) {
      alert("Please select all three options!");
      return;
    }
    onMakeAccusation({ suspect, weapon, location });
  };

  return (
    <div className="bg-white p-6 rounded-2xl shadow-lg border-4 border-yellow-400">
      <h2 className="text-2xl font-bold text-gray-800 mb-5 pb-2 border-b-4 border-blue-500">
        ⚖️ Make Your Accusation
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="flex flex-col gap-2">
          <label className="font-semibold text-gray-800">Suspect:</label>
          <select
            value={suspect}
            onChange={(e) => setSuspect(e.target.value)}
            className="p-3 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none bg-white"
          >
            <option value="">Select Suspect</option>
            {suspects.map((s) => (
              <option key={s} value={s}>
                {s}
              </option>
            ))}
          </select>
        </div>
        <div className="flex flex-col gap-2">
          <label className="font-semibold text-gray-800">Weapon:</label>
          <select
            value={weapon}
            onChange={(e) => setWeapon(e.target.value)}
            className="p-3 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none bg-white"
          >
            <option value="">Select Weapon</option>
            {weapons.map((w) => (
              <option key={w} value={w}>
                {w}
              </option>
            ))}
          </select>
        </div>
        <div className="flex flex-col gap-2">
          <label className="font-semibold text-gray-800">Location:</label>
          <select
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            className="p-3 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none bg-white"
          >
            <option value="">Select Location</option>
            {locations.map((l) => (
              <option key={l} value={l}>
                {l}
              </option>
            ))}
          </select>
        </div>
      </div>
      <button
        onClick={handleAccuse}
        className="w-full mt-5 bg-red-500 text-white px-6 py-4 rounded-lg font-bold text-lg hover:bg-red-600 transition-colors duration-300 shadow-lg"
      >
        🎯 Make Accusation!
      </button>
    </div>
  );
};

export default AccusationPanel;