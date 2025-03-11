import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';  // useNavigate for redirecting
import "../styles/Login.css";

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');  // To store any error message
  const navigate = useNavigate();  // To navigate to other pages

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();

    // Call your backend login API (this is an example, update with actual API request)
    try {
      // Replace with actual backend login logic
      const response = await fetch('http://localhost:5000/api/auth/login', {  // Make sure to use the correct URL here
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (response.ok) {
        // On success, store user data or token in localStorage
        // Store the token or any other required data in localStorage
        localStorage.setItem('token', data.token);  // Store JWT token (or user data) in localStorage
        navigate('/dashboard');  // Redirect to homepage/dashboard
      } else {
        setErrorMessage(data.message || 'Login failed. Please try again.');  // Show error message
      }
    } catch (error) {
      setErrorMessage('Something went wrong. Please try again later.');
    }
  };

  return (
    <div className="login-page">
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
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
