import { motion } from "framer-motion";
import { useTheme } from "../../context/ThemeContext";

function MessageBubble({ sender, text }) {
  const { darkMode } = useTheme();

  const isUser = sender === "user";

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className={`flex ${
        isUser ? "justify-end" : "justify-start"
      }`}
    >
      <div
        className={`max-w-[85%] rounded-3xl px-6 py-5 ${
          isUser
            ? "bg-blue-600 text-white"
            : darkMode
            ? "bg-slate-800 text-slate-100 border border-slate-700"
            : "bg-white text-slate-800 border border-slate-200"
        }`}
      >
        {!isUser && (
          <div className="flex items-center gap-2 mb-3">
            <span className="font-semibold">
              NyayaAI
            </span>
          </div>
        )}

        <p className="leading-8 whitespace-pre-wrap">
          {text}
        </p>
      </div>
    </motion.div>
  );
}

export default MessageBubble;