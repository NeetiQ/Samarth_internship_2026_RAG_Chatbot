import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Signup() {
  const navigate = useNavigate();

  const API_URL = import.meta.env.VITE_API_URL;

  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [messageType, setMessageType] = useState(""); // "success" or "error"

  const handleSignup = async (e) => {
    e.preventDefault();

    setLoading(true);
    setMessage("");

    try {
      const res = await fetch(`${API_URL}/api/v1/auth/signup`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email,
          password,
          full_name: fullName,
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        setMessageType("error");
        setMessage(data.detail || "Signup failed");
        setLoading(false);
        return;
      }

      setMessageType("success");
      setMessage("Account created successfully! Redirecting to login...");

      setTimeout(() => {
        navigate("/");
      }, 1500);

    } catch (error) {
      console.error(error);
      setMessageType("error");
      setMessage("Backend not reachable.");
    }

    setLoading(false);
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        background: "#0f172a",
      }}
    >
      <div
        style={{
          background: "#1e293b",
          padding: "40px",
          borderRadius: "15px",
          width: "350px",
          color: "white",
        }}
      >
        <h2 style={{ textAlign: "center", marginBottom: "25px" }}>
          Create Account
        </h2>

        {message && (
          <p
            style={{
              textAlign: "center",
              marginBottom: "15px",
              padding: "10px",
              borderRadius: "8px",
              fontSize: "14px",
              color: messageType === "success" ? "#4ade80" : "#f87171",
              background: messageType === "success" ? "#14532d33" : "#7f1d1d33",
            }}
          >
            {message}
          </p>
        )}

        <form onSubmit={handleSignup}>

          <input
            type="text"
            placeholder="Full Name"
            value={fullName}
            required
            onChange={(e) => setFullName(e.target.value)}
            style={{
              width: "100%",
              padding: "12px",
              marginBottom: "15px",
            }}
          />

          <input
            type="email"
            placeholder="Email"
            value={email}
            required
            onChange={(e) => setEmail(e.target.value)}
            style={{
              width: "100%",
              padding: "12px",
              marginBottom: "15px",
            }}
          />

          <input
            type="password"
            placeholder="Password"
            value={password}
            required
            onChange={(e) => setPassword(e.target.value)}
            style={{
              width: "100%",
              padding: "12px",
              marginBottom: "20px",
            }}
          />

          <button
            type="submit"
            disabled={loading}
            style={{
              width: "100%",
              padding: "12px",
              cursor: "pointer",
            }}
          >
            {loading ? "Creating Account..." : "Sign Up"}
          </button>

        </form>

        <p
          style={{
            textAlign: "center",
            marginTop: "20px",
          }}
        >
          Already have an account?{" "}
          <span
            style={{
              color: "#38bdf8",
              cursor: "pointer",
            }}
            onClick={() => navigate("/")}
          >
            Login
          </span>
        </p>
      </div>
    </div>
  );
}