import { useTheme } from "../../context/ThemeContext";

function StatsCard() {
  const { darkMode } = useTheme();

  const cards = [
    {
      title: "Total Judgements",
      value: "248",
    },
    {
      title: "Case Comparison Tool",
      value: "12",
    },
    {
      title: "AI Confidence",
      value: "92%",
    },
  ];

  return (
    <div className="grid md:grid-cols-3 gap-6 mt-8">
      {cards.map((card) => (
        <div
          key={card.title}
          className={`rounded-3xl p-8 border transition-all duration-300 ${
            darkMode
              ? "bg-slate-900 border-slate-700"
              : "bg-white border-slate-200"
          }`}
        >
          <h1 className="text-4xl font-bold text-[#2348C6]">
            {card.value}
          </h1>

          <p
            className={`mt-3 ${
              darkMode
                ? "text-slate-400"
                : "text-gray-500"
            }`}
          >
            {card.title}
          </p>
        </div>
      ))}
    </div>
  );
}

export default StatsCard;