// carRoutes.js
const express = require('express');
const carController = require('../controllers/carController');
const router = express.Router();

// Log to check if the router is being hit
router.use((req, res, next) => {
  console.log(`Request method: ${req.method}, Route: ${req.originalUrl}`);
  next();
});

// Create a new car listing
router.post('/', carController.createCar);

// Get a car by ID
router.get('/:car_id', carController.getCarById);
//get all cars
router.get('/cars', carController.getAllCars);
// Update a car's details
router.put('/:car_id', carController.updateCar);

// Delete a car listing
router.delete('/:car_id', carController.deleteCar);

// GET /cars/search for searching cars based on filters
router.get('/search', carController.searchCars);

module.exports = router;
