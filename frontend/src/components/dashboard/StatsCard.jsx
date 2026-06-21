function StatsCard() {
  const cards = [
    { title: "Active Cases" },
    { title: "Documents" },
    { title: "Win Rate" },
    { title: "AI Insights" },
  ];

  return (
    <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mt-8">
      {cards.map((card) => (
        <div
          key={card.title}
          className="
          bg-white
          rounded-3xl
          p-8
          shadow-md
          "
        >
          <h1 className="text-5xl font-bold text-gray-300">
            --
          </h1>

          <p className="text-gray-500 mt-3">
            {card.title}
          </p>
        </div>
      ))}
    </div>
  );
}

export default StatsCard;