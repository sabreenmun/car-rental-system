// controllers/authController.js
const User = require('../models/User');
const { hashPassword, verifyPassword } = require('../utils/encryption');
const jwt = require('jsonwebtoken');

// Register a new user
exports.register = (req, res) => {
    const { email, password, security_question_1, security_answer_1, security_question_2, security_answer_2, security_question_3, security_answer_3, user_type } = req.body;

   console.log('Registering new user with data:', req.body);
   if (!user_type) {
    return res.status(400).json({ error: 'user_type is required' });
  }
  // Hash the password
  const password_hash = hashPassword(password);

  const newUser = {
    email,
    password_hash,
    security_question_1,
    security_answer_1,
    security_question_2,
    security_answer_2,
    security_question_3,
    security_answer_3,
    user_type
  };

  console.log('New user data:', newUser); 


  User.create(newUser, (err, results) => {
    if (err) {
      return res.status(500).json({ error: 'Error registering user', details: err });
    }
    res.status(201).json({ message: 'User registered successfully' });
  });
};

// Log in a user
exports.login = (req, res) => {
  const { email, password } = req.body;

  User.findByEmail(email, (err, results) => {
    if (err || results.length === 0) {
      return res.status(401).json({ error: 'Invalid email or password' });
    }

    const user = results[0];
    if (verifyPassword(password, user.password_hash)) {
      // Generate a JWT token
      const token = jwt.sign({ userId: user.user_id, email: user.email }, 'your-secret-key', { expiresIn: '1h' });
      res.status(200).json({ message: 'Login successful', token });
    } else {
      res.status(401).json({ error: 'Invalid email or password' });
    }
  });
};

// Forgot password (initiate recovery)
exports.forgotPassword = (req, res) => {
  const { email, security_answers } = req.body;

  User.findByEmail(email, (err, results) => {
    if (err || results.length === 0) {
      return res.status(404).json({ error: 'User not found' });
    }

    const user = results[0];
    const isAnswersCorrect =
      security_answers.question1 === user.security_answer_1 &&
      security_answers.question2 === user.security_answer_2 &&
      security_answers.question3 === user.security_answer_3;

    if (isAnswersCorrect) {
      res.status(200).json({ message: 'Security questions answered correctly', email });
    } else {
      res.status(400).json({ error: 'Incorrect answers to security questions' });
    }
  });
};

// Reset password
exports.resetPassword = (req, res) => {
  const { email, newPassword } = req.body;

  // Hash the new password
  const newPasswordHash = hashPassword(newPassword);

  User.updatePassword(email, newPasswordHash, (err, results) => {
    if (err) {
      return res.status(500).json({ error: 'Error resetting password', details: err });
    }
    res.status(200).json({ message: 'Password reset successfully' });
  });
};