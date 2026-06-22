import { BrowserRouter, Routes, Route } from "react-router-dom";

import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import CaseComparison from "./pages/CaseComparison";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />

        <Route
          path="/dashboard"
          element={<Dashboard />}
        />

        <Route
          path="/compare"
          element={<CaseComparison />}
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;