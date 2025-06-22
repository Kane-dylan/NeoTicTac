import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";

const LandingPage = () => {
  const [currentImageIndex, setCurrentImageIndex] = useState(0);
  const [imageLoaded, setImageLoaded] = useState(false);
  const gameImages = [
    "ttt6.png",
    "ttt1.png",
    "ttt2.png", 
    "ttt3.png",
    "ttt4.png",
    "ttt5.png",
  ];

  // Cycle through images for visual showcase
  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentImageIndex((prev) => (prev + 1) % gameImages.length);
      setImageLoaded(false);
    }, 3000);
    return () => clearInterval(interval);
  }, [gameImages.length]);

  // Preload images for better performance
  useEffect(() => {
    gameImages.forEach((imageName) => {
      const img = new Image();
      img.src = `/${imageName}`;
    });
  }, []);

  const handleImageLoad = () => {
    setImageLoaded(true);
  };

  const handleImageError = (e) => {
    console.log(`Failed to load image: ${gameImages[currentImageIndex]}`);
    const img = e.target;
    const currentSrc = img.src;
    
    if (currentSrc.includes(".jpeg")) {
      const pngSrc = currentSrc.replace(".jpeg", ".png");
      img.src = pngSrc;
    } else {
      setImageLoaded(false);
    }
  };
  return (
    <div className="min-h-screen bg-black relative overflow-hidden">
      {/* Floating Particles */}
      <div className="floating-particles">
        {[...Array(20)].map((_, i) => (
          <div
            key={i}
            className="particle"
            style={{
              left: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 15}s`,
              animationDuration: `${10 + Math.random() * 5}s`,
            }}
          />
        ))}
      </div>

      {/* Animated Background Grid */}
      <div className="absolute inset-0 game-grid opacity-20"></div>

      {/* Main Content */}
      <div className="relative z-10 min-h-screen flex flex-col">
        {/* Header Section */}
        <header className="text-center pt-8 pb-8 px-4">
          <div className="text-6xl mb-4 animate-float-path">🎮</div>
          <h1
            className="text-5xl md:text-7xl lg:text-8xl font-bold mb-4 font-mono"
            style={{
              color: "#00ff41",
              textShadow: "0 0 5px #00ff41, 0 0 10px #00ff41, 0 0 15px #00ff41",
              animation: "glitch 0.3s ease-in-out infinite alternate",
            }}
          >
            NEO<span style={{ color: "#ff0080" }}>TIC</span>
            <span style={{ color: "#00ffff" }}>TAC</span>
          </h1>
          <div className="text-sm text-cyan-400 font-mono mb-8">
            &gt; RETRO_MULTIPLAYER_TERMINAL.EXE
          </div>
        </header>

        {/* Main Content Grid */}
        <div className="flex-1 container mx-auto px-4 lg:px-8">
          <div className="grid lg:grid-cols-2 gap-8 items-start max-w-6xl mx-auto">
            {/* Left Column - System Overview */}
            <div className="order-2 lg:order-1">
              <div className="bg-gray-900/90 border border-green-400/50 rounded-lg p-6 backdrop-blur-sm">
                <h2 className="text-lg font-bold text-green-400 mb-4 neon-text font-mono">
                  &gt; SYSTEM_OVERVIEW
                </h2>

                <div className="space-y-3 text-white font-mono text-sm">
                  <p>
                    Enter the{" "}
                    <span className="text-cyan-400">digital battlefield</span>{" "}
                    where classic Tic Tac Toe meets{" "}
                    <span className="text-pink-500">real-time multiplayer</span>{" "}
                    combat.
                  </p>

                  <p className="text-gray-300">
                    Challenge players worldwide in this{" "}
                    <span className="text-green-400">retro-styled arena</span>{" "}
                    featuring dark cyberpunk aesthetics, neon-lit interfaces,
                    and seamless real-time synchronization.
                  </p>
                </div>

                {/* Features List */}
                <div className="mt-6 space-y-2">
                  <div className="flex items-center gap-2 text-green-400 font-mono text-sm">
                    <span className="text-blue-400">▣</span>
                    <span>Real-time multiplayer battles</span>
                  </div>
                  <div className="flex items-center gap-2 text-cyan-400 font-mono text-sm">
                    <span className="text-blue-400">▣</span>
                    <span>Retro cyberpunk aesthetic</span>
                  </div>
                  <div className="flex items-center gap-2 text-pink-500 font-mono text-sm">
                    <span className="text-blue-400">▣</span>
                    <span>Instant game room creation</span>
                  </div>
                  <div className="flex items-center gap-2 text-purple-400 font-mono text-sm">
                    <span className="text-blue-400">▣</span>
                    <span>Cross-platform compatibility</span>
                  </div>
                </div>
              </div>

              {/* CTA Buttons */}
              <div className="flex gap-4 mt-6">
                <Link
                  to="/login"
                  className="bg-transparent border-2 border-green-400 text-green-400 px-6 py-2 text-sm font-mono rounded hover:bg-green-400 hover:text-black transition-all duration-300 neon-text flex items-center gap-2"
                  role="button"
                  aria-label="Navigate to login page"
                >
                  🔐 LOGIN
                </Link>

                <Link
                  to="/register"
                  className="bg-transparent border-2 border-pink-500 text-pink-500 px-6 py-2 text-sm font-mono rounded hover:bg-pink-500 hover:text-black transition-all duration-300 neon-text flex items-center gap-2"
                  role="button"
                  aria-label="Navigate to registration page"
                >
                  ✨ SIGN UP
                </Link>
              </div>
            </div>

            {/* Right Column - Game Preview */}
            <div className="order-1 lg:order-2">
              <div className="cyber-card p-6 rounded-lg animate-float-path-reverse">
                <div className="terminal-window rounded-lg overflow-hidden">
                  <div className="bg-cyber-black p-4 pt-8">
                    <div className="text-neon-green font-mono text-sm mb-4">
                      &gt; GAME_PREVIEW.DISPLAY()
                    </div>{" "}
                    {/* Image Showcase */}
                    <div className="relative aspect-square bg-cyber-darker rounded-lg overflow-hidden neon-border">
                      <img
                        src={`/${gameImages[currentImageIndex]}`}
                        alt={`NeoTicTac gameplay preview ${
                          currentImageIndex + 1
                        }`}
                        className={`w-full h-full bg-center md:bg-top object-cover transition-opacity duration-1000 ${
                          imageLoaded ? "opacity-100" : "opacity-0"
                        }`}
                        onLoad={handleImageLoad}
                        onError={handleImageError}
                      />

                      {/* Fallback content - always visible, only hidden when image loads */}
                      <div
                        className={`absolute inset-0 flex items-center justify-center bg-cyber-darker transition-opacity duration-1000 ${
                          imageLoaded
                            ? "opacity-0 pointer-events-none"
                            : "opacity-100"
                        }`}
                      >
                        <div className="text-center text-neon-green font-mono">
                          <div className="text-6xl mb-4 animate-spin-reverse">
                            ⚡
                          </div>
                          <div className="text-lg">GAME PREVIEW</div>
                          <div className="text-sm text-neon-cyan mt-2">
                            Real-time Multiplayer Action
                          </div>
                        </div>
                      </div>
                    </div>
                    {/* Image Navigation Dots */}
                    <div className="flex justify-center gap-2 mt-4">
                      {gameImages.map((_, index) => (
                        <button
                          key={index}
                          onClick={() => setCurrentImageIndex(index)}
                          className={`w-2 h-2 rounded-full transition-all duration-300 ${
                            index === currentImageIndex
                              ? "bg-neon-green neon-glow"
                              : "bg-gray-600 hover:bg-gray-400"
                          }`}
                          aria-label={`View preview image ${index + 1}`}
                        />
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Bottom Section - Stats */}
        <div className="mt-8 pb-8 px-4">
          <div className="container mx-auto max-w-4xl">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-center">
              <div className="bg-gray-900/70 border border-green-400/30 p-4 rounded backdrop-blur-sm">
                <div className="text-2xl text-green-400 mb-1 neon-text font-mono">
                  ∞
                </div>
                <div className="text-green-400 font-mono text-xs">
                  UNLIMITED GAMES
                </div>
              </div>

              <div className="bg-gray-900/70 border border-pink-500/30 p-4 rounded backdrop-blur-sm">
                <div className="text-2xl text-pink-500 mb-1 neon-text font-mono">
                  ⚡
                </div>
                <div className="text-pink-500 font-mono text-xs">
                  REAL-TIME SYNC
                </div>
              </div>

              <div className="bg-gray-900/70 border border-cyan-400/30 p-4 rounded backdrop-blur-sm">
                <div className="text-2xl text-cyan-400 mb-1 neon-text font-mono">
                  🌐
                </div>
                <div className="text-cyan-400 font-mono text-xs">
                  GLOBAL PLAYERS
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <footer className="text-center pb-4 px-4">
          <div className="bg-black border border-green-400/50 p-3 rounded inline-block">
            <p className="text-xs text-green-400 font-mono">
              NEOTICTAC v2.1.0 • MULTIPLAYER_ENGINE_ACTIVE • RETRO_MODE_ENABLED
            </p>
          </div>
        </footer>
      </div>
    </div>
  );
};

export default LandingPage;
