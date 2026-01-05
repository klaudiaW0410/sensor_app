import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./SensorDetail.css";


export const Register = () => {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const navigate = useNavigate();

const onRegisterClick = async () => {
  try {
    const res = await fetch("http://localhost:8000/api/auth/register/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, email, password }),
    });

    if (!res.ok) {
      const error = await res.json();
      alert(error.detail || "Register error");
      return;
    }

    const data = await res.json();
    localStorage.setItem("token", data.token);

    alert("Registration successful");
    navigate("/sensors");
  } catch (error) {
     console.error("Error during registration:", error);
    alert("Server error");
  }
};


  return (
    <div className="container">
      <div className="card">
        <h2 className="title">Register</h2>

        <form>
          <label>Username</label>
          <input
            value={username}
            placeholder="Enter your username"
            onChange={(e) => setUsername(e.target.value)}
          />

          <label>Email</label>
          <input
            value={email}
            placeholder="Enter your email"
            onChange={(e) => setEmail(e.target.value)}
          />

          <label>Password</label>
          <input
            type="password"
            placeholder="Enter your password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <label>Confirm Password</label>
          <input
            type="password"
            placeholder="Confirm your password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          <button type="button" onClick={onRegisterClick}>
            Register
          </button>
        </form>
        <p className="signup">
          Already have an account? <a href="/">Sign in</a>
        </p>
      </div>
    </div>
  );
}
