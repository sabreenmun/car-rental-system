import React, { useState } from 'react';
import { NavLink } from "react-router-dom";
import "./Register.css";

function Register() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [securityQuestions, setSecurityQuestions] = useState({
        question1: "",
        question2: "",
        question3: "",
    });
    const [errors, setErrors] = useState([]);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setSecurityQuestions((prev) => ({
            ...prev,
            [name]: value,
        }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        let messages = [];

        // Validate email
        if (!email.trim()) {
            messages.push("Email is required");
        }

        // Validate password length
        if (password.length <= 7) {
            messages.push("Password must be longer than 7 characters.");
        }

        // If there are errors, display them and stop the form submission
        if (messages.length > 0) {
            setErrors(messages);
        } else {
            setErrors([]); // Reset errors if everything is valid
            // Add form submission logic here (e.g., sending data to an API)
            console.log("Form submitted:", { email, password, securityQuestions });
        }
    };

    return (
        <div className="register-page">
            <form className="form" id="register" onSubmit={handleSubmit}>
                <h1 className="form-title">Register</h1>

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

                {/* Security questions */}
                <label>
                    <input
                        type="text"
                        name="question1"
                        value={securityQuestions.question1}
                        onChange={handleInputChange}
                        placeholder="Security Question 1"
                        required
                    />
                </label>
                <br />
                <label>
                    <input
                        type="text"
                        name="question2"
                        value={securityQuestions.question2}
                        onChange={handleInputChange}
                        placeholder="Security Question 2"
                        required
                    />
                </label>
                <br />
                <label>
                    <input
                        type="text"
                        name="question3"
                        value={securityQuestions.question3}
                        onChange={handleInputChange}
                        placeholder="Security Question 3"
                        required
                    />
                </label>
                <br />
                

                {/* Submit button */}
                <button type="submit">Register</button>
                
                {/* Display error messages */}
                {errors.length > 0 && (
                    <div id="error-message" className="error-message">
                        <ul>
                            {errors.map((message, index) => (
                                <li key={index}>{message}</li>
                            ))}
                        </ul>
                    </div>
                )}

                {/* Link to login page */}
                <NavLink to="/login">Already have an account? Login</NavLink>
            </form>
        </div>
    );
}

export default Register;

