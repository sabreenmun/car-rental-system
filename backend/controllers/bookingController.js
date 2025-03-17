const Booking = require("../models/Booking");
const moment = require("moment");  // Import Moment.js for date validation

// Helper function to check if a date is in the future
const isDateInFuture = (date) => {
  return moment(date).isAfter(moment(), 'day');
};

// Create a new booking
exports.createBooking = (req, res) => {
  const { car_id, renter_id, start_date, end_date, total_cost } = req.body;

  // Validation checks
  if (!car_id || !renter_id || !start_date || !end_date || !total_cost) {
    return res.status(400).json({ message: "All fields are required" });
  }

  // Validate start and end dates
  if (!isDateInFuture(start_date) || !isDateInFuture(end_date)) {
    return res.status(400).json({ message: "Start and end dates must be in the future" });
  }

  if (moment(start_date).isAfter(moment(end_date))) {
    return res.status(400).json({ message: "End date cannot be earlier than start date" });
  }

  // Check if the car is available for the given dates
  Booking.checkAvailability(car_id, start_date, end_date, (err, result) => {
    if (err) return res.status(500).json({ message: err.message });

    if (result.length > 0) {
      return res.status(400).json({ message: "Car is already booked during these dates" });
    }

    // Create the booking if available
    Booking.create(
      { car_id, renter_id, start_date, end_date, total_cost },
      (err, result) => {
        if (err) return res.status(500).json({ message: err.message });
        res.status(201).json({
          message: "Booking created successfully",
          booking_id: result.insertId,
        });
      }
    );
  });
};

// Get all bookings
exports.getAllBookings = (req, res) => {
  Booking.getAll((err, results) => {
    if (err) return res.status(500).json({ message: err.message });
    res.json(results);
  });
};

// Get a booking by ID
exports.getBookingById = (req, res) => {
  const { id } = req.params;

  Booking.findById(id, (err, result) => {
    if (err) return res.status(500).json({ message: err.message });
    if (!result.length)
      return res.status(404).json({ message: "Booking not found" });
    res.json(result[0]);
  });
};

// Update booking status
exports.updateBookingStatus = (req, res) => {
  const { id } = req.params;
  const { booking_status } = req.body;

  if (!booking_status) {
    return res.status(400).json({ message: "Booking status is required" });
  }

  Booking.updateStatus(id, booking_status, (err) => {
    if (err) return res.status(500).json({ message: err.message });
    res.json({ message: "Booking status updated successfully" });
  });
};

// Delete a booking
exports.deleteBooking = (req, res) => {
  const { id } = req.params;

  Booking.delete(id, (err) => {
    if (err) return res.status(500).json({ message: err.message });
    res.json({ message: "Booking deleted successfully" });
  });
};
