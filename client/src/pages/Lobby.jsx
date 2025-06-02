import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useSocket } from "../context/SocketContext";
import { getActiveGames } from "../services/api";

const Lobby = () => {
  const [games, setGames] = useState([]);
  const [username, setUsername] = useState("");
  const { socket } = useSocket();
  const navigate = useNavigate();

  useEffect(() => {
    // Fetch active games
    const fetchGames = async () => {
      try {
        const activeGames = await getActiveGames();
        setGames(activeGames);
      } catch (error) {
        console.error("Failed to fetch games:", error);
        setGames([]);
      }
    };

    fetchGames();

    // Get user details
    const token = localStorage.getItem("token");
    if (!token) {
      navigate("/");
      return;
    }

    // Set up socket events for lobby updates
    if (socket) {
      socket.on("game-created", (game) => {
        setGames((prevGames) => [...prevGames, game]);
      });

      socket.on("game-started", (gameId) => {
        setGames((prevGames) => prevGames.filter((game) => game.id !== gameId));
      });
    }

    return () => {
      if (socket) {
        socket.off("game-created");
        socket.off("game-started");
      }
    };
  }, [socket, navigate]);

  const createGame = () => {
    if (socket && username) {
      socket.emit("create-game", { username }, (response) => {
        if (response && response.gameId) {
          navigate(`/game/${response.gameId}`);
        }
      });
    }
  };

  const joinGame = (gameId) => {
    if (socket && username) {
      socket.emit("join-game", { gameId, username }, (response) => {
        if (response && response.success) {
          navigate(`/game/${gameId}`);
        }
      });
    }
  };

  const logout = () => {
    localStorage.removeItem("token");
    navigate("/");
  };

  return (
    <div className="container mx-auto p-4">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Game Lobby</h1>
        <button
          className="bg-red-500 text-white py-2 px-4 rounded hover:bg-red-600"
          onClick={logout}
        >
          Logout
        </button>
      </div>

      <div className="mb-6">
        <div className="mb-4">
          <label className="block mb-2">Your Username:</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="border rounded px-3 py-2 mr-4"
            placeholder="Enter your username"
          />
        </div>

        <button
          className="bg-green-500 text-white py-2 px-4 rounded hover:bg-green-600 disabled:bg-gray-400"
          onClick={createGame}
          disabled={!username.trim()}
        >
          Create New Game
        </button>
      </div>

      <div>
        <h2 className="text-xl font-semibold mb-3">Available Games</h2>

        {games.length === 0 ? (
          <p className="text-gray-600">No active games. Create one!</p>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {games.map((game) => (
              <div key={game.id} className="border p-4 rounded shadow">
                <p className="font-semibold">Host: {game.host}</p>
                <p className="text-sm text-gray-600">
                  Created: {new Date(game.createdAt).toLocaleString()}
                </p>
                <p className="text-sm">Players: {game.playerCount || 1}/2</p>
                <button
                  className="mt-2 bg-blue-500 text-white py-1 px-3 rounded hover:bg-blue-600 disabled:bg-gray-400"
                  onClick={() => joinGame(game.id)}
                  disabled={!username.trim() || game.playerCount >= 2}
                >
                  {game.playerCount >= 2 ? "Game Full" : "Join Game"}
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Lobby;
