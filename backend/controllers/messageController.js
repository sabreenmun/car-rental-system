const db = require("../config/db");
const Message = require("../models/Message");

// Combined Controller to Send a Message and Fetch Messages
exports.handleMessage = (req, res) => {
  const { action } = req.params; // Determine action from the route (either 'send' or 'get')

  // Handle Sending a Message
  if (action === "send") {
    const { sender_id, receiver_id, message_text } = req.body;

    // Validate input fields
    if (!sender_id || !receiver_id || !message_text) {
      return res
        .status(400)
        .json({ error: "Sender, receiver, and message text are required." });
    }

    // Create a new message object
    const newMessage = { sender_id, receiver_id, message_text };

    // Insert new message into the database
    Message.create(newMessage, (err, message) => {
      if (err) {
        return res
          .status(500)
          .json({ error: "Failed to send message", details: err.message });
      }

      // Return a success response with the sent message data
      res.status(201).json({
        message: "Message sent successfully",
        data: message,
      });
    });
  }

  // Handle Fetching Messages
  else if (action === "get") {
    const { sender_id, receiver_id } = req.params;

    // Validate input parameters
    if (!sender_id || !receiver_id) {
      return res
        .status(400)
        .json({ error: "Sender and receiver IDs are required." });
    }

    // Use Message model to fetch conversation
    Message.getConversation(sender_id, receiver_id, (err, messages) => {
      if (err) {
        return res.status(500).json({
          error: "Failed to retrieve messages",
          details: err.message,
        });
      }

      // Return the list of messages between the sender and receiver
      res.status(200).json({
        message: "Messages retrieved successfully",
        data: messages,
      });
    });
  }

  // Handle invalid action
  else {
    return res
      .status(400)
      .json({ error: 'Invalid action. Please use either "send" or "get".' });
  }
};
