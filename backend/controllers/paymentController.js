const Payment = require("../models/Payment");
const Booking = require("../models/Booking");

// Create a new payment
exports.createPayment = (req, res) => {
  const { booking_id, payment_amount } = req.body;

  // Ensure required fields are provided
  if (!booking_id || !payment_amount) {
    return res.status(400).json({
      message: "Booking ID and payment amount are required!",
    });
  }

  // Check if booking exists and its status is valid for payment
  Booking.findById(booking_id, (err, booking) => {
    if (err) return res.status(500).json({ message: err.message });
    if (!booking) {
      return res.status(404).json({ message: "Booking not found!" });
    }
    // Log the entire booking object to see what is returned
    console.log("Booking object: ", booking);

    console.log("Booking status: ", booking.booking_status);
    // Ensure the booking status is confirmed
    if (booking.booking_status !== "confirmed") {
      return res.status(400).json({
        message: "Booking must be confirmed before processing payment!",
      });
    }

    // Create payment object with status "pending"
    const paymentData = {
      booking_id,
      amount: payment_amount,
      payment_status: "pending", // Set payment status to "pending" by default
      payment_date: new Date(),
    };

    // Call the Payment model to create a payment
    Payment.create(paymentData, (err, payment) => {
      if (err) return res.status(500).json({ message: err.message });

      // If payment status is updated to "completed", update booking status
      // This can be handled later based on payment confirmation logic
      return res.status(201).json({
        message:
          "Payment is in pending status. Please confirm payment to complete booking.",
        payment: payment,
      });
    });
  });
};

// Get payment by booking ID
exports.getPaymentByBookingId = (req, res) => {
  const { booking_id } = req.params;

  Payment.findByBookingId(booking_id, (err, payment) => {
    if (err) return res.status(500).json({ message: err.message });
    if (!payment) {
      return res
        .status(404)
        .json({ message: "Payment not found for this booking!" });
    }
    res.json(payment);
  });
};

// Get all payments
exports.getAllPayments = (req, res) => {
  Payment.getAll((err, payments) => {
    if (err) return res.status(500).json({ message: err.message });
    res.json(payments);
  });
};
