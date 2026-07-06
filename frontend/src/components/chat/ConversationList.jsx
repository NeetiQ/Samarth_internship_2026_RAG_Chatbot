import { useState } from "react";
import { motion } from "framer-motion";
import { FiPlus, FiMoreVertical } from "react-icons/fi";
import { useTheme } from "../../context/ThemeContext";

function ConversationList({
  conversations,
  activeConversation,
  setActiveConversation,
  togglePin,
  renameChat,
  onNewChat,
}) {
  // eslint-disable-next-line no-unused-vars
  const _activeConversation = activeConversation;
  const { darkMode } = useTheme();

  const [openMenu, setOpenMenu] = useState(null);
  const [editId, setEditId] = useState(null);
  const [editText, setEditText] = useState("");

  return (
    <div
      className={`w-[340px] rounded-3xl border p-5 flex flex-col ${
        darkMode
          ? "bg-slate-900 border-slate-700"
          : "bg-white border-slate-200"
      }`}
    >
      {/* ✅ FIXED NEW CHAT BUTTON */}
      <button
        onClick={onNewChat}
        className="w-full bg-gradient-to-r from-[#2348C6] to-[#1E3A8A] text-white py-4 rounded-2xl font-semibold flex items-center justify-center gap-2"
      >
        <FiPlus size={20} />
        New Chat
      </button>

      <div className="mt-6 mb-4">
        <h3 className="text-lg font-bold">Conversations</h3>
      </div>

      <div className="flex-1 overflow-y-auto space-y-3">
        {conversations.map((chat) => (
          <motion.div
            key={chat.id}
            className={`relative group p-4 rounded-2xl border cursor-pointer ${
              activeConversation?.id === chat.id
                ? darkMode ? "border-blue-500 bg-slate-800" : "border-blue-500 bg-blue-50"
                : ""
  }`}
            onClick={() => setActiveConversation(chat)}
>
            {/* 3 DOT MENU */}
            <div className="absolute right-3 top-3 opacity-0 group-hover:opacity-100">
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  setOpenMenu(openMenu === chat.id ? null : chat.id);
                }}
              >
                <FiMoreVertical />
              </button>

              {openMenu === chat.id && (
                <div
                  className={`absolute right-0 mt-2 w-36 border rounded-lg shadow-lg z-50 ${
                    darkMode
                      ? "bg-slate-900 border-slate-700 text-white"
                      : "bg-white border-slate-200 text-slate-800"
                  }`}
                >
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      togglePin(chat.id);
                      setOpenMenu(null);
                    }}
                    className={`w-full px-3 py-2 text-sm text-left ${
                      darkMode
                        ? "hover:bg-slate-800"
                        : "hover:bg-slate-100"
                    }`}
                  >
                    {chat.pinned ? "Unpin" : "Pin Chat"}
                  </button>

                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      setEditId(chat.id);
                      setEditText(chat.title);
                      setOpenMenu(null);
                    }}
                    className={`w-full px-3 py-2 text-sm text-left ${
                      darkMode
                        ? "hover:bg-slate-800"
                        : "hover:bg-slate-100"
                    }`}
                  >
                    Rename
                  </button>
                </div>
              )}
            </div>

            {/* TITLE */}
            {editId === chat.id ? (
              <input
                value={editText}
                autoFocus
                onChange={(e) => setEditText(e.target.value)}
                onBlur={() => {
                  renameChat(chat.id, editText);
                  setEditId(null);
                }}
                onKeyDown={(e) => {
                  if (e.key === "Enter") {
                    renameChat(chat.id, editText);
                    setEditId(null);
                  }
                }}
                className="bg-transparent border-b outline-none w-full text-sm"
              />
            ) : (
              <h4 className="font-medium flex items-center gap-2">
                {chat.pinned && <span>📌</span>}
                {chat.emoji && <span>{chat.emoji}</span>}
                {chat.title}
              </h4>
            )}

            <p className="text-xs text-slate-500 mt-1">
              Legal Analysis
            </p>
          </motion.div>
        ))}
      </div>
    </div>
  );
}

export default ConversationList;