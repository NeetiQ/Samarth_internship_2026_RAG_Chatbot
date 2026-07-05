import { useState } from "react";
import { motion } from "framer-motion";
import Sidebar from "../components/layout/Sidebar";
import Navbar from "../components/layout/Navbar";
import { useTheme } from "../context/ThemeContext";

function Settings() {
  const { darkMode, setDarkMode } = useTheme();

  const [isEditing, setIsEditing] = useState(false);
  const [name, setName] = useState("Kairavi Malik");

  const handleSave = () => {
    // Later you can connect this to your backend API
    alert("Profile updated successfully!");
    setIsEditing(false);
  };

  return (
    <div
      className={`min-h-screen flex transition-all duration-300 ${
        darkMode ? "bg-slate-900" : "bg-[#F8FAFC]"
      }`}
    >
      <Sidebar />

      <div className="flex-1 p-8">
        <Navbar />

        <motion.div
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-8"
        >
          <h1
            className={`text-3xl font-bold mb-6 ${
              darkMode ? "text-white" : "text-[#1E293B]"
            }`}
          >
            ⚙️ Settings
          </h1>

          {/* Profile */}
          <motion.div
            whileHover={{ y: -4 }}
            className={`rounded-2xl shadow-md p-6 mb-6 ${
              darkMode ? "bg-slate-800 text-white" : "bg-white"
            }`}
          >
            <div className="flex justify-between items-center mb-5">
              <h2 className="text-2xl font-semibold">Profile</h2>

              <button
                onClick={() => setIsEditing(true)}
                className="bg-[#2563EB] text-white px-4 py-2 rounded-xl hover:bg-blue-700 transition"
              >
                Edit
              </button>
            </div>

            <div className="flex items-center gap-6">
              <div className="w-24 h-24 rounded-full bg-[#1E293B] text-white flex items-center justify-center text-2xl font-bold">
                KM
              </div>

              <div className="grid md:grid-cols-2 gap-4 flex-1">
                <input
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  disabled={!isEditing}
                  className={`border rounded-xl p-3 transition ${
                    darkMode
                      ? "bg-slate-700 text-white border-slate-600"
                      : "bg-white"
                  } ${
                    !isEditing
                      ? "opacity-70 cursor-not-allowed"
                      : ""
                  }`}
                  placeholder="Name"
                />

                <input
                  type="email"
                  value="kairavi@email.com"
                  readOnly
                  className={`border rounded-xl p-3 ${
                    darkMode
                      ? "bg-slate-700 text-white border-slate-600"
                      : "bg-white"
                  } opacity-70 cursor-not-allowed`}
                />
              </div>
            </div>

            <button
              onClick={handleSave}
              disabled={!isEditing}
              className={`mt-5 px-6 py-3 rounded-xl text-white transition ${
                isEditing
                  ? "bg-[#D4A017] hover:opacity-90"
                  : "bg-gray-400 cursor-not-allowed"
              }`}
            >
              Save Changes
            </button>
          </motion.div>

          {/* Notifications */}
          <motion.div
            whileHover={{ y: -4 }}
            className={`rounded-2xl shadow-md p-6 mb-6 ${
              darkMode ? "bg-slate-800 text-white" : "bg-white"
            }`}
          >
            <h2 className="text-2xl font-semibold mb-4">
              Notifications
            </h2>

            <div className="space-y-4">
              <div className="flex justify-between">
                <span>Email Alerts</span>
                <input type="checkbox" defaultChecked />
              </div>

              <div className="flex justify-between">
                <span>SMS Alerts</span>
                <input type="checkbox" />
              </div>

              <div className="flex justify-between">
                <span>AI Recommendations</span>
                <input type="checkbox" defaultChecked />
              </div>
            </div>
          </motion.div>
                   {/* Security */}
          <motion.div
            whileHover={{ y: -4 }}
            className={`rounded-2xl shadow-md p-6 mb-6 ${
              darkMode ? "bg-slate-800 text-white" : "bg-white"
            }`}
          >
            <h2 className="text-2xl font-semibold mb-4">
              Security
            </h2>

            <div className="flex justify-between items-center">
              <span>Change Password</span>

              <button className="bg-[#2563EB] text-white px-4 py-2 rounded-xl hover:bg-blue-700 transition">
                Update
              </button>
            </div>
          </motion.div>

          {/* Appearance */}
          <motion.div
            whileHover={{ y: -4 }}
            className={`rounded-2xl shadow-md p-6 ${
              darkMode ? "bg-slate-800 text-white" : "bg-white"
            }`}
          >
            <h2 className="text-2xl font-semibold mb-4">
              Appearance
            </h2>

            <div className="flex justify-between items-center">
              <span>Dark Mode</span>

              <input
                type="checkbox"
                checked={darkMode}
                onChange={() => setDarkMode(!darkMode)}
              />
            </div>
          </motion.div>
        </motion.div>
      </div>
    </div>
  );
}

export default Settings; 