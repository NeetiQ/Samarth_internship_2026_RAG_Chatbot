import { Routes, Route } from "react-router-dom";
import { useTheme } from "./context/ThemeContext";

import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import CaseComparison from "./pages/CaseComparison";
import Chat from "./pages/Chat";
import Settings from "./pages/Settings";

function App() {
  const { darkMode } = useTheme();

  return (
    <div
      className={`min-h-screen transition-all duration-300 ${
        darkMode
          ? "bg-slate-950 text-slate-100"
          : "bg-slate-50 text-slate-900"
      }`}
    >
      <Routes>
        <Route path="/" element={<Login />} />

        <Route path="/dashboard" element={<Dashboard />} />

        <Route path="/compare" element={<CaseComparison />} />

        <Route path="/chat" element={<Chat />} />

        <Route path="/settings" element={<Settings />} />
      </Routes>
    </div>
  );
}

export default App;