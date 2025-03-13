// app.js
const express = require("express");
const cors = require("cors");
const authRoutes = require("./routes/authRoutes");
const carRoutes = require("./routes/carRoutes");
const bookingRoutes = require("./routes/bookingRoutes");
const paymentRoutes = require("./routes/paymentRoutes");
const app = express();

app.use(cors());

// Middleware to parse JSON bodies
app.use(express.json());
// Test route to check if the server is running
app.get("/test", (req, res) => {
  console.log("Test route hit!");
  res.send("Server is working!");
});

// Use auth routes
app.use("/api/auth", authRoutes);
app.use("/api", carRoutes);
app.use("/api/bookings", bookingRoutes);
app.use("/api/payments", paymentRoutes);
module.exports = app;
