const express = require('express');
const bcrypt = require('bcryptjs');
const db = require('../db');
const router = express.Router();

// Registration route
router.post('/', async (req, res) => {
  const { email, password, sq_1, sa_1, sq_2, sa_2, sq_3, sa_3 } = req.body;

  // Basic validation to check that all fields are present
  if (!email || !password || !sq_1 || !sa_1 || !sq_2 || !sa_2 || !sq_3 || !sa_3) {
    return res.status(400).json({ success: false, message: 'All fields are required' });
  }

  try {
    // Hash the password before storing it
    const hashedPassword = await bcrypt.hash(password, 10);

    // Prepare the SQL query to insert the data into the users table
    const query = `
      INSERT INTO users (email, password, security_q1, security_a1, security_q2, security_a2, security_q3, security_a3)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    `;

    // Execute the query with data
    db.query(query, [email, hashedPassword, sq_1, sa_1, sq_2, sa_2, sq_3, sa_3], (err, result) => {
      if (err) {
        console.error('Error inserting data:', err);
        return res.status(500).json({ success: false, message: 'Error registering user' });
      }
      res.status(200).json({ success: true, message: 'User registered successfully' });
    });
  } catch (err) {
    console.error('Error hashing password:', err);
    res.status(500).json({ success: false, message: 'Error registering user' });
  }
});

// Export the router to be used in server.js
module.exports = router;
