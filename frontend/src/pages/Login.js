
import React, { useState, useContext } from "react";
import { useNavigate } from "react-router-dom"; // for navigation after login
import AuthContext from "../components/AuthContext"; // Import the AuthContext
import "../styles/Login.css";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const navigate = useNavigate(); // Navigate to different pages after login
  const { login } = useContext(AuthContext); // Access the login method from context

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch("http://localhost:5000/api/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (response.ok) {
        // Call the login method from context to update the login state
        const userRole = data.user_role;
        const token = data.token;
        login(userRole, token);

        // Redirect to the appropriate dashboard
        if (userRole === "Renter") {
          navigate("/renter-dashboard");
        } else if (userRole === "Owner") {
          navigate("/owner-dashboard");
        }
      } else {
        setErrorMessage(data.error || "Login failed. Please try again.");
      }
    } catch (error) {
      setErrorMessage("Something went wrong. Please try again later.");
    }
  };

  return (
    <div className="login-page">
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <br />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <br />
        <button type="submit">Login</button>
      </form>

      {errorMessage && <p>{errorMessage}</p>}
    </div>
  );
}

export default Login;
