// car.js - Car Model
const db = require("../config/db");

const Payment = {};

// In Payment Model

// Create a new payment
Payment.create = (paymentData, result) => {
  const query = `INSERT INTO payments (booking_id, amount, payment_status) VALUES (?, ?, ?)`; // Removed payment_date

  db.query(
    query,
    [paymentData.booking_id, paymentData.amount, paymentData.payment_status],
    (err, res) => {
      if (err) {
        console.error("Error inserting payment:", err);
        result(err, null);
        return;
      }
      result(null, res);
    }
  );
};

module.exports = Payment;

// Find payment by booking ID
Payment.findByBookingId = (booking_id, result) => {
  const query = `SELECT * FROM payments WHERE booking_id = ?`;
  db.query(query, [booking_id], (err, res) => {
    if (err) {
      console.error("Error retrieving payment:", err);
      result(err, null);
      return;
    }
    if (res.length) {
      result(null, res[0]); // Return the first payment if found
    } else {
      result(null, null); // No payment found
    }
  });
};

// Get all payments
Payment.getAll = (result) => {
  const query = `SELECT * FROM payments`;
  db.query(query, (err, res) => {
    if (err) {
      console.error("Error retrieving payments:", err);
      result(err, null);
      return;
    }
    result(null, res);
  });
};
