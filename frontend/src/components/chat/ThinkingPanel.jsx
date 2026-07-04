import { motion } from "framer-motion";

function ThinkingPanel() {
  const steps = [
    "Searching Judgments",
    "Extracting Facts",
    "Comparing Similar Cases",
    "Generating Response",
  ];

  return (
    <motion.div
      initial={{
        opacity: 0,
      }}
      animate={{
        opacity: 1,
      }}
      className="bg-white border border-slate-200 rounded-3xl p-5 shadow-sm max-w-md"
    >
      <div className="flex items-center gap-3 mb-4">
        <div className="w-10 h-10 rounded-full bg-gradient-to-r from-[#2348C6] to-[#1E3A8A] text-white flex items-center justify-center">
          ⚖
        </div>

        <div>
          <h4 className="font-semibold text-slate-800">
            NyayaAI is analyzing...
          </h4>

          <p className="text-sm text-slate-500">
            Please wait
          </p>
        </div>
      </div>

      <div className="space-y-3">
        {steps.map((step, index) => (
          <motion.div
            key={index}
            initial={{
              opacity: 0,
              x: -10,
            }}
            animate={{
              opacity: 1,
              x: 0,
            }}
            transition={{
              delay: index * 0.4,
            }}
            className="flex items-center gap-3"
          >
            <span className="text-green-500">
              ✓
            </span>

            <span className="text-slate-600 text-sm">
              {step}
            </span>
          </motion.div>
        ))}
      </div>
    </motion.div>
  );
}

export default ThinkingPanel;