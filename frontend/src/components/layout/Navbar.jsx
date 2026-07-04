import {
  FiBell,
  FiSearch,
  FiMoon,
  FiSun,
} from "react-icons/fi";

import { useTheme } from "../../context/ThemeContext";

function Navbar() {
  const { darkMode, toggleTheme } = useTheme();

  // Logged-in user's email
  const userEmail =
    localStorage.getItem("userEmail") || "guest@nyayaai.com";

  // Username before @
  const username = userEmail.split("@")[0];

  // Avatar initials
  const initials = username.charAt(0).toUpperCase();

  return (
    <div
      className={`flex justify-between items-center rounded-2xl px-6 py-4 transition-all duration-300 ${
        darkMode
          ? "bg-slate-900 border border-slate-800"
          : "bg-white border border-slate-200 shadow-sm"
      }`}
    >
      {/* Search Bar */}
      <div
        className={`flex items-center gap-3 px-5 py-3 rounded-2xl border w-[500px] transition ${
          darkMode
            ? "bg-slate-950 border-slate-700"
            : "bg-slate-50 border-slate-200"
        }`}
      >
        <FiSearch
          size={20}
          className={
            darkMode ? "text-slate-400" : "text-slate-500"
          }
        />

        <input
          type="text"
          placeholder="Search judgments, documents..."
          className={`bg-transparent outline-none w-full ${
            darkMode
              ? "text-white placeholder:text-slate-500"
              : "text-slate-700 placeholder:text-slate-400"
          }`}
        />
      </div>

      {/* Right Side */}
      <div className="flex items-center gap-4">

        {/* Notifications */}
        <button
          className={`w-12 h-12 rounded-2xl border flex items-center justify-center transition ${
            darkMode
              ? "bg-slate-950 border-slate-700 hover:bg-slate-800"
              : "bg-white border-slate-200 hover:bg-slate-100"
          }`}
        >
          <FiBell
            size={20}
            className={
              darkMode ? "text-slate-300" : "text-slate-600"
            }
          />
        </button>

        {/* Theme Toggle */}
        <button
          onClick={toggleTheme}
          className={`w-12 h-12 rounded-2xl border flex items-center justify-center transition ${
            darkMode
              ? "bg-slate-950 border-slate-700 hover:bg-slate-800"
              : "bg-white border-slate-200 hover:bg-slate-100"
          }`}
        >
          {darkMode ? (
            <FiSun
              size={20}
              className="text-yellow-400"
            />
          ) : (
            <FiMoon
              size={20}
              className="text-slate-600"
            />
          )}
        </button>

        {/* User Profile */}
        <div className="flex items-center gap-3 cursor-pointer">

          {/* User Details */}
          <div className="hidden md:block text-right">

            <h3
              className={`text-sm font-semibold ${
                darkMode
                  ? "text-white"
                  : "text-slate-800"
              }`}
            >
              {username}
            </h3>

            <p
              className={`text-xs ${
                darkMode
                  ? "text-slate-400"
                  : "text-slate-500"
              }`}
            >
              {userEmail}
            </p>

          </div>

          {/* Avatar */}
          <div
            className="w-12 h-12 rounded-full
            bg-gradient-to-br
            from-[#2563EB]
            via-[#1D4ED8]
            to-[#1E3A8A]
            flex items-center justify-center
            text-white
            font-bold
            text-lg
            shadow-lg"
          >
            {initials}
          </div>

        </div>

      </div>
    </div>
  );
}

export default Navbar;