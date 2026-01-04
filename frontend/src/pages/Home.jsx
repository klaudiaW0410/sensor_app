import { useState } from "react";
import "./Home.css";

 export const Home = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log({ email, password });
    // later: call login API
  };

  return (
    <div className="container">
      <div className="card">
        <h1 className="title">Welcome to Sensor App</h1>

        <form onSubmit={handleSubmit}>
          <label>Email</label>
          <input
            type="email"
            placeholder="Enter your email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />

          <label>Password</label>
          <input
            type="password"
            placeholder="Enter your password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          <button type="submit">Sign in</button>
        </form>

        <p className="signup">
          Don’t have an account? <a href="/register">Sign up</a>
        </p>
      </div>
    </div>
  );
};

