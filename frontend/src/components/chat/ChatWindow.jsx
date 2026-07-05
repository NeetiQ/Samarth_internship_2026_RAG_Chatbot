import { useEffect, useRef } from "react";
import { motion } from "framer-motion";

import {
  FiFileText,
  FiSearch,
  FiBookOpen,
  FiClock,
} from "react-icons/fi";

import MessageBubble from "./MessageBubble";
import { useTheme } from "../../context/ThemeContext";

function ChatWindow({ messages }) {
  const { darkMode } = useTheme();

  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages]);

  const suggestions = [
    {
      icon: <FiFileText />,
      title: "Summarize Judgment",
      description:
        "Get a concise summary of any judgment",
    },
    {
      icon: <FiSearch />,
      title: "Find Similar Cases",
      description:
        "Discover related precedents instantly",
    },
    {
      icon: <FiBookOpen />,
      title: "Explain Legal Terms",
      description:
        "Understand complex legal concepts",
    },
    {
      icon: <FiClock />,
      title: "Generate Timeline",
      description:
        "Visualize case progression",
    },
  ];

  if (messages.length === 0) {
    return (
      <div
        className={`flex-1 overflow-y-auto transition-all duration-300 ${
          darkMode
            ? "bg-slate-950"
            : "bg-slate-50"
        }`}
      >
        <div className="h-full flex flex-col items-center justify-center px-8">
          {/* Hero */}

          <motion.div
            initial={{
              opacity: 0,
              y: 20,
            }}
            animate={{
              opacity: 1,
              y: 0,
            }}
            className="text-center"
          >
            <div className="text-7xl mb-5">
              ⚖️
            </div>

            <h1
              className={`text-3xl font-bold ${
                darkMode
                  ? "text-white"
                  : "text-slate-800"
              }`}
            >
              Ask NyayaAI
            </h1>

            <p
              className={`mt-3 max-w-xl text-sm leading-7 ${
                darkMode
                  ? "text-slate-400"
                  : "text-slate-500"
              }`}
            >
              Analyze judgments, compare cases,
              understand legal concepts and
              discover precedents using
              AI-powered legal assistance.
            </p>
          </motion.div>

          {/* Suggestions */}

          <div className="grid grid-cols-2 gap-4 mt-10 max-w-3xl w-full">
            {suggestions.map((item, index) => (
              <motion.div
                key={index}
                whileHover={{
                  y: -4,
                }}
                whileTap={{
                  scale: 0.98,
                }}
                className={`rounded-3xl p-5 cursor-pointer transition-all duration-300 border ${
                  darkMode
                    ? "bg-slate-900 border-slate-700 hover:border-blue-500"
                    : "bg-white border-slate-200 hover:border-blue-200"
                }`}
              >
                <div className="w-11 h-11 rounded-2xl bg-blue-50 text-[#2348C6] flex items-center justify-center text-lg mb-3">
                  {item.icon}
                </div>

                <h3
                  className={`font-semibold text-[15px] ${
                    darkMode
                      ? "text-white"
                      : "text-slate-800"
                  }`}
                >
                  {item.title}
                </h3>

                <p
                  className={`text-xs mt-2 leading-6 ${
                    darkMode
                      ? "text-slate-400"
                      : "text-slate-500"
                  }`}
                >
                  {item.description}
                </p>
              </motion.div>
            ))}
          </div>

          <div className="mt-10">
            <p
              className={`text-xs ${
                darkMode
                  ? "text-slate-500"
                  : "text-slate-400"
              }`}
            >
              Justice Meets Intelligence
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div
      className={`flex-1 overflow-y-auto transition-all duration-300 ${
        darkMode
          ? "bg-slate-950"
          : "bg-slate-50"
      }`}
    >
      <div className="max-w-3xl mx-auto p-6 space-y-5">
        {messages.map((message) => (
          <MessageBubble
            key={message.id}
            sender={message.sender}
            text={message.text}
          />
        ))}

        <div ref={bottomRef} />
      </div>
    </div>
  );
}

export default ChatWindow;