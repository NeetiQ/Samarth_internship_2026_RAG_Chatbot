import { Routes, Route } from "react-router-dom";

import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import CaseComparison from "./pages/CaseComparison";
import Settings from "./pages/Settings";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/compare" element={<CaseComparison />} />
      <Route path="/settings" element={<Settings />} />
    </Routes>
  );
}

export default App;