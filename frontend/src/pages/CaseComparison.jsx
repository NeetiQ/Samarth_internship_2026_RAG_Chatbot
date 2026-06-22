import { motion } from "framer-motion";

import SearchCaseBox from "../components/SearchCaseBox";
import SimilarityMeter from "../components/SimilarityMeter";
import ComparisonTable from "../components/ComparisonTable";
import AIInsights from "../components/AIInsights";
import TimelineComparison from "../components/TimelineComparison";
import LoadingAnalysis from "../components/LoadingAnalysis";

import "../styles/caseComparison.css";

export default function CaseComparison() {
  return (
    <div className="comparison-page">

      {/* HERO */}
      <motion.div
        className="hero-card"
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
        className="card search-card"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
      >
        <SearchCaseBox />
      </motion.div>

      {/* TOP GRID */}
      <div className="top-grid">

        <motion.div
          className="card similarity-card"
          whileHover={{ y: -4 }}
        >
          <SimilarityMeter />
        </motion.div>

        <motion.div
          className="card analysis-card"
          whileHover={{ y: -4 }}
        >
          <LoadingAnalysis />
        </motion.div>

      </div>

      {/* INSIGHTS */}
      <motion.div
        className="card"
        whileHover={{ y: -4 }}
      >
        <AIInsights />
      </motion.div>

      {/* COMPARISON */}
      <motion.div
        className="card"
        whileHover={{ y: -4 }}
      >
        <h2>📑 Case Comparison Matrix</h2>
        <ComparisonTable />
      </motion.div>

      {/* TIMELINE */}
      <motion.div
        className="card"
        whileHover={{ y: -4 }}
      >
        <h2>📅 Timeline Visualization</h2>
        <TimelineComparison />
      </motion.div>

    </div>
  );
}

