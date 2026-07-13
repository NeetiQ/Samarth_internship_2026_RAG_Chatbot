import { useState, useEffect } from "react";
import Sidebar from "../components/layout/Sidebar";
import ChatHeader from "../components/chat/ChatHeader";
import ChatWindow from "../components/chat/ChatWindow";
import ChatInput from "../components/chat/ChatInput";
import { useTheme } from "../context/ThemeContext";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

function Chat() {
  const { darkMode } = useTheme();
  const [messages, setMessages] = useState([]);
  const [sessionId, setSessionId] = useState(null);
  const [errorMessage, setErrorMessage] = useState("");

  const authHeaders = () => ({
    "Content-Type": "application/json",
    Authorization: `Bearer ${localStorage.getItem("token")}`,
  });

  // Ek hi session banao jab page load ho
  useEffect(() => {
    const createSession = async () => {
      try {
        const res = await fetch(`${API_URL}/api/v1/chat/history`, {
          method: "POST",
          headers: authHeaders(),
        });
        const data = await res.json();
        setSessionId(data.id);
      } catch (err) {
        console.error(err);
        setErrorMessage("Could not start a chat session.");
      }
    };
    createSession();
  }, []);

  const handleSendMessage = async (text) => {
    if (!text.trim()) return;

    setErrorMessage("");
    setMessages((prev) => [...prev, { id: Date.now(), sender: "user", text }]);

    try {
      const res = await fetch(`${API_URL}/api/v1/chat`, {
        method: "POST",
        headers: authHeaders(),
        body: JSON.stringify({ message: text, session_id: sessionId }),
      });

      const data = await res.json();

      if (!res.ok) {
        setErrorMessage(data.detail || "Chat failed");
        return;
      }

      setMessages((prev) => [
        ...prev,
        { id: Date.now() + 1, sender: "ai", text: data.message.content },
      ]);
    } catch (err) {
      console.error(err);
      setErrorMessage("Backend not reachable");
    }
  };

  return (
    <div className={`flex h-screen overflow-hidden ${darkMode ? "bg-[#0B1120] text-white" : "bg-[#F8FAFC] text-slate-900"}`}>
      <Sidebar />
      <div className="flex-1 flex flex-col p-6 overflow-hidden">
        <div className={`flex-1 rounded-3xl border overflow-hidden flex flex-col shadow-xl mt-6 ${darkMode ? "bg-[#111827] border-[#1E293B]" : "bg-white border-slate-200"}`}>
          <ChatHeader messages={messages} />
          {errorMessage && (
            <div
              style={{
                textAlign: "center",
                padding: "8px",
                fontSize: "13px",
                color: "#f87171",
                background: "#7f1d1d33",
              }}
            >
              {errorMessage}
            </div>
          )}
          <ChatWindow messages={messages} />
          <ChatInput onSend={handleSendMessage} onQuickAction={() => {}} />
        </div>
      </div>
    </div>
  );
}

export default Chat;