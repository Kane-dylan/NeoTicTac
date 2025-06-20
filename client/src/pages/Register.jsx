import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { registerUser } from "../services/api";

const Register = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    try {
      await registerUser({ username, password });
      navigate("/");
    } catch (err) {
      setError(err.response?.data?.message || "Registration failed");
    }
  };
  return (
    <div className="min-h-screen bg-cyber-black relative overflow-hidden">
      {/* Floating Particles */}
      <div className="floating-particles">
        {[...Array(8)].map((_, i) => (
          <div
            key={i}
            className="particle"
            style={{
              left: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 8}s`,
              animationDuration: `${6 + Math.random() * 3}s`,
            }}
          />
        ))}
      </div>

      {/* Animated Background Grid */}
      <div className="absolute inset-0 game-grid opacity-15"></div>

      <div className="relative z-10 min-h-screen flex items-center justify-center px-4">
        <div className="cyber-card rounded-lg p-8 w-full max-w-md animate-float-up">
          {/* Header */}
          <div className="text-center mb-8">
            <div className="text-5xl mb-4 animate-neon-pulse">🎮</div>
            <h2 className="text-3xl font-bold text-neon-green mb-3 neon-text font-mono glitch-text">
              USER REGISTRATION
            </h2>
            <p className="text-neon-cyan text-sm font-mono">
              CREATE NEW ACCOUNT • JOIN THE GRID
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

          {/* Registration Form */}
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-mono font-bold text-neon-green mb-2 uppercase tracking-wider">
                &gt; Username
              </label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="cyber-input w-full p-3 rounded font-mono text-neon-green"
                placeholder="choose.username"
                required
                minLength={3}
                maxLength={20}
              />
              <p className="text-xs text-text-muted mt-1 font-mono">
                // 3-20 chars, visible to other players
              </p>
            </div>

            <div>
              <label className="block text-sm font-mono font-bold text-neon-green mb-2 uppercase tracking-wider">
                &gt; Password
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="cyber-input w-full p-3 rounded font-mono text-neon-green"
                placeholder="create.password"
                required
                minLength={6}
              />
              <p className="text-xs text-text-muted mt-1 font-mono">
                // minimum 6 characters
              </p>
            </div>

            <div>
              <label className="block text-sm font-mono font-bold text-neon-green mb-2 uppercase tracking-wider">
                &gt; Confirm Password
              </label>
              <input
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                className="cyber-input w-full p-3 rounded font-mono text-neon-green"
                placeholder="confirm.password"
                required
              />
              {confirmPassword && password !== confirmPassword && (
                <p className="text-xs text-neon-pink mt-1 font-mono animate-neon-flicker">
                  // ERROR: passwords do not match
                </p>
              )}
              {confirmPassword && password === confirmPassword && (
                <p className="text-xs text-neon-green mt-1 font-mono neon-text">
                  // SUCCESS: passwords match
                </p>
              )}
            </div>

            <button
              type="submit"
              className="btn-neon w-full py-4 text-lg font-mono rounded hover:transform hover:scale-105 transition-all duration-300"
              disabled={password !== confirmPassword}
            >
              INITIALIZE ACCOUNT
            </button>
          </form>

          {/* Login Link */}
          <div className="mt-8 text-center">
            <p className="text-text-muted text-sm font-mono">
              ACCOUNT EXISTS?{" "}
              <Link
                to="/"
                className="text-neon-cyan hover:text-neon-purple font-bold transition-colors duration-300 neon-text"
              >
                ACCESS LOGIN
              </Link>
            </p>
          </div>

          {/* Footer Terminal Style */}
          <div className="mt-8 text-center">
            <div className="terminal-window p-3 rounded bg-cyber-black">
              <p className="text-xs text-neon-green font-mono">
                REGISTRATION_PROTOCOL v1.8.3 • SECURE_HASH_ACTIVE
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Register;
