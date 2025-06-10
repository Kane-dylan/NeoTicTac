import "./App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
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
    </ErrorBoundary>
  );
}

export default App;
