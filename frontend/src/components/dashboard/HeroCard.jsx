import { useTheme } from "../../context/ThemeContext";
import { useNavigate } from "react-router-dom";

function HeroCard() {
  const { darkMode } = useTheme();
  const navigate = useNavigate();

  // Dynamic Greeting
  const hour = new Date().getHours();

  let greeting = "Good Morning";
  let subText = "Start your day by analyzing legal cases with AI.";

  if (hour >= 12 && hour < 17) {
    greeting = "Good Afternoon";
    subText = "Let's continue working on your legal research.";
  } else if (hour >= 17 && hour < 21) {
    greeting = "Good Evening";
    subText = "Finish today's legal work with AI assistance.";
  } else if (hour >= 21 || hour < 5) {
    greeting = "Good Night";
    subText = "Need late-night legal assistance? I'm here to help.";
  }

  return (
    <div
      className={`mt-8 rounded-3xl border p-8 flex justify-between items-center transition-all duration-300 ${
        darkMode
          ? "bg-slate-900 border-slate-700"
          : "bg-white border-slate-200"
      }`}
    >
      {/* Left Section */}
      <div>
        <h1
          className={`text-4xl font-bold ${
            darkMode ? "text-white" : "text-[#1E293B]"
          }`}
        >
          {greeting}, User 👋
        </h1>

        <p
          className={`mt-3 text-lg ${
            darkMode ? "text-slate-400" : "text-gray-500"
          }`}
        >
          {subText}
        </p>
      </div>

      {/* Right Section */}
      <div className="relative">
        {/* Glow Effect */}
        <div className="absolute inset-0 rounded-2xl bg-blue-500 blur-2xl opacity-40 animate-pulse"></div>

        <button
          onClick={() => navigate("/chat")}
          className="
            relative
            overflow-hidden
            px-8
            py-3.5
            rounded-2xl
            font-semibold
            text-white
            bg-gradient-to-r
            from-[#2348C6]
            via-[#3B82F6]
            to-[#2563EB]
            shadow-xl
            shadow-blue-500/40
            transition-all
            duration-300
            hover:scale-105
            hover:shadow-2xl
            hover:shadow-blue-500/70
            active:scale-95
          "
        >
          <span className="relative z-10 flex items-center gap-2">
            🤖 Ask AI
          </span>

          {/* Shine Animation */}
          <span
            className="
              absolute
              inset-0
              bg-white/20
              -translate-x-full
              hover:translate-x-full
              transition-transform
              duration-700
              skew-x-12
            "
          ></span>
        </button>
      </div>
    </div>
  );
}

export default HeroCard;