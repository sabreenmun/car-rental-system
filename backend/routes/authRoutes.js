// routes/authRoutes.js
const express = require('express');
const authController = require('../controllers/authController');

const router = express.Router();

// register a new user
router.post('/register', authController.register);

// login in a user
router.post('/login', authController.login);

// forgot password (initiate recovery)
router.post('/forgot-password', authController.forgotPassword);

// reset password
router.post('/reset-password', authController.resetPassword);

module.exports = router;