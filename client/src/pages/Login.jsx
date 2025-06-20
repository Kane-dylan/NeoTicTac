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
    <div className="min-h-screen bg-background-secondary flex items-center justify-center px-4 relative overflow-hidden">
      {" "}      {/* Animated Background Pattern - Abstract Art Inspired */}
      <div className="absolute inset-0 opacity-10">
        {/* Base gradient */}
        <div className="absolute inset-0 bg-gradient-to-br from-orange-400/15 via-blue-400/8 to-yellow-400/15"></div>

        {/* Abstract organic shapes inspired by the image */}
        <div className="absolute top-16 left-12 w-24 h-16 bg-red-400 rounded-full transform rotate-12 animate-float-slow opacity-60"></div>
        <div className="absolute top-32 right-16 w-20 h-32 bg-orange-400 rounded-full transform rotate-45 animate-sway opacity-70"></div>
        <div className="absolute bottom-32 left-20 w-16 h-16 bg-blue-500 rounded-full animate-float-medium opacity-80"></div>
        <div className="absolute top-40 left-1/3 w-12 h-20 bg-yellow-400 rounded-full transform rotate-25 animate-float-fast opacity-60"></div>
        <div className="absolute bottom-24 right-12 w-28 h-14 bg-teal-400 rounded-full animate-morph opacity-70"></div>
        <div className="absolute top-1/4 right-1/3 w-8 h-8 bg-green-400 rounded-full animate-bounce-subtle opacity-80"></div>

        {/* Small dots scattered around */}
        <div className="absolute top-24 left-1/2 w-3 h-3 bg-red-300 rounded-full animate-pulse"></div>
        <div className="absolute bottom-40 left-1/4 w-2 h-2 bg-blue-300 rounded-full animate-float-slow"></div>
        <div className="absolute top-60 right-24 w-4 h-4 bg-yellow-300 rounded-full animate-float-medium"></div>
        <div className="absolute bottom-60 right-1/4 w-3 h-3 bg-green-300 rounded-full animate-pulse"></div>

        {/* Abstract curved lines and shapes */}
        <svg
          className="absolute inset-0 w-full h-full"
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 800 600"
        >
          {/* Squiggly lines */}
          <path
            d="M50,100 Q100,80 150,120 T250,100 Q300,80 350,120"
            stroke="#ef4444"
            strokeWidth="3"
            fill="none"
            className="animate-draw opacity-30"
          />
          <path
            d="M600,200 Q550,180 500,220 T400,200 Q350,180 300,220"
            stroke="#3b82f6"
            strokeWidth="2"
            fill="none"
            className="animate-draw-delayed opacity-40"
          />
          <path
            d="M100,400 Q150,380 200,420 T300,400"
            stroke="#f59e0b"
            strokeWidth="4"
            fill="none"
            className="animate-wiggle opacity-35"
          />

          {/* Abstract blob shapes */}
          <path
            d="M150,250 Q200,200 250,250 Q300,300 250,350 Q200,400 150,350 Q100,300 150,250 Z"
            fill="#10b981"
            className="animate-morph-blob opacity-20"
          />
          <path
            d="M500,150 Q550,100 600,150 Q650,200 600,250 Q550,300 500,250 Q450,200 500,150 Z"
            fill="#8b5cf6"
            className="animate-morph-blob-reverse opacity-25"
          />

          {/* Curved doodle lines */}
          <path
            d="M200,300 Q250,250 300,300 Q350,350 400,300"
            stroke="#ec4899"
            strokeWidth="2"
            fill="none"
            className="animate-float-path opacity-30"
          />
          <path
            d="M400,450 Q450,400 500,450 Q550,500 600,450"
            stroke="#06b6d4"
            strokeWidth="3"
            fill="none"
            className="animate-float-path-reverse opacity-35"
          />

          {/* Spiral elements */}
          <circle
            cx="150"
            cy="150"
            r="30"
            fill="none"
            stroke="#f97316"
            strokeWidth="2"
            className="animate-spin-slow opacity-40"
          />
          <circle
            cx="650"
            cy="450"
            r="25"
            fill="none"
            stroke="#84cc16"
            strokeWidth="2"
            className="animate-spin-reverse opacity-30"
          />

          {/* Abstract scribbles */}
          <path
            d="M300,50 Q320,70 340,50 Q360,30 380,50 Q400,70 420,50"
            stroke="#6366f1"
            strokeWidth="2"
            fill="none"
            className="animate-wiggle opacity-40"
          />
          <path
            d="M500,500 Q520,520 540,500 Q560,480 580,500 Q600,520 620,500"
            stroke="#d946ef"
            strokeWidth="2"
            fill="none"
            className="animate-wiggle-reverse opacity-35"
          />
        </svg>

        {/* Additional floating elements */}
        <div className="absolute top-20 right-40 w-6 h-12 bg-orange-300 transform rotate-45 animate-sway opacity-50"></div>
        <div className="absolute bottom-16 left-40 w-10 h-6 bg-blue-300 transform rotate-12 animate-float-slow opacity-60"></div>
        <div className="absolute top-1/2 left-16 w-4 h-16 bg-yellow-300 transform rotate-75 animate-float-medium opacity-55"></div>
      </div>      <div className="card p-8 w-full max-w-md relative z-10 animate-fade-in-up backdrop-blur-sm bg-white/95 shadow-xl border border-slate-200/50">{/* Header */}
        <div className="text-center mb-8">
          <div className="text-4xl mb-4">🎮</div>
          <h2 className="text-3xl font-bold text-text-primary mb-2">
            Welcome Back
          </h2>
          <p className="text-text-secondary">Sign in to continue playing</p>
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

        {/* Login Form */}
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
              placeholder="Enter your username"
              required
            />
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
              placeholder="Enter your password"
              required
            />
          </div>

          <button type="submit" className="btn-primary w-full py-3 text-base">
            🚀 Sign In
          </button>
        </form>

        {/* Register Link */}
        <div className="mt-6 text-center">
          <p className="text-text-secondary text-sm">
            Don't have an account?{" "}
            <Link
              to="/register"
              className="text-primary hover:text-primary-hover font-medium transition-colors"
            >
              Create one here
            </Link>
          </p>
        </div>

        {/* Footer */}
        <div className="mt-8 text-center">
          <p className="text-xs text-text-muted">
            Secure login powered by JWT authentication
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;
