// carRoutes.js
const express = require("express");
const carController = require("../controllers/carController");
const router = express.Router();

// Route to create a new car listing
router.post("/cars", carController.createCar);

// Route to search cars based on query parameters
router.get("/cars/search", carController.searchCars);

// Route to fetch car by ID
router.get("/cars/:car_id", carController.getCarById);

// Route to get all cars
router.get("/cars", carController.getAllCars);

// Route to update car details
router.put("/cars/:car_id", carController.updateCar);

// Route to delete a car listing
router.delete("/cars/:car_id", carController.deleteCar);

module.exports = router;
