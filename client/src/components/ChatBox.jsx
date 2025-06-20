import React, { useState, useRef, useEffect } from "react";

const ChatBox = ({ messages, sendMessage }) => {
  const [message, setMessage] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (message.trim()) {
      sendMessage(message);
      setMessage("");
      setIsTyping(false);
    }
  };

  const handleInputChange = (e) => {
    setMessage(e.target.value);
    setIsTyping(e.target.value.length > 0);
  };

  const formatTime = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });
  };
  return (
    <div className="cyber-card h-80 flex flex-col font-mono">
      {/* Chat Header */}
      <div className="px-4 py-3 border-b border-neon-green/30 bg-cyber-darker">
        <h3 className="font-bold text-neon-green flex items-center gap-2 neon-text uppercase tracking-wider">
          💬 COMM CHANNEL
          <span className="text-xs bg-cyber-black text-neon-cyan px-2 py-1 rounded-full border border-neon-cyan">
            {messages.length} MSG
          </span>
        </h3>
      </div>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto px-4 py-2 space-y-2 bg-cyber-black/50">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-neon-cyan">
            <div className="text-2xl mb-2 animate-neon-pulse">💭</div>
            <p className="text-sm font-mono uppercase">CHANNEL EMPTY</p>
            <p className="text-xs font-mono opacity-70">
              // START TRANSMISSION
            </p>
          </div>
        ) : (
          messages.map((msg, index) => (
            <div key={msg.message_id || index} className="group">
              <div className="flex items-start gap-2">
                {/* Avatar */}
                <div className="flex items-center justify-center w-6 h-6 rounded-full bg-neon-green text-cyber-black text-xs font-bold border border-neon-green">
                  {msg.sender.charAt(0).toUpperCase()}
                </div>

                {/* Message Content */}
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-sm font-bold text-neon-green truncate uppercase">
                      {msg.sender}
                    </span>
                    {msg.timestamp && (
                      <span className="text-xs text-neon-cyan opacity-0 group-hover:opacity-100 transition-opacity font-mono">
                        [{formatTime(msg.timestamp)}]
                      </span>
                    )}
                  </div>
                  <p className="text-sm text-text-primary break-words bg-cyber-darker/50 p-2 rounded border border-neon-green/20">
                    {msg.text}
                  </p>
                </div>
              </div>
            </div>
          ))
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Typing Indicator */}
      {isTyping && (
        <div className="px-4 py-1 border-t border-neon-green/30 bg-cyber-darker">
          <p className="text-xs text-neon-cyan font-mono animate-neon-flicker">
            &gt; USER_TYPING...
          </p>
        </div>
      )}

      {/* Input Form */}
      <form
        onSubmit={handleSubmit}
        className="p-4 border-t border-neon-green/30 bg-cyber-darker"
      >
        <div className="flex gap-2">
          <input
            ref={inputRef}
            type="text"
            value={message}
            onChange={handleInputChange}
            className="flex-1 cyber-input text-sm p-2 font-mono"
            placeholder="enter.message..."
            maxLength={200}
          />
          <button
            type="submit"
            className="btn-neon-cyan px-4 py-2 text-sm font-bold disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
            disabled={!message.trim()}
          >
            <span className="hidden sm:inline">SEND</span>
            <span className="sm:hidden">📤</span>
          </button>
        </div>

        {/* Character Count */}
        <div className="flex justify-between items-center mt-2">
          <div className="text-xs text-neon-cyan font-mono">
            // ENTER TO TRANSMIT
          </div>
          <div className="text-xs text-neon-cyan font-mono">
            {message.length}/200
          </div>
        </div>
      </form>
    </div>
  );
};

export default ChatBox;
