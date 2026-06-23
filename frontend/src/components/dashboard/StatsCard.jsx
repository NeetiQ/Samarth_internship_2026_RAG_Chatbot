function StatsCard() {
const cards = [
{
title: "Total Judgements",
value: "248"
},
{
title: "Case Comparison Tool",
value: "12"
},
{
title: "AI Confidence",
value: "92%"
}
];

return ( <div className="grid md:grid-cols-3 gap-6 mt-8">
{cards.map((card) => ( <div
       key={card.title}
       className="bg-white rounded-3xl p-8 shadow-md"
     > <h1 className="text-4xl font-bold text-[#2348C6]">
{card.value} </h1>

      <p className="text-gray-500 mt-3">
        {card.title}
      </p>
    </div>
  ))}
</div>

);
}

export default StatsCard;
