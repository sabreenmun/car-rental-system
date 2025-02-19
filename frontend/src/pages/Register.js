import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import "../styles/Register.css";
import { NavLink } from 'react-router-dom';

function Register() {
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [userType, setUserType] = useState('Owner'); // Default to 'Owner', can be 'Renter' or 'Both'

    // State for security answers
    const [answer1, setAnswer1] = useState('');
    const [answer2, setAnswer2] = useState('');
    const [answer3, setAnswer3] = useState('');
    
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleRegister = async (e) => {
        e.preventDefault();

        // Collecting user data along with security answers
        const userData = {
            firstName,
            lastName,
            email,
            password,
            userType,
            securityAnswer1: answer1,
            securityAnswer2: answer2,
            securityAnswer3: answer3
        };

        try {
            const response = await axios.post('http://localhost:5000/register', userData);
            navigate('/login');
        } catch (error) {
            setError('Error registering user. Please try again.');
        }
    };

    return (
        <div className="register-page">
            <form className="form" id="register" onSubmit={handleRegister}>
                <h1 className="form-title">Register</h1>

                {/* First Name input */}
                <label>
                    <input
                        type="text"
                        placeholder="First Name"
                        value={firstName}
                        onChange={(e) => setFirstName(e.target.value)}
                        required
                    />
                </label>
                <br />

                {/* Last Name input */}
                <label>
                    <input
                        type="text"
                        placeholder="Last Name"
                        value={lastName}
                        onChange={(e) => setLastName(e.target.value)}
                        required
                    />
                </label>
                <br />

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

                {/* User Type selection */}
                <label>
                    <select
                        value={userType}
                        onChange={(e) => setUserType(e.target.value)}
                        required
                    >
                        <option value="Owner">Owner</option>
                        <option value="Renter">Renter</option>
                        <option value="Both">Both</option>
                    </select>
                </label>
                <br />

                {/* Security Question 1 */}
                <label>What was the name of your first pet?</label>
                <input
                    type="text"
                    value={answer1}
                    onChange={(e) => setAnswer1(e.target.value)}
                    required
                />
                <br />

                {/* Security Question 2 */}
                <label>What is your mother's maiden name?</label>
                <input
                    type="text"
                    value={answer2}
                    onChange={(e) => setAnswer2(e.target.value)}
                    required
                />
                <br />

                {/* Security Question 3 */}
                <label>What is the name of the city you were born in?</label>
                <input
                    type="text"
                    value={answer3}
                    onChange={(e) => setAnswer3(e.target.value)}
                    required
                />
                <br />

                {/* Submit button */}
                <button type="submit">Register</button>

                {/* Display error message */}
                {error && (
                    <div className="error-message">
                        <p>{error}</p>
                    </div>
                )}

                {/* Link to login page */}
               

                <NavLink to="/login">Already have an account? Login</NavLink>
            </form>
        </div>
    );
}

export default Register;