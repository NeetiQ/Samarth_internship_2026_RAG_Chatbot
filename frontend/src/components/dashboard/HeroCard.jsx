import { useTheme } from "../../context/ThemeContext";

function HeroCard() {
  const { darkMode } = useTheme();

  return (
    <div
      className={`mt-8 rounded-3xl border p-8 flex justify-between items-center transition-all duration-300 ${
        darkMode
          ? "bg-slate-900 border-slate-700"
          : "bg-white border-slate-200"
      }`}
    >
      <div>
        <h1
          className={`text-4xl font-bold ${
            darkMode
              ? "text-white"
              : "text-[#1E293B]"
          }`}
        >
          Good Morning, User 👋
        </h1>

        <p
          className={`mt-3 ${
            darkMode
              ? "text-slate-400"
              : "text-gray-500"
          }`}
        >
          Ready to analyze today's legal cases?
        </p>
      </div>

      <div className="flex gap-4">
        <button className="bg-[#2348C6] text-white px-6 py-3 rounded-2xl">
          Ask AI
        </button>

        <button
          className={`px-6 py-3 rounded-2xl border ${
            darkMode
              ? "border-blue-500 text-blue-400"
              : "border-[#2348C6] text-[#2348C6]"
          }`}
        >
          + New Case
        </button>
      </div>
    </div>
  );
}

export default HeroCard;