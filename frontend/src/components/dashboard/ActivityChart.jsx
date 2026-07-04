import CaseStatusChart from "./CaseStatusChart";
import CaseTypeChart from "./CaseTypeChart";

function ActivityChart() {
  return (
    <div className="grid md:grid-cols-2 gap-6 mt-8">
      <CaseStatusChart />
      <CaseTypeChart />
    </div>
  );
}

export default ActivityChart;