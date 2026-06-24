import { motion } from "framer-motion";
import {
  FiDownload,
  FiMoreVertical,
  FiShield,
} from "react-icons/fi";

function ChatHeader() {
  return (
    <motion.div
      initial={{
        opacity: 0,
        y: -10,
      }}
      animate={{
        opacity: 1,
        y: 0,
      }}
      className="border-b border-slate-200 bg-white px-6 py-4 flex items-center justify-between"
    >
      {/* Left */}

      <div className="flex items-center gap-3">
        <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-[#1E3A8A] to-[#2563EB] text-white flex items-center justify-center shadow-md">
          <FiShield size={20} />
        </div>

        <div>
          <h2 className="text-lg font-bold text-slate-800">
            NyayaAI Assistant
          </h2>

          <div className="flex items-center gap-2 mt-1">
            <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>

            <span className="text-xs text-slate-500">
              Ready to Analyze Cases
            </span>
          </div>
        </div>
      </div>

      {/* Right */}

      <div className="flex items-center gap-3">
        <button className="flex items-center gap-2 px-3 py-2 rounded-xl border border-slate-200 hover:bg-slate-50 transition text-sm">
          <FiDownload size={16} />
          Export
        </button>

        <div className="flex items-center gap-2 px-3 py-2 rounded-2xl bg-slate-50 border border-slate-200">
          <div className="w-9 h-9 rounded-full bg-gradient-to-br from-[#2348C6] to-[#1E3A8A] text-white flex items-center justify-center font-semibold text-sm">
            NAI
          </div>

          <div>
            <p className="text-sm font-medium text-slate-800">
              Nyaya User
            </p>

            <p className="text-[11px] text-slate-500">
              Legal Workspace
            </p>
          </div>
        </div>

        <button className="w-9 h-9 rounded-xl border border-slate-200 flex items-center justify-center hover:bg-slate-50 transition">
          <FiMoreVertical size={16} />
        </button>
      </div>
    </motion.div>
  );
}

export default ChatHeader;