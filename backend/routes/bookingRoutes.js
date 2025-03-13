const express = require("express");
/*const {
    createBooking,
    getAllBookings,
    getBookingById,
    updateBookingStatus,
    deleteBooking
} = require('../controllers/bookingController');
*/

const bookingController = require("../controllers/bookingController");

const router = express.Router();

// Create a new booking
router.post("/", bookingController.createBooking);

// Get all bookings
router.get("/", bookingController.getAllBookings);

// Get a single booking by ID
router.get("/:id", bookingController.getBookingById);

// Update booking status
router.put("/:id", bookingController.updateBookingStatus);

// Delete a booking
router.delete("/:id", bookingController.deleteBooking);

module.exports = router;
