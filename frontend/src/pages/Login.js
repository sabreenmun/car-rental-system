import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';  // Import useNavigate from 'react-router-dom'

import "../styles/Login.css";

function Login() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const navigate = useNavigate(); // Declare navigate here, use it to navigate

    const handleLogin = async (e) => {
        e.preventDefault();

        // Validation
        if (!email || !password) {
            setError("Please fill in both fields");
            return;
        }

        try {
            const response = await fetch("http://localhost:5000/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password }),
            });

            const data = await response.json();

            if (response.status === 200) {
                // Store JWT in localStorage
                localStorage.setItem("authToken", data.token);
                // Redirect to dashboard
                navigate('/dashboard'); // Use navigate to redirect to dashboard
            } else {
                setError(data.message || "Login failed.");
            }
        } catch (error) {
            setError("An error occurred while logging in.");
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
                        name="email"
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
                        name="password"
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
                {error && (
                    <div id="error-message" className="error-message">
                        {error}
                    </div>
                )}
            </form>
        </div>
    );
}

export default Login;
