import { useState, useRef } from "react";
import { motion } from "framer-motion";

import {
  FiPaperclip,
  FiSend,
  FiMic,
} from "react-icons/fi";

import UploadMenu from "./UploadMenu";
import { useTheme } from "../../context/ThemeContext";

function ChatInput({ onSend }) {
  const { darkMode } = useTheme();

  const [message, setMessage] = useState("");
  const [showMenu, setShowMenu] = useState(false);

  const pdfInputRef = useRef(null);
  const imageInputRef = useRef(null);
  const caseInputRef = useRef(null);

  const handleSend = () => {
    if (!message.trim()) return;

    onSend(message);
    setMessage("");
  };

  const handleFileSelect = (event, type) => {
    const file = event.target.files[0];

    if (!file) return;

    console.log(`${type} Selected:`, file);

    // Temporary feedback until backend integration
    setMessage((prev) =>
      prev
        ? `${prev}\n📎 ${file.name}`
        : `📎 ${file.name}`
    );

    setShowMenu(false);

    // Reset input so same file can be selected again
    event.target.value = "";
  };

  return (
    <div
      className={`p-5 border-t transition-all duration-300 ${
        darkMode
          ? "bg-slate-900 border-slate-700"
          : "bg-white border-slate-200"
      }`}
    >
      {/* Hidden Inputs */}

      <input
        ref={pdfInputRef}
        type="file"
        accept=".pdf"
        hidden
        onChange={(e) => handleFileSelect(e, "PDF")}
      />

      <input
        ref={imageInputRef}
        type="file"
        accept="image/*"
        hidden
        onChange={(e) => handleFileSelect(e, "Image")}
      />

      <input
        ref={caseInputRef}
        type="file"
        accept=".pdf,.doc,.docx,.txt,.zip,.rar"
        hidden
        onChange={(e) => handleFileSelect(e, "Case File")}
      />

      {/* Quick Actions */}

      <div className="flex flex-wrap gap-2 mb-4">
        {[
          "Summarize",
          "Similar Cases",
          "Explain Terms",
          "Timeline",
        ].map((item) => (
          <button
            key={item}
            className={`px-4 py-2 text-xs rounded-full transition ${
              darkMode
                ? "bg-slate-800 text-slate-300 hover:bg-slate-700"
                : "bg-slate-100 text-slate-600 hover:bg-slate-200"
            }`}
          >
            {item}
          </button>
        ))}
      </div>

      <div className="relative">
        {showMenu && (
          <UploadMenu
            onPdfUpload={() => pdfInputRef.current.click()}
            onImageUpload={() => imageInputRef.current.click()}
            onCaseUpload={() => caseInputRef.current.click()}
          />
        )}

        <div
          className={`flex items-center gap-3 rounded-3xl px-4 py-3 border transition-all duration-300 ${
            darkMode
              ? "bg-slate-800 border-slate-700"
              : "bg-slate-50 border-slate-200"
          }`}
        >
          <button
            onClick={() => setShowMenu(!showMenu)}
            className={`w-12 h-12 rounded-full flex items-center justify-center transition ${
              darkMode
                ? "hover:bg-slate-700"
                : "hover:bg-white"
            }`}
          >
            <FiPaperclip
              size={24}
              className={
                darkMode
                  ? "text-slate-300"
                  : "text-slate-600"
              }
            />
          </button>

          <input
  value={message}
  onChange={(e) => setMessage(e.target.value)}
  onKeyDown={(e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }}
  placeholder="Ask NyayaAI anything about law..."
  className={`flex-1 bg-transparent outline-none text-[15px] ${
    darkMode
      ? "text-white placeholder:text-slate-500"
      : "text-slate-800 placeholder:text-slate-400"
  }`}
/>

          <button
            className={`w-12 h-12 rounded-full flex items-center justify-center transition ${
              darkMode
                ? "hover:bg-slate-700"
                : "hover:bg-white"
            }`}
          >
            <FiMic
              size={22}
              className={
                darkMode
                  ? "text-slate-300"
                  : "text-slate-600"
              }
            />
          </button>

          <motion.button
            whileTap={{ scale: 0.92 }}
            onClick={handleSend}
            className="w-14 h-14 rounded-2xl bg-gradient-to-r from-[#2348C6] to-[#1E3A8A] text-white flex items-center justify-center shadow-lg"
          >
            <FiSend size={24} />
          </motion.button>
        </div>
      </div>
    </div>
  );
}

export default ChatInput;