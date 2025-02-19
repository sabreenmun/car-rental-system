require("dotenv").config();
const express = require("express");
const cors = require("cors");
const db = require("./db"); // import MySQL connection from db.js

// middleware
app.use(cors());
app.use(express.json()); // parse the JSON requests

// test route
app.get("/", (req, res) => {
  res.send("Welcome to Drive Share API!");
});
app.get



// start the server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
