import React from "react";

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    console.error("Error Boundary caught an error:", error, errorInfo);
  }

  handleReset = () => {
    this.setState({ hasError: false });
  };
  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen flex items-center justify-center bg-cyber-black">
          <div className="cyber-card p-8 max-w-md w-full mx-4">
            <div className="text-center">
              <div className="text-6xl mb-6 animate-neon-pulse">💥</div>
              <h2 className="text-2xl font-bold text-neon-green mb-4 neon-text font-mono">
                SYSTEM ERROR
              </h2>
              <p className="text-neon-cyan mb-6 leading-relaxed font-mono">
                {this.props.fallbackMessage ||
                  "We encountered an unexpected error. Don't worry, this happens sometimes in the digital world!"}
              </p>

              <div className="space-y-3">
                <button
                  onClick={this.handleReset}
                  className="btn-neon w-full py-3 font-mono"
                >
                  🔄 TRY AGAIN
                </button>
                <div className="flex gap-3">
                  <button
                    onClick={() => (window.location.href = "/lobby")}
                    className="btn-neon-cyan flex-1 py-2 font-mono"
                  >
                    🏠 LOBBY
                  </button>
                  <button
                    onClick={() => window.location.reload()}
                    className="btn-neon-pink flex-1 py-2 font-mono"
                  >
                    🔄 REFRESH
                  </button>
                </div>
              </div>

              <div className="mt-6 pt-6 border-t border-neon-green/30">
                <p className="text-xs text-text-muted font-mono">
                  // If this problem persists, try clearing your browser cache
                  or contact support.
                </p>
              </div>
            </div>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
