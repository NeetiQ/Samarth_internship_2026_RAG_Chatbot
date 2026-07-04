import { motion } from "framer-motion";

export default function LoadingAnalysis() {
  return (
    <div className="card">
      <h3>⚖️ NyayaAI Analysis Engine</h3>

      <motion.p
        animate={{ opacity: [0.4, 1, 0.4] }}
        transition={{ repeat: Infinity, duration: 1.5 }}
      >
        ✓ Retrieving Judgments...
      </motion.p>

      <motion.p
        animate={{ opacity: [0.4, 1, 0.4] }}
        transition={{ repeat: Infinity, duration: 1.5, delay: 0.2 }}
      >
        ✓ Extracting Legal Facts...
      </motion.p>

      <motion.p
        animate={{ opacity: [0.4, 1, 0.4] }}
        transition={{ repeat: Infinity, duration: 1.5, delay: 0.4 }}
      >
        ✓ Matching Precedents...
      </motion.p>

      <motion.p
        animate={{ opacity: [0.2, 1] }}
        transition={{ repeat: Infinity, duration: 1 }}
      >
        ⏳ Generating Legal Insight...
      </motion.p>
    </div>
  );
}