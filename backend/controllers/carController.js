// carController.js
const Car = require('../models/Car');  // Import Car model

// Create a new car listing
exports.createCar = async (req, res) => {
  const { owner_id, car_model, car_year, mileage, pickup_location, rental_price_per_day, availability_calendar } = req.body;

  if (!car_model || !rental_price_per_day) {
    return res.status(400).json({ message: 'Missing required fields' });
  }

  const newCar = {
    owner_id,
    car_model,
    car_year,
    mileage,
    pickup_location,
    rental_price_per_day,
    availability_calendar,
  };

  try {
    // Insert car into the database
    Car.create(newCar, (err, result) => {
      if (err) {
        console.error('Error inserting car into the database:', err);
        return res.status(500).json({ message: 'Error creating car listing', error: err });
      }
      res.status(201).json({ message: 'Car listing created successfully', car: result });
    });
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ message: 'Error creating car listing', error });
  }
};


// Get a car by ID
exports.getCarById = (req, res) => {
  const carId = req.params.car_id;
  console.log('Fetching car with ID:', carId); // Log the car ID to confirm it's correct

  Car.findById(carId, (err, results) => {
    if (err) {
      return res.status(500).json({ message: 'Error fetching car details', error: err });
    }

    if (!results.length) {
      console.log("CAR NOT FOUND");
      return res.status(404).json({ message: 'Car not found' });
    }

    res.status(200).json({ car: results[0] });
  });
};

exports.getAllCars = async (req, res) => {
  try {
    const query = "SELECT c.car_id, c.car_model, c.rental_price_per_day, c.owner_id, u.email AS owner_email FROM Cars c JOIN Users u ON c.owner_id = u.user_id";
    db.query(query, (err, results) => {
      if (err) {
        console.error("Error fetching cars from database:", err);
        return res.status(500).json({ message: 'Error fetching cars from database', error: err });
      }
      console.log("Fetched cars:", results);  // Check the result in your backend logs
      res.status(200).json(results); // Send the results as a JSON response
    });
  } catch (error) {
    console.error("Error fetching cars:", error);
    res.status(500).json({ message: 'Error fetching cars', error });
  }
};



// Update a car's details
exports.updateCar = (req, res) => {
  const carId = req.params.car_id;
  const updatedCar = req.body;

  Car.update(carId, updatedCar, (err, result) => {
    if (err) {
      return res.status(500).json({ message: 'Error updating car details', error: err });
    }

    res.status(200).json({ message: 'Car details updated successfully', car: updatedCar });
  });
};

// Delete a car listing
exports.deleteCar = (req, res) => {
  const carId = req.params.car_id;

  Car.delete(carId, (err, result) => {
    if (err) {
      return res.status(500).json({ message: 'Error deleting car listing', error: err });
    }

    res.status(200).json({ message: 'Car listing deleted successfully' });
  });
};

// Search cars based on filters (location, model, availability)
exports.searchCars = (req, res) => {
  const { model, location, date } = req.query;  // Using query params for search filters

  const filters = {};
  if (location) filters.pickup_location = location;
  if (model) filters.car_model = model;
  if (date) filters.date = date;

  Car.search(filters, (err, results) => {
    if (err) {
      return res.status(500).json({ message: 'Error searching for cars', error: err });
    }
    res.status(200).json({ cars: results });
  });
};
