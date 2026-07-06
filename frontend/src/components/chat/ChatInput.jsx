import { useState } from "react";
import { motion } from "framer-motion";
import { FiSend } from "react-icons/fi";
import { useTheme } from "../../context/ThemeContext";

function ChatInput({ onSend, onQuickAction }) {
  const { darkMode } = useTheme();

  const [message, setMessage] = useState("");

  const handleSend = () => {
    if (!message.trim()) return;

    onSend(message);
    setMessage("");
  };

  const quickActions = [
    { label: "Summarize", key: "summarize" },
    { label: "Similar Cases", key: "similar" },
    { label: "Explain Terms", key: "explain" },
    { label: "Timeline", key: "timeline" },
  ];

  return (
    <div className={`p-5 border-t ${darkMode ? "bg-slate-900" : "bg-white"}`}>
      
      {/* QUICK ACTIONS */}
      <div className="flex flex-wrap gap-2 mb-4">
        {quickActions.map((item) => (
          <button
            key={item.key}
            onClick={() => onQuickAction?.(item.key)}
            className={`px-4 py-2 text-xs rounded-full ${
              darkMode
                ? "bg-slate-800 text-white"
                : "bg-slate-100 text-slate-700"
            }`}
          >
            {item.label}
          </button>
        ))}
      </div>

      {/* INPUT */}
      <div className="flex items-center gap-3">
        <input
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") handleSend();
          }}
          placeholder="Ask NyayaAI..."
          className="flex-1 bg-transparent outline-none"
        />

        <motion.button
          onClick={handleSend}
          whileTap={{ scale: 0.9 }}
          className="px-4 py-2 bg-blue-600 text-white rounded-xl"
        >
          <FiSend />
        </motion.button>
      </div>
    </div>
  );
}

export default ChatInput;