import { motion } from "framer-motion";
import { useTheme } from "../context/ThemeContext";

import Sidebar from "../components/layout/Sidebar";
import Navbar from "../components/layout/Navbar";

import SearchCaseBox from "../components/SearchCaseBox";
import SimilarityMeter from "../components/SimilarityMeter";
import ComparisonTable from "../components/ComparisonTable";
import AIInsights from "../components/AIInsights";
import TimelineComparison from "../components/TimelineComparison";
import LoadingAnalysis from "../components/LoadingAnalysis";

import "../styles/caseComparison.css";

export default function CaseComparison() {
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

        {/* ONLY CHANGE IS HERE */}
        <div
          className={`comparison-page ${
            darkMode ? "dark-theme" : ""
          }`}
        >
          {/* HERO */}
          <motion.div
            className={`hero-card ${
              darkMode ? "bg-slate-800 text-white" : ""
            }`}
            initial={{ opacity: 0, y: -15 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <h1>⚖️ NyayaAI</h1>

            <p>Justice Meets Intelligence</p>

            <div className="live-status">
              <span className="pulse"></span>
              AI Analysis Engine Active
            </div>
          </motion.div>

          {/* SEARCH */}
          <motion.div
            className={`card search-card ${
              darkMode ? "bg-slate-800 text-white" : ""
            }`}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
          >
            <SearchCaseBox />
          </motion.div>

          {/* TOP GRID */}
          <div className="top-grid">

            <motion.div
              className={`card similarity-card ${
                darkMode ? "bg-slate-800 text-white" : ""
              }`}
              whileHover={{ y: -4 }}
            >
              <SimilarityMeter />
            </motion.div>

            <motion.div
              className={`card analysis-card ${
                darkMode ? "bg-slate-800 text-white" : ""
              }`}
              whileHover={{ y: -4 }}
            >
              <LoadingAnalysis />
            </motion.div>

          </div>

          {/* INSIGHTS */}
          <motion.div
            className={`card ${
              darkMode ? "bg-slate-800 text-white" : ""
            }`}
            whileHover={{ y: -4 }}
          >
            <AIInsights />
          </motion.div>

          {/* COMPARISON */}
          <motion.div
            className={`card ${
              darkMode ? "bg-slate-800 text-white" : ""
            }`}
            whileHover={{ y: -4 }}
          >
            <h2>📑 Case Comparison Matrix</h2>

            <ComparisonTable />
          </motion.div>

          {/* TIMELINE */}
          <motion.div
            className={`card ${
              darkMode ? "bg-slate-800 text-white" : ""
            }`}
            whileHover={{ y: -4 }}
          >
            <h2>📅 Timeline Visualization</h2>

            <TimelineComparison />
          </motion.div>

        </div>
      </div>
    </div>
  );
}