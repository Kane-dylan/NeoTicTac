import React, { useState } from "react";

const ChatBox = ({ messages, sendMessage }) => {
  const [message, setMessage] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (message.trim()) {
      sendMessage(message);
      setMessage("");
    }
  };

  return (
    <div className="border rounded p-4">
      <div className="h-60 overflow-y-auto mb-2">
        {messages.map((msg, index) => (
          <div key={index} className="mb-1">
            <strong>{msg.sender}: </strong>
            {msg.text}
          </div>
        ))}
      </div>
      <form onSubmit={handleSubmit} className="flex">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          className="flex-grow border px-2 py-1"
          placeholder="Type a message..."
        />
        <button type="submit" className="bg-blue-500 text-white px-4 ml-2">
          Send
        </button>
      </form>
    </div>
  );
};

export default ChatBox;
