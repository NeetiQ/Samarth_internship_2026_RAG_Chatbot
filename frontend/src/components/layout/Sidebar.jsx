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
    `flex items-center gap-4 px-5 py-4 rounded-xl transition ${
      isActive
        ? "bg-blue-600 text-white"
        : darkMode
        ? "text-slate-300 hover:bg-slate-800"
        : "text-slate-600 hover:bg-slate-100"
    }`;

  return (
    <div
      className={`w-72 h-screen p-6 border-r flex flex-col ${
        darkMode
          ? "bg-slate-900 border-slate-800"
          : "bg-white border-slate-200"
      }`}
    >
      <h1 className="text-3xl font-bold text-blue-600">
        ⚖️ NyayaAI
      </h1>

      <div className="mt-10 space-y-2">
        <NavLink to="/dashboard" className={navItemClass}>
          <FiHome /> Dashboard
        </NavLink>

        <NavLink to="/chat" className={navItemClass}>
          <FiMessageSquare /> Chat
        </NavLink>

        <NavLink to="/compare" className={navItemClass}>
          <FiFileText /> Compare
        </NavLink>

        <NavLink to="/settings" className={navItemClass}>
          <FiSettings /> Settings
        </NavLink>
      </div>
    </div>
  );
}

export default Sidebar;