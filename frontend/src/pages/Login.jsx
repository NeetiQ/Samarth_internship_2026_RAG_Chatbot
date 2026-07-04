import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import "./Login.css";

export default function Login() {
  const navigate = useNavigate();

  const API_URL = import.meta.env.VITE_API_URL;

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleGoogleLogin = () => {
    alert("Google Login is not implemented yet.");
  };

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      // Clear any previous session
      localStorage.removeItem("token");
      localStorage.removeItem("userEmail");

     const res = await fetch(`${API_URL}/api/v1/auth/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
  },
      body: JSON.stringify({
        email,
        password,
  }),
});

      const data = await res.json();

      if (!res.ok) {
        alert(data.detail || "Login failed");
        return;
      }

      // Store login session
      localStorage.setItem("token", data.access_token);
      localStorage.setItem("userEmail", email);

      alert("Login Successful ✅");

      navigate("/dashboard");
    } catch (err) {
      console.error(err);
      alert("Backend not reachable");
    }
  };

  return (
    <div className="login-container">

      {/* Background Glow */}
      <div className="blob blob1"></div>
      <div className="blob blob2"></div>

      {/* Left Panel */}
      <motion.div
        className="left-panel"
        initial={{ x: -100, opacity: 0 }}
        animate={{ x: 0, opacity: 1 }}
        transition={{ duration: 0.8 }}
      >
        <div className="brand">
          <h1>⚖️ NyayaAI</h1>
          <p>Justice Meets Intelligence</p>
        </div>

        <div className="login-card">
          <h2>Welcome Back</h2>

          <form onSubmit={handleLogin}>

            <input
              type="email"
              placeholder="Email Address"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />

            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />

            <button type="submit">
              Sign In
            </button>

            <button
              className="google-btn"
              type="button"
              onClick={handleGoogleLogin}
            >
              Continue with Google
            </button>

          </form>

          <p className="signup-link">
            Don't have an account?{" "}
            <span
              style={{ cursor: "pointer" }}
              onClick={() => navigate("/signup")}
            >
              Sign Up
            </span>
          </p>
        </div>
      </motion.div>

      {/* Right Panel */}
      <motion.div
        className="right-panel"
        animate={{
          y: [0, -20, 0],
        }}
        transition={{
          repeat: Infinity,
          duration: 4,
        }}
      >
        <div className="illustration">
          <div className="justice-icon">⚖️</div>

          <h2>AI-Powered Legal Assistant</h2>

          <p>
            Analyze judgments, compare cases,
            generate summaries, and gain legal
            insights instantly.
          </p>

          <div className="quote">
            "Justice delayed is justice denied."
          </div>
        </div>
      </motion.div>

    </div>
  );
}