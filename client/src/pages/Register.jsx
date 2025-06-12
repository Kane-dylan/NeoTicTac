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
    <div className="min-h-screen bg-background-secondary flex items-center justify-center px-4">
      <div className="card p-8 w-full max-w-md">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="text-4xl mb-4">🎮</div>
          <h2 className="text-3xl font-bold text-text-primary mb-2">
            Join the Game
          </h2>
          <p className="text-text-secondary">
            Create your account to start playing
          </p>
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-accent-error/10 border border-accent-error/20 text-accent-error p-4 rounded-lg mb-6">
            <div className="flex items-center gap-2">
              <span>⚠️</span>
              <span className="text-sm">{error}</span>
            </div>
          </div>
        )}

        {/* Registration Form */}
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-text-primary mb-2">
              Username
            </label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="input-field w-full"
              placeholder="Choose a unique username"
              required
              minLength={3}
              maxLength={20}
            />
            <p className="text-xs text-text-muted mt-1">
              3-20 characters, will be visible to other players
            </p>
          </div>

          <div>
            <label className="block text-sm font-medium text-text-primary mb-2">
              Password
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="input-field w-full"
              placeholder="Create a secure password"
              required
              minLength={6}
            />
            <p className="text-xs text-text-muted mt-1">Minimum 6 characters</p>
          </div>

          <div>
            <label className="block text-sm font-medium text-text-primary mb-2">
              Confirm Password
            </label>
            <input
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              className="input-field w-full"
              placeholder="Confirm your password"
              required
            />
            {confirmPassword && password !== confirmPassword && (
              <p className="text-xs text-accent-error mt-1">
                Passwords do not match
              </p>
            )}
            {confirmPassword && password === confirmPassword && (
              <p className="text-xs text-accent-success mt-1">
                ✓ Passwords match
              </p>
            )}
          </div>

          <button
            type="submit"
            className="btn-primary w-full py-3 text-base"
            disabled={password !== confirmPassword}
          >
            🚀 Create Account
          </button>
        </form>

        {/* Login Link */}
        <div className="mt-6 text-center">
          <p className="text-text-secondary text-sm">
            Already have an account?{" "}
            <Link
              to="/"
              className="text-primary hover:text-primary-hover font-medium transition-colors"
            >
              Sign in here
            </Link>
          </p>
        </div>

        {/* Footer */}
        <div className="mt-8 text-center">
          <p className="text-xs text-text-muted">
            By creating an account, you agree to play fair and have fun!
          </p>
        </div>
      </div>
    </div>
  );
};

export default Register;
