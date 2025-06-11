import React, { useEffect, useState, useCallback } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useSocket } from "../context/SocketContext";
import { getGameDetails } from "../services/api";
import GameBoard from "../components/GameBoard";
import PlayerInfo from "../components/PlayerInfo";
import ChatBox from "../components/ChatBox";

const GameRoom = () => {
  const { id: gameId } = useParams();
  const { socket } = useSocket();
  const navigate = useNavigate();

  const [game, setGame] = useState(null);
  const [messages, setMessages] = useState([]);
  const [currentPlayer, setCurrentPlayer] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const fetchGameDetails = useCallback(async () => {
    if (!gameId) return;
    try {
      const gameData = await getGameDetails(gameId);
      setGame(gameData);
      setError("");
    } catch (error) {
      setError("Failed to load game");
    } finally {
      setLoading(false);
    }
  }, [gameId]);

  useEffect(() => {
    if (!gameId) {
      navigate("/lobby");
      return;
    }

    const token = localStorage.getItem("token");
    const username = localStorage.getItem("username");

    if (!token || !username) {
      navigate("/");
      return;
    }

    setCurrentPlayer(username);
    fetchGameDetails();

    // Socket setup
    if (socket) {
      socket.emit("join_room", { room: gameId, player: username });

      // Game state updates
      socket.on("game_state_update", (data) => {
        if (data?.game) setGame(data.game);
      });

      socket.on("move_made", (data) => {
        if (data?.game) setGame(data.game);
      });

      // Chat messages
      socket.on("receive_message", (message) => {
        setMessages((prev) => [...prev, message]);
      });

      // Game events
      socket.on("player_joined", () => fetchGameDetails());
      socket.on("game_over", () => fetchGameDetails());
    }

    return () => {
      if (socket) {
        socket.emit("leave_room", { room: gameId, player: username });
        socket.off("game_state_update");
        socket.off("move_made");
        socket.off("receive_message");
        socket.off("player_joined");
        socket.off("game_over");
      }
    };
  }, [socket, gameId, navigate, fetchGameDetails]);

  const handleSquareClick = (index) => {
    if (!game || !socket || !currentPlayer) return;

    // Basic validations
    if (game.board[index] !== "" || game.winner || game.is_draw) return;
    if (!game.player_o) {
      setError("Waiting for another player to join!");
      return;
    }

    // Check if it's player's turn
    const isPlayerTurn =
      (game.current_turn === "X" && currentPlayer === game.player_x) ||
      (game.current_turn === "O" && currentPlayer === game.player_o);

    if (!isPlayerTurn) {
      setError("It's not your turn!");
      setTimeout(() => setError(""), 2000);
      return;
    }

    // Make the move
    socket.emit("make_move", {
      room: gameId,
      index: index,
      symbol: game.current_turn,
      player: currentPlayer,
    });
  };

  const sendMessage = (text) => {
    if (socket && currentPlayer) {
      socket.emit("send_message", {
        room: gameId,
        sender: currentPlayer,
        text: text,
        timestamp: Date.now(),
      });
    }
  };

  const requestRestart = () => {
    if (socket && currentPlayer) {
      socket.emit("request_game_restart", {
        room: gameId,
        player: currentPlayer,
      });
    }
  };

  const leaveGame = () => navigate("/lobby");

  const isCurrentPlayerTurn = () => {
    if (!game || !game.player_o) return false;
    const playerRole =
      currentPlayer === game.player_x
        ? "X"
        : currentPlayer === game.player_o
        ? "O"
        : "spectator";
    return playerRole !== "spectator" && game.current_turn === playerRole;
  };

  if (loading) {
    return (
      <div className="container mx-auto p-4">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900 mx-auto mb-4"></div>
          <p>Loading game...</p>
        </div>
      </div>
    );
  }

  if (!game) {
    return (
      <div className="container mx-auto p-4">
        <div className="bg-red-100 text-red-700 p-4 rounded mb-4">
          <h2 className="text-xl font-bold mb-2">Game Not Found</h2>
          <p>The game you're looking for doesn't exist or has been deleted.</p>
        </div>
        <button
          className="bg-blue-500 text-white py-2 px-4 rounded"
          onClick={() => navigate("/lobby")}
        >
          Back to Lobby
        </button>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-4">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Game Room: {gameId}</h1>
        <button
          className="bg-red-500 text-white py-2 px-4 rounded hover:bg-red-600"
          onClick={leaveGame}
        >
          Leave Game
        </button>
      </div>

      {error && (
        <div className="bg-red-100 text-red-700 p-3 rounded mb-4">{error}</div>
      )}

      {(game.winner || game.is_draw) && (
        <div className="bg-yellow-100 border border-yellow-400 text-yellow-700 p-4 rounded mb-4">
          <div className="text-center text-lg font-semibold mb-3">
            {game.is_draw
              ? "🤝 Game ended in a draw!"
              : `🎉 ${
                  game.winner === "X" ? game.player_x : game.player_o
                } (Player ${game.winner}) wins!`}
          </div>
          {(currentPlayer === game.player_x ||
            currentPlayer === game.player_o) && (
            <div className="text-center">
              <button
                className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 mr-2"
                onClick={requestRestart}
              >
                🔄 Play Again
              </button>
              <button
                className="bg-green-500 text-white py-2 px-4 rounded hover:bg-green-600"
                onClick={leaveGame}
              >
                🏠 Back to Lobby
              </button>
            </div>
          )}
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div>
          <h2 className="text-xl font-semibold mb-3">Players</h2>
          <div className="space-y-3">
            <PlayerInfo
              player={{ username: game.player_x || "Player X", symbol: "X" }}
              isActive={
                game.current_turn === "X" &&
                game.player_o &&
                !game.winner &&
                !game.is_draw
              }
              isCurrentUser={currentPlayer === game.player_x}
              isWaiting={false}
              isConnected={true}
            />
            <PlayerInfo
              player={{
                username: game.player_o || "Waiting for Player O...",
                symbol: "O",
              }}
              isActive={
                game.current_turn === "O" && !game.winner && !game.is_draw
              }
              isCurrentUser={currentPlayer === game.player_o}
              isWaiting={!game.player_o}
              isConnected={true}
            />
          </div>

          <div className="mt-4">
            {game.player_o ? (
              isCurrentPlayerTurn() ? (
                <div className="bg-green-100 p-2 rounded text-center">
                  Your turn!
                </div>
              ) : (
                <div className="bg-gray-100 p-2 rounded text-center">
                  {currentPlayer === game.player_x
                    ? game.player_o
                    : game.player_x}
                  's turn
                </div>
              )
            ) : (
              <div className="bg-yellow-100 p-2 rounded text-center">
                Waiting for opponent
              </div>
            )}
          </div>
        </div>

        <div className="flex items-center justify-center">
          <GameBoard board={game.board} onSquareClick={handleSquareClick} />
        </div>

        <div>
          <h2 className="text-xl font-semibold mb-3">Chat</h2>
          <ChatBox messages={messages} sendMessage={sendMessage} />
        </div>
      </div>
    </div>
  );
};

export default GameRoom;
