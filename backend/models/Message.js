const db = require("../config/db");

const Message = {};

// Create a new message
Message.create = (newMessage, result) => {
  // SQL query to insert the new message into the database
  const query = `
        INSERT INTO Messages (sender_id, receiver_id, message_text)
        VALUES (?, ?, ?)
    `;

  // Execute the query
  db.query(
    query,
    [newMessage.sender_id, newMessage.receiver_id, newMessage.message_text],
    (err, res) => {
      if (err) {
        console.error("Error inserting message:", err);
        result(err, null); // Return the error if the query fails
        return;
      }

      console.log("Message sent successfully:", res);
      result(null, { message_id: res.insertId, ...newMessage }); // Return the new message with its generated ID
    }
  );
};

module.exports = Message;
