import { useState } from "react";
import Sidebar from "../components/layout/Sidebar";
import Navbar from "../components/layout/Navbar";

import ConversationList from "../components/chat/ConversationList";
import ChatHeader from "../components/chat/ChatHeader";
import ChatWindow from "../components/chat/ChatWindow";
import ChatInput from "../components/chat/ChatInput";

import { useTheme } from "../context/ThemeContext";

function Chat() {
  const { darkMode } = useTheme();

  const [messages, setMessages] = useState([]);

  const [conversations] = useState([
    {
      id: 1,
      title: "Property Dispute",
      bookmarked: true,
    },
    {
      id: 2,
      title: "Criminal Appeal",
      bookmarked: false,
    },
    {
      id: 3,
      title: "Land Acquisition",
      bookmarked: true,
    },
    {
      id: 4,
      title: "Consumer Protection",
      bookmarked: false,
    },
    {
      id: 5,
      title: "Civil Petition",
      bookmarked: false,
    },
  ]);

  const [activeConversation, setActiveConversation] =
    useState(conversations[0]);

  const handleSendMessage = (text) => {
    if (!text.trim()) return;

    const userMessage = {
      id: Date.now(),
      sender: "user",
      text,
    };

    setMessages((prev) => [...prev, userMessage]);

    // Simulated AI Response
    setTimeout(() => {
      const aiMessage = {
        id: Date.now() + 1,
        sender: "ai",
        text: `Based on the uploaded legal documents and precedents, here is an analysis regarding "${text}". This response is currently simulated and will later connect to your AI backend.`,
      };

      setMessages((prev) => [...prev, aiMessage]);
    }, 2200);
  };

  return (
    <div
      className={`flex h-screen overflow-hidden transition-all duration-300 ${
        darkMode
          ? "bg-[#0B1120] text-white"
          : "bg-[#F8FAFC] text-slate-900"
      }`}
    >
      <Sidebar />

      <div className="flex-1 flex flex-col p-6 overflow-hidden">
        <Navbar />

        <div className="flex flex-1 gap-6 mt-6 min-h-0 pb-4">
          {/* Conversation List */}
          <ConversationList
            conversations={conversations}
            activeConversation={activeConversation}
            setActiveConversation={setActiveConversation}
          />

          {/* Chat Card */}
          <div
            className={`flex-1 rounded-3xl border overflow-hidden flex flex-col shadow-xl ${
              darkMode
                ? "bg-[#111827] border-[#1E293B]"
                : "bg-white border-slate-200"
            }`}
          >
            <ChatHeader
              messages={messages}
              conversation={activeConversation}
            />

            <ChatWindow messages={messages} />

            <ChatInput onSend={handleSendMessage} />
          </div>
        </div>
      </div>
    </div>
  );
}

export default Chat;