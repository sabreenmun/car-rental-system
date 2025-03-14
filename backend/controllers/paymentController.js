const Payment = require("../models/Payment");
const Booking = require("../models/Booking");

// Create a new payment
exports.createPayment = (req, res) => {
  const { booking_id, payment_amount } = req.body;

  // Validate required fields
  if (!booking_id || !payment_amount) {
    return res.status(400).json({
      message: "Booking ID and payment amount are required!",
    });
  }

  // Check if the booking exists
  Booking.findById(booking_id, (err, booking) => {
    if (err) {
      console.error("Database error:", err);
      return res.status(500).json({ message: "Internal server error" });
    }
    if (!booking) {
      return res.status(404).json({ message: "Booking not found!" });
    }

    // Debugging: Log booking details
    console.log("Booking object:", booking);

    if (!booking.booking_status) {
      return res.status(400).json({
        message: "Booking status is missing. Please check the database.",
      });
    }

    // Ensure the booking status is "confirmed"
    if (booking.booking_status !== "confirmed") {
      return res.status(400).json({
        message: "Booking must be confirmed before processing payment!",
      });
    }

    // Create payment with "pending" status
    const paymentData = {
      booking_id,
      amount: payment_amount,
      payment_status: "pending",
      payment_date: new Date(),
    };

    // Save payment in the database
    Payment.create(paymentData, (err, payment) => {
      if (err) {
        console.error("Payment creation error:", err);
        return res.status(500).json({ message: "Error processing payment" });
      }

      return res.status(201).json({
        message:
          "Payment is pending. Please confirm the payment to complete the booking.",
        payment,
      });
    });
  });
};

// Get payment by booking ID
exports.getPaymentByBookingId = (req, res) => {
  const { booking_id } = req.params;

  Payment.findByBookingId(booking_id, (err, payment) => {
    if (err) {
      console.error("Database error:", err);
      return res.status(500).json({ message: "Internal server error" });
    }
    if (!payment) {
      return res
        .status(404)
        .json({ message: "No payment found for this booking!" });
    }
    res.json(payment);
  });
};

// Get all payments
exports.getAllPayments = (req, res) => {
  Payment.getAll((err, payments) => {
    if (err) {
      console.error("Database error:", err);
      return res.status(500).json({ message: "Internal server error" });
    }
    res.json(payments);
  });
};
