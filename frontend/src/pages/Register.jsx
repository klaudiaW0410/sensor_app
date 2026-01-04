import { useState } from "react";
import { useNavigate } from "react-router-dom";


export const Register = () => {
    const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const navigate = useNavigate();

  const onRegisterClick = () => {
    if (!username || !email || !password) {
      alert("Uzupełnij wszystkie pola");
      return;
    }

    const user = { username, email };
    localStorage.setItem("user", JSON.stringify(user));

    alert("Rejestracja zakończona sukcesem");
    navigate("/");
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
