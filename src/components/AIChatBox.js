// src/components/AIChatBox.js
import React, { useState } from "react";
import { askAI } from "../services/api";

const AIChatBox = () => {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);

  const handleAsk = async () => {
    if (!query.trim()) return;

    // Add user's question
    const newMessages = [...messages, { role: "user", text: query }];
    setMessages(newMessages);
    setQuery("");

    try {
      const res = await askAI(query);
      setMessages([...newMessages, { role: "ai", text: res.answer }]);
    } catch (error) {
      console.error("AI error:", error);
      setMessages([...newMessages, { role: "ai", text: "Something went wrong." }]);
    }
  };

  return (
    <div className="border p-4 rounded-xl shadow bg-white h-[400px] flex flex-col">
      <h2 className="text-lg font-bold mb-2">💬 Ask StockPulse AI</h2>

      <div className="flex-1 overflow-y-auto space-y-2 mb-2">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`p-2 rounded ${
              msg.role === "user" ? "bg-blue-100 text-right" : "bg-gray-100 text-left"
            }`}
          >
            {msg.text}
          </div>
        ))}
      </div>

      <div className="flex gap-2">
        <input
          type="text"
          placeholder="Ask something like 'Why is my portfolio down?'"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="flex-1 p-2 border rounded"
        />
        <button
          onClick={handleAsk}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Ask
        </button>
      </div>
    </div>
  );
};

export default AIChatBox;
