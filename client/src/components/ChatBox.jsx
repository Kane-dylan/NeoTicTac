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
    <div className="card h-80 flex flex-col">
      {/* Chat Header */}
      <div className="px-4 py-3 border-b border-border-light">
        <h3 className="font-semibold text-text-primary flex items-center gap-2">
          💬 Game Chat
          <span className="text-xs bg-background-tertiary text-text-secondary px-2 py-1 rounded-full">
            {messages.length} messages
          </span>
        </h3>
      </div>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto px-4 py-2 space-y-2">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-text-muted">
            <div className="text-2xl mb-2">💭</div>
            <p className="text-sm">No messages yet</p>
            <p className="text-xs">Start the conversation!</p>
          </div>
        ) : (
          messages.map((msg, index) => (
            <div key={msg.message_id || index} className="group">
              <div className="flex items-start gap-2">
                {/* Avatar */}
                <div className="flex items-center justify-center w-6 h-6 rounded-full bg-primary text-text-inverse text-xs font-medium">
                  {msg.sender.charAt(0).toUpperCase()}
                </div>

                {/* Message Content */}
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-sm font-medium text-text-primary truncate">
                      {msg.sender}
                    </span>
                    {msg.timestamp && (
                      <span className="text-xs text-text-muted opacity-0 group-hover:opacity-100 transition-opacity">
                        {formatTime(msg.timestamp)}
                      </span>
                    )}
                  </div>
                  <p className="text-sm text-text-secondary break-words">
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
        <div className="px-4 py-1 border-t border-border-light bg-background-secondary">
          <p className="text-xs text-text-muted italic">You are typing...</p>
        </div>
      )}

      {/* Input Form */}
      <form
        onSubmit={handleSubmit}
        className="p-4 border-t border-border-light"
      >
        <div className="flex gap-2">
          <input
            ref={inputRef}
            type="text"
            value={message}
            onChange={handleInputChange}
            className="flex-1 input-field text-sm"
            placeholder="Type a message..."
            maxLength={200}
          />
          <button
            type="submit"
            className="btn-primary px-4 py-2 text-sm font-medium disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
            disabled={!message.trim()}
          >
            <span className="hidden sm:inline">Send</span>
            <span className="sm:hidden">📤</span>
          </button>
        </div>

        {/* Character Count */}
        <div className="flex justify-between items-center mt-2">
          <div className="text-xs text-text-muted">Press Enter to send</div>
          <div className="text-xs text-text-muted">{message.length}/200</div>
        </div>
      </form>
    </div>
  );
};

export default ChatBox;
