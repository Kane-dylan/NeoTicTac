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
        <div className="min-h-screen flex items-center justify-center bg-background-secondary">
          <div className="card p-8 max-w-md w-full mx-4">
            <div className="text-center">
              <div className="text-6xl mb-6">💥</div>
              <h2 className="text-2xl font-bold text-text-primary mb-4">
                Oops! Something went wrong
              </h2>
              <p className="text-text-secondary mb-6 leading-relaxed">
                {this.props.fallbackMessage ||
                  "We encountered an unexpected error. Don't worry, this happens sometimes in the digital world!"}
              </p>

              <div className="space-y-3">
                <button
                  onClick={this.handleReset}
                  className="btn-primary w-full py-3"
                >
                  🔄 Try Again
                </button>
                <div className="flex gap-3">
                  <button
                    onClick={() => (window.location.href = "/lobby")}
                    className="btn-secondary flex-1 py-2"
                  >
                    🏠 Go to Lobby
                  </button>
                  <button
                    onClick={() => window.location.reload()}
                    className="bg-accent-info hover:bg-accent-info/90 text-text-inverse flex-1 py-2 rounded-md font-medium transition-all duration-200"
                  >
                    🔄 Refresh
                  </button>
                </div>
              </div>

              <div className="mt-6 pt-6 border-t border-border-light">
                <p className="text-xs text-text-muted">
                  If this problem persists, try clearing your browser cache or
                  contact support.
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
