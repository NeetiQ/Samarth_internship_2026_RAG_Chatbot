import Sidebar from "../components/layout/Sidebar";
import Navbar from "../components/layout/Navbar";
import HeroCard from "../components/dashboard/HeroCard";
import StatsCard from "../components/dashboard/StatsCard";
import TimelineCard from "../components/dashboard/TimelineCard";
import ConfidenceMeter from "../components/dashboard/ConfidenceMeter";
import CaseComparison from "../components/dashboard/CaseComparison";
import ActivityChart from "../components/dashboard/ActivityChart";

function Dashboard() {
  return (
    <div className="min-h-screen bg-[#F8FAFC] flex">
      <Sidebar />

      <div className="flex-1 p-8">
        <Navbar />

        <HeroCard />

        <StatsCard />

        <div className="grid lg:grid-cols-3 gap-6 mt-8">
          <TimelineCard />
          <ConfidenceMeter />
          <CaseComparison />
        </div>

        <ActivityChart />
      </div>
    </div>
  );
}

export default Dashboard;