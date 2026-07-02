import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Signup() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const navigate = useNavigate();

  const API_URL = "http://localhost:8000";

  const handleSignup = async (e) => {
    e.preventDefault();

    try {
      const res = await fetch(`${API_URL}/register`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          email: email,
          password: password
        })
      });

      const data = await res.json();
      console.log(data);

      if (!res.ok) {
        alert(data.detail || "Signup failed ❌");
        return;
      }

      alert("Signup successful 🚀 Now login");
      navigate("/"); // login page

    } catch (error) {
      console.log(error);
      alert("Server error ❌ Backend not reachable");
    }
  };

  return (
    <div style={{ padding: "50px" }}>
      <h2>Signup</h2>

      <form onSubmit={handleSignup}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <br /><br />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <br /><br />

        <button type="submit">Sign Up</button>
      </form>
    </div>
  );
}