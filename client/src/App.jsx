import "./App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Toaster } from "react-hot-toast";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Lobby from "./pages/Lobby";
import GameRoom from "./pages/GameRoom";
import ErrorBoundary from "./components/ErrorBoundary";

function App() {
  return (
    <ErrorBoundary fallbackMessage="The game application encountered an error. Please try refreshing or return to the lobby.">
      <Router>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/lobby" element={<Lobby />} />
          <Route
            path="/game/:id"
            element={
              <ErrorBoundary fallbackMessage="The game room encountered an error. Please try refreshing or return to the lobby.">
                <GameRoom />
              </ErrorBoundary>
            }
          />
        </Routes>
      </Router>
      <Toaster
        position="top-center"
        toastOptions={{
          duration: 4000,
          style: {
            background: "#0a0a0a",
            color: "#00ff88",
            border: "2px solid #00ff88",
            borderRadius: "8px",
            fontFamily: "monospace",
            fontSize: "14px",
            fontWeight: "bold",
            textTransform: "uppercase",
            letterSpacing: "0.5px",
          },
          success: {
            iconTheme: {
              primary: "#00ff88",
              secondary: "#0a0a0a",
            },
          },
          error: {
            style: {
              border: "2px solid #ff0080",
              color: "#ff0080",
            },
            iconTheme: {
              primary: "#ff0080",
              secondary: "#0a0a0a",
            },
          },
        }}
      />
    </ErrorBoundary>
  );
}

export default App;
