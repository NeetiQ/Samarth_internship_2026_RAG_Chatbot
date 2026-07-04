import { motion } from "framer-motion";
import { FiPlus, FiStar } from "react-icons/fi";
import { useTheme } from "../../context/ThemeContext";

function ConversationList({
  conversations,
  activeConversation,
  setActiveConversation,
}) {
  const { darkMode } = useTheme();

  return (
    <div
      className={`w-[340px] rounded-3xl border p-5 flex flex-col ${
        darkMode
          ? "bg-slate-900 border-slate-700"
          : "bg-white border-slate-200"
      }`}
    >
      <button className="w-full bg-gradient-to-r from-[#2348C6] to-[#1E3A8A] text-white py-4 rounded-2xl font-semibold flex items-center justify-center gap-2">
        <FiPlus size={20} />
        New Chat
      </button>

      <div className="mt-6 mb-4">
        <h3
          className={`text-lg font-bold ${
            darkMode ? "text-white" : "text-slate-800"
          }`}
        >
          Conversations
        </h3>

        <p
          className={
            darkMode ? "text-slate-400" : "text-slate-500"
          }
        >
          Recent legal discussions
        </p>
      </div>

      <div className="flex-1 overflow-y-auto space-y-3">
        {conversations.map((chat) => (
          <motion.div
            key={chat.id}
            whileHover={{ scale: 1.02 }}
            onClick={() =>
              setActiveConversation(chat)
            }
            className={`p-4 rounded-2xl border cursor-pointer ${
              activeConversation?.id === chat.id
                ? "bg-blue-600 text-white border-blue-600"
                : darkMode
                ? "bg-slate-800 border-slate-700 text-white"
                : "bg-white border-slate-200"
            }`}
          >
            <div className="flex justify-between">
              <div>
                <h4 className="font-medium">
                  {chat.title}
                </h4>

                <p
                  className={`text-xs mt-1 ${
                    activeConversation?.id ===
                    chat.id
                      ? "text-blue-100"
                      : darkMode
                      ? "text-slate-400"
                      : "text-slate-500"
                  }`}
                >
                  Legal Analysis
                </p>
              </div>

              {chat.bookmarked && (
                <FiStar
                  size={16}
                  className="text-yellow-400"
                />
              )}
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}

export default ConversationList;