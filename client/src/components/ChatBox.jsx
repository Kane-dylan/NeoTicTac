import React, { useState, useRef, useEffect } from "react";

const ChatBox = ({ messages, sendMessage }) => {
  const [message, setMessage] = useState("");
  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (message.trim()) {
      sendMessage(message);
      setMessage("");
    }
  };

  return (
    <div className="border rounded p-4 h-80 flex flex-col">
      <div className="flex-1 overflow-y-auto mb-2 space-y-1">
        {messages.map((msg, index) => (
          <div key={msg.message_id || index} className="mb-1">
            <div className="flex justify-between items-start">
              <div>
                <strong className="text-sm font-semibold">
                  {msg.sender}:{" "}
                </strong>
                <span className="text-sm">{msg.text}</span>
              </div>
              {msg.timestamp && (
                <span className="text-xs text-gray-400 ml-2">
                  {new Date(msg.timestamp).toLocaleTimeString([], {
                    hour: "2-digit",
                    minute: "2-digit",
                  })}
                </span>
              )}
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          className="flex-1 border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Type a message..."
          maxLength={200}
        />
        <button
          type="submit"
          className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded text-sm font-medium disabled:bg-gray-400"
          disabled={!message.trim()}
        >
          Send
        </button>
      </form>
    </div>
  );
};

export default ChatBox;
