import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios"; // Import axios for making API requests
import "../styles/Register.css";

function Register() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [security_question_1, setSecurityQuestion1] = useState("");
  const [security_answer_1, setAnswer1] = useState("");
  const [security_question_2, setSecurityQuestion2] = useState("");
  const [security_answer_2, setAnswer2] = useState("");
  const [security_question_3, setSecurityQuestion3] = useState("");
  const [security_answer_3, setAnswer3] = useState("");
  const [user_type, setUserType] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const navigate = useNavigate(); // Use navigate for redirection

  const securityQuestions = [
    "What is your mother's maiden name?",
    "What was the name of your first pet?",
    "What was the name of your elementary school?",
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
  
    // Basic validation
    if (
      !email ||
      !password ||
      !security_question_1 ||
      !security_answer_1 ||
      !security_question_2 ||
      !security_answer_2 ||
      !security_question_3 ||
      !security_answer_3
    ) {
      alert("Please fill out all fields.");
      return;
    }
  
    const formData = {
      email,
      password,
      security_question_1,
      security_answer_1,
      security_question_2,
      security_answer_2,
      security_question_3,
      security_answer_3,
      user_type,
    };
  
    try {
      // Make a POST request to the backend to register the user
      console.log('Form Data:', formData);
      const response = await axios.post(
        "http://localhost:5000/api/auth/register",
        formData
      );
  
      // Check if the registration was successful
      if (response.status === 201) {
        alert("User registered successfully");
        // Redirect to login page after successful registration
        navigate("/login");
      } else {
        setErrorMessage("Registration failed. Please try again.");
      }
    } catch (error) {
      console.error("Error registering user:", error);
      setErrorMessage("Error registering user. Please try again later.");
    }
  
    // Reset form fields after submission
    setEmail("");
    setPassword("");
    setSecurityQuestion1("");
    setAnswer1("");
    setSecurityQuestion2("");
    setAnswer2("");
    setSecurityQuestion3("");
    setAnswer3("");
    setUserType("");
  };
  

  return (
    <div className="register-page">
      <h2>Register</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Email:</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        <div>
          <label>User Type:</label>
          <select
            value={user_type}
            onChange={(e) => setUserType(e.target.value)}
            required
          >
            <option value="">Select User Type</option>
            <option value="Owner">Car Owner</option>
            <option value="Renter">Car Renter</option>
          </select>
        </div>

        <div>
          <label>Security Question 1:</label>
          <select
            value={security_question_1}
            onChange={(e) => setSecurityQuestion1(e.target.value)}
            required
          >
            <option value="">Select a question</option>
            {securityQuestions.map((question, index) => (
              <option key={index} value={question}>
                {question}
              </option>
            ))}
          </select>
          <input
            type="text"
            placeholder="Answer"
            value={security_answer_1}
            onChange={(e) => setAnswer1(e.target.value)}
            required
          />
        </div>

        <div>
          <label>Security Question 2:</label>
          <select
            value={security_question_2}
            onChange={(e) => setSecurityQuestion2(e.target.value)}
            required
          >
            <option value="">Select a question</option>
            {securityQuestions.map((question, index) => (
              <option key={index} value={question}>
                {question}
              </option>
            ))}
          </select>
          <input
            type="text"
            placeholder="Answer"
            value={security_answer_2}
            onChange={(e) => setAnswer2(e.target.value)}
            required
          />
        </div>

        <div>
          <label>Security Question 3:</label>
          <select
            value={security_question_3}
            onChange={(e) => setSecurityQuestion3(e.target.value)}
            required
          >
            <option value="">Select a question</option>
            {securityQuestions.map((question, index) => (
              <option key={index} value={question}>
                {question}
              </option>
            ))}
          </select>
          <input
            type="text"
            placeholder="Answer"
            value={security_answer_3}
            onChange={(e) => setAnswer3(e.target.value)}
            required
          />
        </div>

        <button type="submit">Register</button>
      </form>

      {errorMessage && <div className="error-message">{errorMessage}</div>}

      <p>
        Already have an account? <Link to="/login">Login</Link>
      </p>
    </div>
  );
}

export default Register;
