// carController.js
const Car = require("../models/Car"); // Import Car model
const db = require("../config/db");

exports.createCar = async (req, res) => {
  const {
    owner_id,
    car_model,
    car_year,
    mileage,
    pickup_location,
    rental_price_per_day,
    availability_start_date,
    availability_end_date,
  } = req.body;

  // Ensure all required fields are provided
  if (
    !car_model ||
    !car_year ||
    !mileage ||
    !pickup_location ||
    !rental_price_per_day ||
    !availability_start_date ||
    !availability_end_date
  ) {
    return res.status(400).json({
      message:
        "All fields are required: car_model, car_year, mileage, pickup_location, rental_price_per_day, availability_start_date, availability_end_date",
    });
  }

  const newCar = {
    owner_id,
    car_model,
    car_year,
    mileage,
    pickup_location,
    rental_price_per_day,
    availability_start_date,
    availability_end_date,
  };

  try {
    // Insert car into the database
    Car.create(newCar, (err, result) => {
      if (err) {
        console.error("Error inserting car into the database:", err);
        return res.status(500).json({
          message: "Error creating car listing",
          error: err.message || "Database error",
        });
      }

      res
        .status(201)
        .json({ message: "Car listing created successfully", car: result });
    });
  } catch (error) {
    console.error("Error:", error);
    res
      .status(500)
      .json({ message: "Error creating car listing", error: error.message });
  }
};

// Get a car by ID
exports.getCarById = (req, res) => {
  const carId = req.params.car_id;
  console.log("Fetching car with ID:", carId); // Log the car ID to confirm it's correct
  console.log("Inside getCarById function");
  Car.findById(carId, (err, results) => {
    if (err) {
      return res
        .status(500)
        .json({ message: "Error fetching car details", error: err });
    }

    if (!results.length) {
      console.log("CAR NOT FOUND");
      return res.status(404).json({ message: "Car not found" });
    }

    res.status(200).json({ car: results[0] });
  });
};

// Controller Method for Handling API Request (GET /api/cars)
exports.getAllCars = async (req, res) => {
  try {
    const { model, location, minPrice, maxPrice } = req.query; // Get query parameters

    let query =
      "SELECT c.car_id, c.car_model, c.rental_price_per_day, c.owner_id, u.email AS owner_email FROM Cars c JOIN Users u ON c.owner_id = u.user_id WHERE 1=1";

    // Dynamically build the query based on provided filters
    if (model) {
      query += ` AND c.car_model LIKE '%${model}%'`; // Case-insensitive search
    }
    if (location) {
      query += ` AND c.pickup_location LIKE '%${location}%'`; // Case-insensitive search
    }
    if (minPrice) {
      query += ` AND c.rental_price_per_day >= ${minPrice}`; // Minimum price filter
    }
    if (maxPrice) {
      query += ` AND c.rental_price_per_day <= ${maxPrice}`; // Maximum price filter
    }

    // Execute the query
    db.query(query, (err, results) => {
      if (err) {
        console.error("Error fetching cars from database:", err);
        return res
          .status(500)
          .json({ message: "Error fetching cars from database", error: err });
      }

      if (results.length === 0) {
        return res.status(404).json({
          message: "No cars found matching your filters",
        });
      }

      console.log("Fetched cars:", results); // Log the fetched results
      return res.status(200).json({
        cars: results, // Send the fetched cars data as a JSON response
      });
    });
  } catch (error) {
    console.error("Error fetching cars:", error);
    return res.status(500).json({ message: "Error fetching cars", error });
  }
};

// Update a car's details
exports.updateCar = (req, res) => {
  const carId = req.params.car_id;
  const updatedCar = req.body;

  Car.update(carId, updatedCar, (err, result) => {
    if (err) {
      return res
        .status(500)
        .json({ message: "Error updating car details", error: err });
    }

    res
      .status(200)
      .json({ message: "Car details updated successfully", car: updatedCar });
  });
};

// Delete a car listing
exports.deleteCar = (req, res) => {
  const carId = req.params.car_id;

  Car.delete(carId, (err, result) => {
    if (err) {
      return res
        .status(500)
        .json({ message: "Error deleting car listing", error: err });
    }

    res.status(200).json({ message: "Car listing deleted successfully" });
  });
};

exports.searchCars = (req, res) => {
  const { model, location, date, price } = req.query;

  const filters = {};
  if (model) filters.car_model = new RegExp(model, "i");
  if (location) filters.pickup_location = new RegExp(location.trim(), "i"); // Trim spaces
  if (date) {
    const searchDate = new Date(date);
    filters.availability_start_date = { $lte: searchDate };
    filters.availability_end_date = { $gte: searchDate };
  }
  if (price) filters.rental_price_per_day = { $lte: price };

  console.log("Filters being used:", filters); // Debugging filters

  Car.find(filters, (err, cars) => {
    if (err) {
      return res
        .status(500)
        .json({ message: "Error searching for cars", error: err });
    }

    if (!cars || cars.length === 0) {
      return res.status(404).json({ message: "No cars found" });
    }

    res.status(200).json({ cars });
  });
};
