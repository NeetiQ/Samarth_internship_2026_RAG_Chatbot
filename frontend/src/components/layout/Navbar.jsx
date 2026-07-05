import {
  FiBell,
  FiSearch,
  FiMoon,
  FiSun,
  FiChevronDown,
  FiSettings,
  FiLogOut,
  FiCheck,
  FiTrash2,
} from "react-icons/fi";

import { useTheme } from "../../context/ThemeContext";
import { useNavigate } from "react-router-dom";
import { useState, useRef, useEffect } from "react";

import {
  getNotifications,
  markAllAsRead,
  clearNotifications,
  unreadCount,
} from "../../utils/notifications";

function Navbar() {
  const { darkMode, toggleTheme } = useTheme();
  const navigate = useNavigate();

  // ==========================
  // Profile Menu
  // ==========================
  const [showMenu, setShowMenu] = useState(false);

  // ==========================
  // Notification Menu
  // ==========================
  const [showNotifications, setShowNotifications] =
    useState(false);

  const [notifications, setNotifications] = useState(
    getNotifications()
  );

  const [unread, setUnread] = useState(
    unreadCount()
  );

  const menuRef = useRef(null);
  const notificationRef = useRef(null);

  // ==========================
  // Logged-in User
  // ==========================
  const userEmail =
    localStorage.getItem("userEmail") ||
    "guest@nyayaai.com";

  const username = userEmail.split("@")[0];

  const initials = username.charAt(0).toUpperCase();

  // ==========================
  // Refresh Notifications
  // ==========================
  const refreshNotifications = () => {
    setNotifications(getNotifications());
    setUnread(unreadCount());
  };

  useEffect(() => {
    function handleClickOutside(event) {
      if (
        menuRef.current &&
        !menuRef.current.contains(event.target)
      ) {
        setShowMenu(false);
      }

      if (
        notificationRef.current &&
        !notificationRef.current.contains(event.target)
      ) {
        setShowNotifications(false);
      }
    }

    document.addEventListener(
      "mousedown",
      handleClickOutside
    );

    window.addEventListener(
      "notification-update",
      refreshNotifications
    );

    return () => {
      document.removeEventListener(
        "mousedown",
        handleClickOutside
      );

      window.removeEventListener(
        "notification-update",
        refreshNotifications
      );
    };
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("userEmail");

    navigate("/");
  };

  const handleMarkRead = () => {
    markAllAsRead();
    refreshNotifications();
  };

  const handleClear = () => {
    clearNotifications();
    refreshNotifications();
  };

  return (
    <div
      className={`flex justify-between items-center rounded-2xl px-6 py-4 transition-all duration-300 ${
        darkMode
          ? "bg-slate-900 border border-slate-800"
          : "bg-white border border-slate-200 shadow-sm"
      }`}
    >
      {/* Search */}
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
            darkMode
              ? "text-slate-400"
              : "text-slate-500"
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
                {/* ================= Notifications ================= */}
        <div className="relative" ref={notificationRef}>
          <button
            onClick={() =>
              setShowNotifications(!showNotifications)
            }
            className={`relative w-12 h-12 rounded-2xl border flex items-center justify-center transition-all duration-300 ${
              darkMode
                ? "bg-slate-950 border-slate-700 hover:bg-slate-800"
                : "bg-white border-slate-200 hover:bg-slate-100"
            }`}
          >
            <FiBell
              size={20}
              className={
                darkMode
                  ? "text-slate-300"
                  : "text-slate-600"
              }
            />

            {unread > 0 && (
              <span className="absolute -top-1 -right-1 min-w-[20px] h-5 px-1 rounded-full bg-blue-600 text-white text-[10px] font-bold flex items-center justify-center shadow-lg animate-pulse">
                {unread > 9 ? "9+" : unread}
              </span>
            )}
          </button>

          {showNotifications && (
            <div
              className={`absolute right-0 mt-4 w-[360px] rounded-2xl overflow-hidden border shadow-2xl z-50 ${
                darkMode
                  ? "bg-slate-900 border-slate-700"
                  : "bg-white border-slate-200"
              }`}
            >
              {/* Header */}
              <div
                className={`flex justify-between items-center px-5 py-4 border-b ${
                  darkMode
                    ? "border-slate-700"
                    : "border-slate-200"
                }`}
              >
                <div>
                  <h3
                    className={`font-bold text-lg ${
                      darkMode
                        ? "text-white"
                        : "text-slate-800"
                    }`}
                  >
                    Notifications
                  </h3>

                  <p
                    className={`text-xs ${
                      darkMode
                        ? "text-slate-400"
                        : "text-slate-500"
                    }`}
                  >
                    {notifications.length} notification
                    {notifications.length !== 1 && "s"}
                  </p>
                </div>

                {unread > 0 && (
                  <span className="px-2 py-1 rounded-full bg-blue-100 text-blue-600 text-xs font-semibold">
                    {unread} New
                  </span>
                )}
              </div>

              {notifications.length === 0 ? (
                <div className="py-12 text-center">
                  <div className="text-5xl mb-3">🎉</div>

                  <p
                    className={`font-semibold ${
                      darkMode
                        ? "text-white"
                        : "text-slate-800"
                    }`}
                  >
                    You're all caught up!
                  </p>

                  <p
                    className={`text-sm mt-2 ${
                      darkMode
                        ? "text-slate-400"
                        : "text-slate-500"
                    }`}
                  >
                    No new notifications.
                  </p>
                </div>
              ) : (
                <>
                  <div className="max-h-80 overflow-y-auto">
                    {notifications.map((item) => (
                      <div
                        key={item.id}
                        className={`px-5 py-4 border-b transition ${
                          darkMode
                            ? "border-slate-800 hover:bg-slate-800"
                            : "border-slate-100 hover:bg-slate-50"
                        }`}
                      >
                        <div className="flex gap-3">
                          <div className="text-2xl">
                            {item.icon}
                          </div>

                          <div className="flex-1">
                            <div className="flex justify-between">
                              <h4
                                className={`font-semibold ${
                                  darkMode
                                    ? "text-white"
                                    : "text-slate-800"
                                }`}
                              >
                                {item.title}
                              </h4>

                              {!item.read && (
                                <span className="w-2 h-2 rounded-full bg-blue-500 mt-2"></span>
                              )}
                            </div>

                            <p
                              className={`text-sm mt-1 ${
                                darkMode
                                  ? "text-slate-400"
                                  : "text-slate-500"
                              }`}
                            >
                              {item.message}
                            </p>

                            <p className="text-xs text-slate-400 mt-2">
                              {item.time}
                            </p>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>

                  <div
                    className={`grid grid-cols-2 border-t ${
                      darkMode
                        ? "border-slate-700"
                        : "border-slate-200"
                    }`}
                  >
                    <button
                      onClick={handleMarkRead}
                      className={`flex items-center justify-center gap-2 py-3 transition ${
                        darkMode
                          ? "hover:bg-slate-800 text-white"
                          : "hover:bg-slate-50 text-slate-700"
                      }`}
                    >
                      <FiCheck />
                      Mark all read
                    </button>

                    <button
                      onClick={handleClear}
                      className="flex items-center justify-center gap-2 py-3 text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 transition"
                    >
                      <FiTrash2 />
                      Clear all
                    </button>
                  </div>
                </>
              )}
            </div>
          )}
        </div>

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
                {/* ================= Profile ================= */}
        <div className="relative" ref={menuRef}>
          <button
            onClick={() => setShowMenu(!showMenu)}
            className={`flex items-center gap-3 px-3 py-2 rounded-2xl border transition ${
              darkMode
                ? "bg-slate-950 border-slate-700 hover:bg-slate-800"
                : "bg-white border-slate-200 hover:bg-slate-100"
            }`}
          >
            <div className="w-9 h-9 rounded-full bg-blue-600 text-white flex items-center justify-center font-bold">
              {initials}
            </div>

            <div className="text-left hidden sm:block">
              <p
                className={`text-sm font-semibold ${
                  darkMode ? "text-white" : "text-slate-800"
                }`}
              >
                {username}
              </p>
              <p
                className={`text-xs ${
                  darkMode ? "text-slate-400" : "text-slate-500"
                }`}
              >
                {userEmail}
              </p>
            </div>

            <FiChevronDown
              className={`transition ${
                showMenu ? "rotate-180" : ""
              } ${darkMode ? "text-slate-400" : "text-slate-600"}`}
            />
          </button>

          {/* Dropdown */}
          {showMenu && (
            <div
              className={`absolute right-0 mt-4 w-56 rounded-2xl border shadow-2xl z-50 overflow-hidden ${
                darkMode
                  ? "bg-slate-900 border-slate-700"
                  : "bg-white border-slate-200"
              }`}
            >
              <div className="px-4 py-3 border-b border-slate-200 dark:border-slate-700">
                <p
                  className={`text-sm font-semibold ${
                    darkMode ? "text-white" : "text-slate-800"
                  }`}
                >
                  Account
                </p>
                <p
                  className={`text-xs ${
                    darkMode ? "text-slate-400" : "text-slate-500"
                  }`}
                >
                  Manage your profile
                </p>
              </div>

              <button
                onClick={() => {
                  setShowMenu(false);
                  navigate("/settings");
                }}
                className={`w-full flex items-center gap-2 px-4 py-3 text-sm transition ${
                  darkMode
                    ? "hover:bg-slate-800 text-white"
                    : "hover:bg-slate-50 text-slate-700"
                }`}
              >
                <FiSettings />
                Settings
              </button>

              <button
                onClick={handleLogout}
                className="w-full flex items-center gap-2 px-4 py-3 text-sm text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 transition"
              >
                <FiLogOut />
                Logout
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Navbar;