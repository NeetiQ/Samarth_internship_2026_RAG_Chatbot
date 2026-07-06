import Sidebar from "../components/layout/Sidebar";
import Navbar from "../components/layout/Navbar";
import HeroCard from "../components/dashboard/HeroCard";
import StatsCard from "../components/dashboard/StatsCard";
import TimelineCard from "../components/dashboard/TimelineCard";

import ActivityChart from "../components/dashboard/ActivityChart";
import { useTheme } from "../context/ThemeContext";

function Dashboard() {
  const { darkMode } = useTheme();

  return (
    <div
      className={`min-h-screen flex transition-all duration-300 ${
        darkMode ? "bg-slate-900" : "bg-[#F8FAFC]"
      }`}
    >
      <Sidebar />

      <div className="flex-1 p-8">
        <Navbar />

        <HeroCard />

        <div
          className={`mt-5 rounded-2xl shadow-md p-4 ${
            darkMode ? "bg-slate-800 text-white" : "bg-white"
          }`}
        >
          <h3
            className={`font-semibold ${
              darkMode ? "text-white" : "text-[#1E293B]"
            }`}
          >
            Latest Judgement Thoughts
          </h3>

          <p
            className={`mt-2 ${
              darkMode ? "text-gray-300" : "text-gray-500"
            }`}
          >
            AI generated legal insights and recent precedent summaries appear
            here.
          </p>
        </div>

        <StatsCard />

        <div className="grid lg:grid-cols-4 gap-6 mt-8">
          <div className="lg:col-span-3">
            <ActivityChart />
          </div>

          <div>
            <TimelineCard />
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;