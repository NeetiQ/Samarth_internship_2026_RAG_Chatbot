function HeroCard() {
return ( <div className="mt-8 bg-white rounded-3xl shadow-md p-8 flex justify-between items-center"> <div> <h1 className="text-4xl font-bold text-[#1E293B]">
Good Morning, User 👋 </h1>

    <p className="mt-3 text-gray-500">
      Ready to analyze today's legal cases?
    </p>
  </div>

  <div className="flex gap-4">
    <button className="bg-[#2348C6] text-white px-6 py-3 rounded-2xl">
      Ask AI
    </button>

    <button className="border border-[#2348C6] text-[#2348C6] px-6 py-3 rounded-2xl">
      + New Case
    </button>
  </div>
</div>

);
}

export default HeroCard;
