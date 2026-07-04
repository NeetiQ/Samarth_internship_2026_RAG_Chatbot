import { useState } from "react";
import Sidebar from "../components/layout/Sidebar";
import Navbar from "../components/layout/Navbar";
import { authFetch } from "../services/api";

import ConversationList from "../components/chat/ConversationList";
import ChatHeader from "../components/chat/ChatHeader";
import ChatWindow from "../components/chat/ChatWindow";
import ChatInput from "../components/chat/ChatInput";

import { useTheme } from "../context/ThemeContext";

function Chat() {
  const { darkMode } = useTheme();

  const [messages, setMessages] = useState([]);
  const [isTyping, setIsTyping] = useState(false);

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

  const handleSendMessage = async (text) => {
    if (!text.trim()) return;

    const userMessage = {
      id: Date.now(),
      sender: "user",
      text,
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsTyping(true);

    try {
      const response = await authFetch("/api/v1/chat", {
        method: "POST",
        body: JSON.stringify({ message: text, use_rag: true }),
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
      }

      const data = await response.json();
      
      const aiMessage = {
        id: Date.now() + 1,
        sender: "ai",
        text: data.message?.content || "No response generated.",
        citations: data.message?.citations || [],
      };

      setMessages((prev) => [...prev, aiMessage]);
    } catch (error) {
      console.error("Chat error:", error);
      const errorMessage = {
        id: Date.now() + 1,
        sender: "ai",
        text: "Sorry, I encountered an error while processing your request.",
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
    }
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

      <div className="flex-1 p-6 overflow-hidden">
        <Navbar />

        <div className="flex gap-6 mt-6 h-[calc(100vh-120px)]">
          <ConversationList
            conversations={conversations}
            activeConversation={activeConversation}
            setActiveConversation={setActiveConversation}
          />

          <div
            className={`flex-1 rounded-3xl border flex flex-col overflow-hidden transition-all duration-300 ${
              darkMode
                ? "bg-[#111827] border-[#1E293B]"
                : "bg-white border-slate-200"
            }`}
          >
            <ChatHeader />

            <ChatWindow messages={messages} isTyping={isTyping} />

            <ChatInput onSend={handleSendMessage} />
          </div>
        </div>
      </div>
    </div>
  );
}

export default Chat;
