const express = require("express");
const router = express.Router();
const messageController = require("../controllers/messageController"); // Ensure this import is correct

// Define POST route for sending a message
router.post("/message/:action", messageController.handleMessage); // Handles both send and get based on action

module.exports = router;
