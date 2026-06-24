import {
  FiHome,
  FiMessageSquare,
  FiFileText,
  FiSettings,
} from "react-icons/fi";

import { NavLink } from "react-router-dom";
import { useTheme } from "../../context/ThemeContext";

function Sidebar() {
  const { darkMode } = useTheme();

  const navItemClass = ({ isActive }) =>
    `flex items-center gap-4 px-5 py-4 rounded-2xl transition-all duration-300 ${
      isActive
        ? "bg-blue-600 text-white font-semibold"
        : darkMode
        ? "text-slate-300 hover:bg-slate-800"
        : "text-slate-500 hover:bg-slate-100"
    }`;

  return (
    <div
      className={`w-80 border-r p-7 flex flex-col transition-all duration-300 ${
        darkMode
          ? "bg-slate-900 border-slate-700"
          : "bg-white border-slate-200"
      }`}
    >
      <div>
        <h1
          className={`text-4xl font-bold ${
            darkMode ? "text-white" : "text-[#1E3A8A]"
          }`}
        >
          ⚖️ NyayaAI
        </h1>

        <p
          className={`mt-2 text-sm ${
            darkMode ? "text-slate-400" : "text-slate-500"
          }`}
        >
          Justice Meets Intelligence
        </p>
      </div>

      <div className="mt-12 space-y-3">
        <NavLink to="/dashboard" className={navItemClass}>
          <FiHome size={22} />
          Dashboard
        </NavLink>

        <NavLink to="/chat" className={navItemClass}>
          <FiMessageSquare size={22} />
          Chat Assistant
        </NavLink>

        <NavLink to="/compare" className={navItemClass}>
          <FiFileText size={22} />
          Case Comparison
        </NavLink>

        <NavLink to="/settings" className={navItemClass}>
          <FiSettings size={22} />
          Settings
        </NavLink>
      </div>

      <div className="mt-auto">
        <div className="bg-gradient-to-br from-[#1E3A8A] via-[#2348C6] to-[#3B82F6] rounded-3xl p-6 text-white shadow-xl">
          <h3 className="font-semibold text-lg">
            Legal Insight
          </h3>

          <p className="text-sm text-blue-100 mt-3 leading-relaxed">
            Property disputes accounted for 42% of retrieved judgments this month.
          </p>
        </div>
      </div>
    </div>
  );
}

export default Sidebar;