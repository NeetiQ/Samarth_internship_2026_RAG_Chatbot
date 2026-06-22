import { motion } from "framer-motion";
import "./Login.css";

export default function Login() {
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
          <h2>Welcome Back</h2>

          <form>
            <input type="email" placeholder="Email Address" />
            <input type="password" placeholder="Password" />

            <button type="submit">Sign In</button>

            <button className="google-btn" type="button">
              Continue with Google
            </button>
          </form>

          <p className="signup-link">
            Don't have an account? <span>Sign Up</span>
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