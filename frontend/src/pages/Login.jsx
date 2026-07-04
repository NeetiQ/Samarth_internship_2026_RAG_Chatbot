import { useState } from "react";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import "./Login.css";

export default function Login() {
  const navigate = useNavigate();
  const { login, signup } = useAuth();

  const [isSignup, setIsSignup] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      if (isSignup) {
        await signup(email, password, fullName);
      } else {
        await login(email, password);
      }
      navigate("/dashboard");
    } catch (err) {
      setError(err.message || "Authentication failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">

      {/* Background Glow */}
      <div className="blob blob1"></div>
      <div className="blob blob2"></div>

      {/* Left Side */}
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
          <h2>{isSignup ? "Create Account" : "Welcome Back"}</h2>

          {error && (
            <div style={{
              color: "#dc2626",
              background: "#fef2f2",
              padding: "10px 14px",
              borderRadius: "8px",
              marginBottom: "16px",
              fontSize: "14px",
            }}>
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit}>
            {isSignup && (
              <input
                type="text"
                placeholder="Full Name"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
              />
            )}
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
              minLength={6}
            />

            <button type="submit" disabled={loading}>
              {loading ? "Please wait..." : isSignup ? "Create Account" : "Sign In"}
            </button>
          </form>

          <p className="signup-link">
            {isSignup ? "Already have an account? " : "Don't have an account? "}
            <span onClick={() => { setIsSignup(!isSignup); setError(""); }}>
              {isSignup ? "Sign In" : "Sign Up"}
            </span>
          </p>
        </div>
      </motion.div>

      {/* Right Side */}
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
            Analyze judgments, compare cases, generate summaries,
            and gain legal insights instantly.
          </p>

          <div className="quote">
            "Justice delayed is justice denied."
          </div>
        </div>
      </motion.div>
    </div>
  );
}