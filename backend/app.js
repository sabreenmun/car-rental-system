// app.js
const express = require('express');
const cors = require('cors');
const authRoutes = require('./routes/authRoutes');

const app = express();

app.use(cors());  

// Middleware to parse JSON bodies
app.use(express.json());

// Use auth routes
app.use('/api/auth', authRoutes);

module.exports = app;