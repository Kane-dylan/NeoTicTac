import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { loginUser } from "../services/api";

const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      const data = await loginUser({ username, password });
      if (data.token) {
        localStorage.setItem("token", data.token);
        localStorage.setItem("username", username);
        navigate("/lobby");
      } else {
        setError("Login successful, but no token received.");
      }
    } catch (err) {
      setError(
        err.response?.data?.msg || err.message || "Invalid username or password"
      );
    }
  };
  return (
    <div className="min-h-screen bg-cyber-black relative overflow-hidden">
      {/* Floating Particles */}
      <div className="floating-particles">
        {[...Array(12)].map((_, i) => (
          <div
            key={i}
            className="particle"
            style={{
              left: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 10}s`,
              animationDuration: `${8 + Math.random() * 4}s`,
            }}
          />
        ))}
      </div>

      {/* Animated Background Grid */}
      <div className="absolute inset-0 game-grid opacity-20"></div>

      {/* Main Login Container */}
      <div className="relative z-10 min-h-screen flex items-center justify-center px-4">
        <div className="cyber-card rounded-lg p-8 w-full max-w-md animate-float-up backdrop-blur-lg">
          {/* Header */}
          <div className="text-center mb-8">
            <div className="text-6xl mb-4 animate-neon-pulse">🎮</div>
            <h2 className="text-4xl font-bold text-neon-green mb-3 neon-text font-mono glitch-text">
              SYSTEM LOGIN
            </h2>
            <p className="text-neon-cyan text-sm font-mono">
              ACCESS TERMINAL • AUTHENTICATE USER
            </p>
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

          {/* Login Form */}
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-mono font-bold text-neon-green mb-2 uppercase tracking-wider">
                &gt; Username
              </label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="cyber-input w-full p-3 rounded font-mono text-neon-green placeholder-text-muted bg-cyber-darker"
                placeholder="enter.username"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-mono font-bold text-neon-green mb-2 uppercase tracking-wider">
                &gt; Password
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="cyber-input w-full p-3 rounded font-mono text-neon-green placeholder-text-muted bg-cyber-darker"
                placeholder="enter.password"
                required
              />
            </div>

            <button
              type="submit"
              className="btn-neon w-full py-4 text-lg font-mono rounded hover:transform hover:scale-105 transition-all duration-300"
            >
              INITIALIZE LOGIN
            </button>
          </form>

          {/* Register Link */}
          <div className="mt-8 text-center">
            <p className="text-text-muted text-sm font-mono">
              NO ACCOUNT FOUND?{" "}
              <Link
                to="/register"
                className="text-neon-cyan hover:text-neon-purple font-bold transition-colors duration-300 neon-text"
              >
                CREATE USER
              </Link>
            </p>
          </div>

          {/* Footer Terminal Style */}
          <div className="mt-8 text-center">
            <div className="terminal-window p-3 rounded bg-cyber-black">
              <p className="text-xs text-neon-green font-mono">
                SECURE_AUTH v2.1.1 • JWT_PROTOCOL_ACTIVE
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
