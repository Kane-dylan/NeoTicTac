import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useSocket } from "../context/SocketContext";
import GameBoard from "../components/GameBoard";
import PlayerInfo from "../components/PlayerInfo";
import ChatBox from "../components/ChatBox";

const GameRoom = () => {
  const { id: gameId } = useParams();
  const { socket } = useSocket();
  const navigate = useNavigate();

  const [game, setGame] = useState({
    board: Array(9).fill(null),
    players: [],
    currentPlayer: null,
    winner: null,
  });
  const [messages, setMessages] = useState([]);
  const [isYourTurn, setIsYourTurn] = useState(false);

  useEffect(() => {
    if (!socket) return;

    // Join the game room
    socket.emit("join-game-room", { gameId }, (response) => {
      if (!response.success) {
        navigate("/lobby");
      }
      setGame(response.game);
    });

    // Listen for game updates
    socket.on("game-update", (updatedGame) => {
      setGame(updatedGame);
      setIsYourTurn(updatedGame.currentPlayer === socket.id);
    });

    // Listen for chat messages
    socket.on("new-message", (message) => {
      setMessages((prev) => [...prev, message]);
    });

    // Listen for game end
    socket.on("game-over", (result) => {
      setGame((prev) => ({
        ...prev,
        winner: result.winner,
      }));
    });

    return () => {
      socket.emit("leave-game-room", { gameId });
      socket.off("game-update");
      socket.off("new-message");
      socket.off("game-over");
    };
  }, [socket, gameId, navigate]);

  const handleSquareClick = (index) => {
    if (!isYourTurn || game.board[index] || game.winner) return;

    socket.emit("make-move", { gameId, index });
  };

  const sendMessage = (text) => {
    socket.emit("send-message", { gameId, text });
  };

  const leaveGame = () => {
    socket.emit("leave-game", { gameId });
    navigate("/lobby");
  };

  return (
    <div className="container mx-auto p-4">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Game Room: {gameId}</h1>
        <button
          className="bg-red-500 text-white py-1 px-3 rounded hover:bg-red-600"
          onClick={leaveGame}
        >
          Leave Game
        </button>
      </div>

      {game.winner && (
        <div className="bg-yellow-100 border border-yellow-400 text-yellow-700 p-3 rounded mb-4">
          {game.winner === "draw"
            ? "Game ended in a draw!"
            : `Player ${game.winner} wins!`}
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div>
          <h2 className="text-xl font-semibold mb-3">Players</h2>
          {game.players.map((player, index) => (
            <PlayerInfo
              key={player.id}
              player={player}
              isActive={game.currentPlayer === player.id}
            />
          ))}

          {game.players.length === 1 && (
            <div className="mt-3 bg-blue-100 p-3 rounded">
              Waiting for another player to join...
            </div>
          )}

          <div className="mt-4">
            {isYourTurn ? (
              <div className="bg-green-100 p-2 rounded text-center">
                Your turn!
              </div>
            ) : (
              <div className="bg-gray-100 p-2 rounded text-center">
                Opponent's turn
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
