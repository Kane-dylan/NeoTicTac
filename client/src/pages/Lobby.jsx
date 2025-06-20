import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useSocket } from "../context/SocketContext";
import { getAllGames, createGame } from "../services/api";

const Lobby = () => {
  const [games, setGames] = useState([]);
  const [username, setUsername] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const { socket } = useSocket();
  const navigate = useNavigate();
  const fetchGames = async () => {
    setLoading(true);
    setError("");
    try {
      const allGames = await getAllGames();
      setGames(allGames);
    } catch {
      setError("Failed to load games");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const token = localStorage.getItem("token");
    const storedUsername = localStorage.getItem("username");

    if (!token) {
      navigate("/");
      return;
    }

    if (storedUsername) {
      setUsername(storedUsername);
    }

    fetchGames();

    // Simple socket listeners
    if (socket) {
      socket.emit("join_lobby");
      socket.on("lobby_games_update", (data) => setGames(data.games || []));
      socket.on("game_created", (newGame) => {
        if (newGame?.id) setGames((prev) => [...prev, newGame]);
      });
    }

    return () => {
      if (socket) {
        socket.emit("leave_lobby");
        socket.off("lobby_games_update");
        socket.off("game_created");
      }
    };
  }, [socket, navigate]);

  const handleCreateGame = async () => {
    if (!username.trim()) {
      setError("Please enter a username first");
      return;
    }
    setError("");
    setLoading(true);
    try {
      const response = await createGame();
      localStorage.setItem("username", username);
      if (response?.gameId) {
        navigate(`/game/${response.gameId}`);
      }
    } catch {
      setError("Failed to create game");
    } finally {
      setLoading(false);
    }
  };

  const handleJoinGame = (gameId) => {
    if (!username.trim()) {
      setError("Please enter a username first");
      return;
    }
    localStorage.setItem("username", username);
    navigate(`/game/${gameId}`);
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    if (socket) socket.disconnect();
    navigate("/");
  };
  return (
    <div className="min-h-screen bg-cyber-black relative overflow-hidden">
      {/* Floating Particles */}
      <div className="floating-particles">
        {[...Array(15)].map((_, i) => (
          <div
            key={i}
            className="particle"
            style={{
              left: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 12}s`,
              animationDuration: `${10 + Math.random() * 5}s`,
            }}
          />
        ))}
      </div>

      {/* Animated Background Grid */}
      <div className="absolute inset-0 game-grid opacity-10"></div>

      <div className="relative z-10 min-h-screen">
        <div className="container mx-auto px-4 py-6 max-w-6xl">
          {/* Header Section */}
          <div className="cyber-card p-6 mb-6">
            <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
              <div>
                <h1 className="text-4xl font-bold text-neon-green mb-2 flex items-center gap-3 neon-text font-mono glitch-text">
                  ⚡ GAME MATRIX ⚡
                </h1>
                <p className="text-neon-cyan font-mono">
                  WELCOME BACK, USER:{" "}
                  <span className="font-bold text-neon-purple neon-text">
                    {username || "ANONYMOUS"}
                  </span>
                </p>
              </div>
              <button
                className="btn-neon-pink py-3 px-6 font-mono hover:transform hover:scale-105 transition-all duration-300"
                onClick={handleLogout}
              >
                🚪 LOGOUT
              </button>
            </div>
          </div>

          {/* Error Message */}
          {error && (
            <div className="bg-neon-pink/10 border-2 border-neon-pink text-neon-pink p-4 rounded-lg mb-6 animate-neon-flicker">
              <div className="flex items-center gap-2 font-mono">
                <span className="text-lg">⚠</span>
                <span className="text-sm uppercase tracking-wide">{error}</span>
              </div>
            </div>
          )}

          {/* User Controls Section */}
          <div className="cyber-card p-6 mb-6">
            <h2 className="text-2xl font-bold text-neon-green mb-4 flex items-center gap-2 neon-text font-mono">
              👤 USER SETUP
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Username Input */}
              <div>
                <label className="block text-sm font-mono font-bold text-neon-green mb-2 uppercase tracking-wider">
                  &gt; Player Identity:
                </label>
                <input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className="cyber-input w-full p-3 rounded font-mono text-neon-green"
                  placeholder="enter.player.name"
                  maxLength={20}
                />
                <p className="text-xs text-text-muted mt-1 font-mono">
                  // visible to all players in network
                </p>
              </div>

              {/* Action Buttons */}
              <div className="flex flex-col justify-end">
                <div className="flex flex-wrap gap-3">
                  <button
                    onClick={handleCreateGame}
                    className="btn-neon flex items-center gap-2 px-6 py-3 disabled:opacity-50 disabled:cursor-not-allowed font-mono hover:transform hover:scale-105 transition-all duration-300"
                    disabled={!username.trim() || loading}
                  >
                    {loading ? (
                      <>
                        <div className="animate-spin rounded-full h-4 w-4 border-2 border-neon-green border-t-transparent"></div>
                        CREATING...
                      </>
                    ) : (
                      <>➕ NEW GAME</>
                    )}
                  </button>
                  <button
                    onClick={fetchGames}
                    className="btn-neon-cyan flex items-center gap-2 px-4 py-3 font-mono hover:transform hover:scale-105 transition-all duration-300"
                  >
                    🔄 REFRESH
                  </button>
                </div>
              </div>
            </div>
          </div>

          {/* Games List Section */}
          <div className="cyber-card p-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-neon-green flex items-center gap-2 neon-text font-mono">
                🎯 ACTIVE GAMES
                <span className="bg-cyber-darker text-neon-cyan px-3 py-1 rounded-full text-sm font-mono border border-neon-cyan neon-text">
                  {games.length}
                </span>
              </h2>
            </div>

            {/* Loading State */}
            {loading && games.length === 0 && (
              <div className="text-center py-12">
                <div className="animate-spin rounded-full h-12 w-12 border-4 border-neon-green border-t-transparent mx-auto mb-4"></div>
                <p className="text-neon-cyan font-mono">
                  LOADING GAME MATRIX...
                </p>
              </div>
            )}

            {/* Empty State */}
            {!loading && games.length === 0 && (
              <div className="text-center py-16 bg-cyber-darker rounded-lg border border-neon-green/30">
                <div className="text-6xl mb-4 animate-neon-pulse">🎮</div>
                <h3 className="text-xl font-bold text-neon-green mb-2 neon-text font-mono">
                  NO ACTIVE GAMES FOUND
                </h3>
                <p className="text-neon-cyan mb-6 font-mono">
                  INITIALIZE FIRST GAME SESSION
                </p>
                <button
                  onClick={handleCreateGame}
                  className="btn-neon px-6 py-3 disabled:opacity-50 disabled:cursor-not-allowed font-mono hover:transform hover:scale-105 transition-all duration-300"
                  disabled={!username.trim() || loading}
                >
                  ➕ CREATE FIRST GAME
                </button>
              </div>
            )}

            {/* Games Grid */}
            {games.length > 0 && (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {games.map((game) => (
                  <div
                    key={game.id}
                    className="cyber-card p-6 hover:shadow-neon transition-all duration-300 border-l-4 border-l-neon-green hover:transform hover:scale-105"
                  >
                    {/* Game Header */}
                    <div className="mb-4">
                      <div className="flex items-center justify-between mb-2">
                        <h3 className="font-bold text-neon-green text-lg font-mono neon-text">
                          🎮 {game.host}
                          {game.player_o && (
                            <span className="text-neon-cyan">
                              {" "}
                              VS {game.player_o}
                            </span>
                          )}
                        </h3>
                        <span className="text-xs font-mono text-text-muted bg-cyber-darker px-2 py-1 rounded border border-neon-green/30">
                          #{game.id}
                        </span>
                      </div>
                    </div>

                    {/* Game Status */}
                    <div className="mb-4 space-y-2 font-mono">
                      <div className="flex items-center justify-between">
                        <span className="text-sm text-neon-cyan">STATUS:</span>
                        <span
                          className={`text-sm font-bold px-2 py-1 rounded-full border ${
                            game.status === "waiting"
                              ? "bg-neon-yellow/10 text-neon-yellow border-neon-yellow"
                              : game.status === "in_progress"
                              ? "bg-neon-cyan/10 text-neon-cyan border-neon-cyan"
                              : "bg-neon-green/10 text-neon-green border-neon-green"
                          }`}
                        >
                          {game.status === "waiting" && "🟡 WAITING"}
                          {game.status === "in_progress" && "🔵 ACTIVE"}
                          {game.status === "completed" && "🟢 COMPLETE"}
                        </span>
                      </div>

                      <div className="flex items-center justify-between">
                        <span className="text-sm text-neon-cyan">PLAYERS:</span>
                        <span className="text-sm font-bold text-neon-green neon-text">
                          {game.playerCount}/2
                        </span>
                      </div>

                      {game.status === "completed" && (
                        <div className="flex items-center justify-between">
                          <span className="text-sm text-neon-cyan">
                            RESULT:
                          </span>
                          <span className="text-sm font-bold text-neon-purple neon-text">
                            {game.is_draw ? "🤝 DRAW" : `🏆 ${game.winner} WIN`}
                          </span>
                        </div>
                      )}
                    </div>

                    {/* Join Button */}
                    <button
                      onClick={() => handleJoinGame(game.id)}
                      className={`w-full py-3 px-4 rounded-md font-mono font-bold transition-all duration-300 hover:transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed ${
                        game.status === "waiting"
                          ? "btn-neon"
                          : game.status === "in_progress"
                          ? "btn-neon-cyan"
                          : "bg-cyber-darker border-2 border-neon-purple text-neon-purple hover:bg-neon-purple hover:text-cyber-black"
                      }`}
                      disabled={!username.trim() || loading}
                    >
                      {game.status === "waiting" && "🚀 JOIN GAME"}
                      {game.status === "in_progress" && "👀 SPECTATE"}
                      {game.status === "completed" && "📊 VIEW RESULTS"}
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Lobby;
