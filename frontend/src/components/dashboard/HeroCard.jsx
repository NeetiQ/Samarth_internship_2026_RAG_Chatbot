function HeroCard() {
  return (
    <div
      className="
      mt-8
      rounded-[30px]
      p-10
      text-white
      bg-gradient-to-r
      from-[#1E3A8A]
      to-[#2348C6]
      "
    >
      <h1 className="text-4xl font-bold">
        Good Morning 👋
      </h1>

      <p className="mt-4 text-lg text-gray-200">
        Welcome back to NyayaAI Dashboard
      </p>

      <div className="flex gap-5 mt-8">
        <button className="bg-white text-[#2348C6] px-8 py-4 rounded-2xl font-bold">
          Ask AI
        </button>

        <button className="border border-white px-8 py-4 rounded-2xl">
          + New Case
        </button>
      </div>
    </div>
  );
}

export default HeroCard;