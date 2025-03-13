const express = require("express");
const paymentController = require("../controllers/paymentController");
const router = express.Router();

router.post("/", paymentController.createPayment);
router.get("/booking/:booking_id", paymentController.getPaymentByBookingId);
router.get("/", paymentController.getAllPayments);

module.exports = router;
