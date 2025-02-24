// app.js
const express = require('express');
const authRoutes = require('./routes/authRoutes');

const app = express();

// Middleware to parse JSON bodies
app.use(express.json());

// Use auth routes
app.use('/api/auth', authRoutes);

module.exports = app;