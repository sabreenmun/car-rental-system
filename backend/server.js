// server.js
const express = require('express');
const dotenv = require('dotenv');
const cors = require('cors');
const registerUser = require( './routes/registerbackend.js');
//const loginUser = require( './routes/loginbackend.js');

// Initialize environment variables
dotenv.config();

const app = express();

// Middleware
app.use(express.json());
app.use(cors());

//api postings
app.post('/register', registerUser);
//app.post('/login', loginUser);

// Start the server
const port = process.env.PORT || 5000;
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
