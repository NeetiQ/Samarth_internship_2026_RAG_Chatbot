import { useTheme } from "../../context/ThemeContext";

function TimelineCard() {
  const { darkMode } = useTheme();

  return (
    <div
      className={`rounded-3xl p-6 border transition-all duration-300 ${
        darkMode
          ? "bg-slate-900 border-slate-700"
          : "bg-white border-slate-200"
      }`}
    >
      <h2
        className={`text-xl font-bold mb-5 ${
          darkMode
            ? "text-white"
            : "text-slate-800"
        }`}
      >
        Timeline
      </h2>

      <p
        className={
          darkMode
            ? "text-slate-400"
            : "text-gray-400"
        }
      >
        No timeline data available.
      </p>
    </div>
  );
}

export default TimelineCard;