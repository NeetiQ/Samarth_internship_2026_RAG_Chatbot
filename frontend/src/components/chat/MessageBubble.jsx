import { motion } from "framer-motion";
import { useTheme } from "../../context/ThemeContext";

function MessageBubble({ sender, text, citations = [] }) {
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
        {!isUser && citations.length > 0 && (
          <div className="mt-4 space-y-2 border-t border-slate-200 pt-3 text-xs">
            {citations.map((citation, index) => (
              <div key={`${citation.chunk_id || index}`} className="leading-5 opacity-80">
                <span className="font-semibold">
                  {citation.chunk_id || `Citation ${index + 1}`}
                </span>
                {typeof citation.score === "number" && (
                  <span>
                    {` | score ${citation.score.toFixed(3)}`}
                  </span>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </motion.div>
  );
}

export default MessageBubble;
