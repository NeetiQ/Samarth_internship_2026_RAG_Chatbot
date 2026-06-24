import {
  FiBell,
  FiSearch,
  FiMoon,
  FiSun,
} from "react-icons/fi";

import { useTheme } from "../../context/ThemeContext";

function Navbar() {
  const { darkMode, setDarkMode } = useTheme();

  return (
    <div className="flex justify-between items-center">
      {/* Search Bar */}

      <div
        className={`rounded-2xl px-5 py-3 flex items-center gap-3 w-[500px] border transition-all duration-300 ${
          darkMode
            ? "bg-slate-900 border-slate-700"
            : "bg-white border-slate-200"
        }`}
      >
        <FiSearch
          size={22}
          className={darkMode ? "text-slate-400" : "text-slate-500"}
        />

        <input
          type="text"
          placeholder="Search judgments, precedents..."
          className={`outline-none w-full bg-transparent ${
            darkMode
              ? "text-slate-200 placeholder:text-slate-500"
              : "text-slate-700 placeholder:text-slate-400"
          }`}
        />
      </div>

      {/* Actions */}

      <div className="flex items-center gap-4">
        <button
          className={`w-12 h-12 rounded-2xl border flex items-center justify-center transition ${
            darkMode
              ? "bg-slate-900 border-slate-700 hover:bg-slate-800"
              : "bg-white border-slate-200 hover:bg-slate-50"
          }`}
        >
          <FiBell
            size={22}
            className={darkMode ? "text-slate-300" : "text-slate-600"}
          />
        </button>

        <button
          onClick={() => setDarkMode(!darkMode)}
          className={`w-12 h-12 rounded-2xl border flex items-center justify-center transition ${
            darkMode
              ? "bg-slate-900 border-slate-700 hover:bg-slate-800"
              : "bg-white border-slate-200 hover:bg-slate-50"
          }`}
        >
          {darkMode ? (
            <FiSun size={22} className="text-yellow-400" />
          ) : (
            <FiMoon size={22} className="text-slate-600" />
          )}
        </button>

        <div className="w-12 h-12 rounded-full bg-gradient-to-br from-[#2348C6] to-[#1E3A8A] text-white flex items-center justify-center font-semibold">
          NAI
        </div>
      </div>
    </div>
  );
}

export default Navbar;