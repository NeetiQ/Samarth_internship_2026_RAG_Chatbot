import { useState } from "react";
import Sidebar from "../components/layout/Sidebar";

import ConversationList from "../components/chat/ConversationList";
import ChatHeader from "../components/chat/ChatHeader";
import ChatWindow from "../components/chat/ChatWindow";
import ChatInput from "../components/chat/ChatInput";

import { useTheme } from "../context/ThemeContext";
import { addNotification } from "../utils/notifications";

function Chat() {
  const { darkMode } = useTheme();

  // ==========================
  // Conversations
  // ==========================
  const [conversations, setConversations] = useState([
    { id: 1, title: "Property Dispute", bookmarked: true },
    { id: 2, title: "Criminal Appeal", bookmarked: false },
    { id: 3, title: "Land Acquisition", bookmarked: true },
    { id: 4, title: "Consumer Protection", bookmarked: false },
    { id: 5, title: "Civil Petition", bookmarked: false },
  ]);

  const [activeConversation, setActiveConversation] = useState(conversations[0]);

  // ==========================
  // Messages per conversation
  // ==========================
  const [messagesByConversation, setMessagesByConversation] = useState({});

  const messages =
    messagesByConversation[activeConversation?.id] || [];

  // ==========================
  // First message tracker
  // ==========================
  const [firstMessageMap, setFirstMessageMap] = useState({});

  // ==========================
  // ✅ NEW CHAT FIX (IMPORTANT)
  // ==========================
  const handleNewChat = () => {
    const newChat = {
      id: Date.now(),
      title: "New Chat",
      emoji: "⚖️",
      bookmarked: false,
    };

    setConversations((prev) => [newChat, ...prev]);
    setActiveConversation(newChat);

    setMessagesByConversation((prev) => ({
      ...prev,
      [newChat.id]: [],
    }));

    setFirstMessageMap((prev) => ({
      ...prev,
      [newChat.id]: false,
    }));
  };

  // ==========================
  // AI Title Generator (Frontend only)
  // ==========================
  const refineText = (text) => {
    return text
      .replace(/tell me about|explain|what is|how to/gi, "")
      .replace(/case/gi, "")
      .trim();
  };

  const generateTitle = (text) => {
    const clean = refineText(text).toLowerCase();

    const rules = [
      { keywords: ["property", "land", "house"], title: "Property dispute analysis", emoji: "🏠" },
      { keywords: ["criminal", "theft", "murder"], title: "Criminal law proceedings", emoji: "⚖️" },
      { keywords: ["appeal"], title: "Appeal case review", emoji: "📜" },
      { keywords: ["consumer"], title: "Consumer protection case", emoji: "🛒" },
      { keywords: ["timeline"], title: "Case timeline analysis", emoji: "⏱️" },
    ];

    for (let r of rules) {
      if (r.keywords.some((k) => clean.includes(k))) {
        return { title: r.title, emoji: r.emoji };
      }
    }

    const fallback =
      text.split(" ").slice(0, 5).join(" ") || "Legal discussion";

    return { title: fallback, emoji: "⚖️" };
  };

  // ==========================
  // Send Message
  // ==========================
  const handleSendMessage = (text) => {
    if (!text.trim()) return;

    const convId = activeConversation.id;

    // AI TITLE (ONLY FIRST MESSAGE)
    if (!firstMessageMap[convId]) {
      const aiTitle = generateTitle(text);

      setConversations((prev) =>
        prev.map((c) =>
          c.id === convId
            ? { ...c, title: aiTitle.title, emoji: aiTitle.emoji }
            : c
        )
      );

      setFirstMessageMap((prev) => ({
        ...prev,
        [convId]: true,
      }));
    }

    const userMessage = {
      id: Date.now(),
      sender: "user",
      text,
    };

    setMessagesByConversation((prev) => ({
      ...prev,
      [convId]: [...(prev[convId] || []), userMessage],
    }));

    setTimeout(() => {
      const aiMessage = {
        id: Date.now() + 1,
        sender: "ai",
        text: `Based on legal analysis regarding "${text}", this is a simulated response.`,
      };

      setMessagesByConversation((prev) => ({
        ...prev,
        [convId]: [...(prev[convId] || []), aiMessage],
      }));

      addNotification(
        "AI Response Ready",
        `Analysis generated for "${text}"`,
        "🤖"
      );
    }, 2000);
  };

  // ==========================
  // Quick actions
  // ==========================
  const handleQuickAction = (type) => {
    const actions = {
      summarize: "Summarize this conversation in legal terms.",
      similar: "Find similar legal cases for this discussion.",
      explain: "Explain legal terms used in this chat.",
      timeline: "Generate case timeline from this discussion.",
    };

    handleSendMessage(actions[type]);
  };

  return (
    <div
      className={`flex h-screen overflow-hidden transition-all duration-300 ${
        darkMode ? "bg-[#0B1120] text-white" : "bg-[#F8FAFC] text-slate-900"
      }`}
    >
      <Sidebar />

      <div className="flex-1 flex flex-col p-6 overflow-hidden">
        <div className="flex flex-1 gap-6 mt-6 min-h-0 pb-4">

          {/* ✅ FIX: NEW CHAT BUTTON NOW WORKS */}
          <ConversationList
            conversations={conversations}
            activeConversation={activeConversation}
            setActiveConversation={setActiveConversation}
            togglePin={() => {}}
            renameChat={() => {}}
            onNewChat={handleNewChat}
          />

          <div
            className={`flex-1 rounded-3xl border overflow-hidden flex flex-col shadow-xl ${
              darkMode
                ? "bg-[#111827] border-[#1E293B]"
                : "bg-white border-slate-200"
            }`}
          >
            <ChatHeader messages={messages} />

            <ChatWindow messages={messages} />

            <ChatInput
              onSend={handleSendMessage}
              onQuickAction={handleQuickAction}
            />
          </div>
        </div>
      </div>
    </div>
  );
}

export default Chat;