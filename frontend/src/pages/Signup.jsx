
import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Signup() {
  const navigate = useNavigate();

  const API_URL = "http://localhost:8000";

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSignup = async (e) => {
    e.preventDefault();

    setLoading(true);

    try {
      const res = await fetch(`${API_URL}/register`, {
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
        alert(data.detail || "Signup failed");
        setLoading(false);
        return;
      }

      alert("Account created successfully! Please login.");

      navigate("/");

    } catch (error) {
      console.error(error);
      alert("Backend not reachable.");
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

        <form onSubmit={handleSignup}>

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

