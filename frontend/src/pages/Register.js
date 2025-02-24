import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import "../styles/Register.css";

function Register() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [securityQuestion1, setSecurityQuestion1] = useState('');
  const [answer1, setAnswer1] = useState('');
  const [securityQuestion2, setSecurityQuestion2] = useState('');
  const [answer2, setAnswer2] = useState('');
  const [securityQuestion3, setSecurityQuestion3] = useState('');
  const [answer3, setAnswer3] = useState('');
  const [user_type, setUserType] = useState('');

  // Define the available security questions
  const securityQuestions = [
    "What is your mother's maiden name?",
    "What was the name of your first pet?",
    "What was the name of your elementary school?",
  ];

  // Handle form submission
  const handleSubmit = (e) => {
    e.preventDefault();

    // Basic validation
    if (!email || !password || !securityQuestion1 || !answer1 || !securityQuestion2 || !answer2 || !securityQuestion3 || !answer3) {
      alert('Please fill out all fields.');
      return;
    }

    const formData = {
      email,
      password,
      securityQuestion1,
      answer1,
      securityQuestion2,
      answer2,
      securityQuestion3,
      answer3,
      user_type,
    };

    // For now, log the form data to the console
    console.log('Form submitted:', formData);

    // Optionally, store it in localStorage or handle the form data as needed
    localStorage.setItem('userData', JSON.stringify(formData));

    // Reset form fields after submission
    setEmail('');
    setPassword('');
    setSecurityQuestion1('');
    setAnswer1('');
    setSecurityQuestion2('');
    setAnswer2('');
    setSecurityQuestion3('');
    setAnswer3('');
    setUserType('');
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
            value={securityQuestion1}
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
            value={answer1}
            onChange={(e) => setAnswer1(e.target.value)}
            required
          />
        </div>

        <div>
          <label>Security Question 2:</label>
          <select
            value={securityQuestion2}
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
            value={answer2}
            onChange={(e) => setAnswer2(e.target.value)}
            required
          />
        </div>

        <div>
          <label>Security Question 3:</label>
          <select
            value={securityQuestion3}
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
            value={answer3}
            onChange={(e) => setAnswer3(e.target.value)}
            required
          />
        </div>

        <button type="submit">Register</button>
      </form>

      <p>
        Already have an account? <Link to="/login">Login</Link>
      </p>
    </div>
  );
}

export default Register;
