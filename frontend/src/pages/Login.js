import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "../styles/Login.css";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      // Clear previous error messages
      setErrorMessage("");

      // Send login request to server
      const response = await axios.post("http://localhost:3000/login", {
        email,
        password,
      });

      // If login is successful, redirect to Dashboard
      if (response.status === 200) {
        navigate("/dashboard");
      }
    } catch (error) {
      console.error("Error:", error);

      // If login failed, display error message
      setErrorMessage("Your Email and Password are incorrect.");
    }
  };

  return (
    <div className="login-page">
      <form className="form" id="login" onSubmit={handleLogin}>
        <h1 className="form-title">Login</h1>

        {/* Email input */}
        <label>
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </label>
        <br />

        {/* Password input */}
        <label>
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </label>
        <br />

        {/* Submit button */}
        <button type="submit">Login</button>

        {/* Display error message */}
        {errorMessage && (
          <div className="error-message">
            <p>{errorMessage}</p>
          </div>
        )}
      </form>
    </div>
  );
}

export default Login;
