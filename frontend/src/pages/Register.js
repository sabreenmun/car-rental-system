import React, { useState } from 'react';
import { NavLink, useNavigate } from "react-router-dom";
import axios from 'axios';

import "../styles/Register.css";

function Register() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [sq_1, setSq1] = useState('What was the name of your first pet?');
    const [sa_1, setSa1] = useState('');
    const [sq_2, setSq2] = useState('What is your mother\'s maiden name?');
    const [sa_2, setSa2] = useState('');
    const [sq_3, setSq3] = useState('What is the name of the city you were born in?');
    const [sa_3, setSa3] = useState('');
    const [message, setMessage] = useState('');
    const [errors, setErrors] = useState([]);
    const navigate = useNavigate();

    const handleRegister = async (e) => {
        e.preventDefault();

        const userData = {
          email,
          password,
          sq_1,
          sa_1,
          sq_2,
          sa_2,
          sq_3,
          sa_3
        };

        try {
            const response = await axios.post('http://localhost:5000/register', userData);
            setMessage(response.data.message);
            navigate('/login');
        } catch (error) {
            setMessage('Error registering user');
        }
    };

    return (
        <div className="register-page">
            <form className="form" id="register" onSubmit={handleRegister}>
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

                {/* Security Question 1 */}
                <label>What was the name of your first pet?</label>
                <input
                    type="text"
                    name="answer1"
                    value={sa_1}
                    onChange={(e) => setSa1(e.target.value)}
                    required
                />
                <br />

                {/* Security Question 2 */}
                <label>What is your mother's maiden name?</label>
                <input
                    type="text"
                    name="answer2"
                    value={sa_2}
                    onChange={(e) => setSa2(e.target.value)}
                    required
                />
                <br />

                {/* Security Question 3 */}
                <label>What is the name of the city you were born in?</label>
                <input
                    type="text"
                    name="answer3"
                    value={sa_3}
                    onChange={(e) => setSa3(e.target.value)}
                    required
                />
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
