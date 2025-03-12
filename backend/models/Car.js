// car.js - Car Model
const db = require("../config/db");

const Car = {};

// Create a new car
Car.create = (newCar, result) => {
  const query = `
    INSERT INTO Cars (owner_id, car_model, car_year, mileage, pickup_location, rental_price_per_day, availability_calendar)
    VALUES (?, ?, ?, ?, ?, ?, ?)
  `;

  const values = [
    newCar.owner_id,
    newCar.car_model,
    newCar.car_year,
    newCar.mileage,
    newCar.pickup_location,
    newCar.rental_price_per_day,
    newCar.availability_calendar,
  ];

  db.query(query, values, (err, res) => {
    if (err) {
      console.error("Error inserting new car:", err);
      result(err, null);
      return;
    }
    result(null, { id: res.insertId, ...newCar });
  });
};

// Find a car by ID
Car.findById = (carId, result) => {
  const query = "SELECT * FROM Cars WHERE car_id = ?";
  db.query(query, [carId], (err, res) => {
    if (err) {
      console.error("Error fetching car by ID:", err);
      result(err, null);
      return;
    }
    if (res.length === 0) {
      result({ message: "Car not found" }, null);
      return;
    }
    result(null, res);
  });
};

// Car Model Method for Getting All Cars with Owner Info
Car.getAllCars = (result) => {
  const query = `
    SELECT c.car_id, c.car_model, c.rental_price_per_day, c.owner_id, u.email AS owner_email
    FROM Cars c
    JOIN Users u ON c.owner_id = u.user_id
  `;

  db.query(query, (err, res) => {
    if (err) {
      console.error("Error fetching cars:", err);
      result(err, null);
      return;
    }
    result(null, res); // Pass results back if successful
  });
};



// Update car details
Car.update = (carId, updatedCar, result) => {
  const query = `
    UPDATE Cars
    SET car_model = ?, car_year = ?, mileage = ?, pickup_location = ?, rental_price_per_day = ?, availability_calendar = ?
    WHERE car_id = ?
  `;

  const values = [
    updatedCar.car_model,
    updatedCar.car_year,
    updatedCar.mileage,
    updatedCar.pickup_location,
    updatedCar.rental_price_per_day,
    updatedCar.availability_calendar,
    carId,
  ];

  db.query(query, values, (err, res) => {
    if (err) {
      console.error("Error updating car:", err);
      result(err, null);
      return;
    }
    if (res.affectedRows === 0) {
      result({ message: "Car not found" }, null);
      return;
    }
    result(null, { id: carId, ...updatedCar });
  });
};

// Delete a car listing
Car.delete = (carId, result) => {
  const query = "DELETE FROM Cars WHERE car_id = ?";
  db.query(query, [carId], (err, res) => {
    if (err) {
      console.error("Error deleting car:", err);
      result(err, null);
      return;
    }
    if (res.affectedRows === 0) {
      result({ message: "Car not found" }, null);
      return;
    }
    result(null, { message: "Car listing deleted successfully" });
  });
};

// Search cars based on filters (location, model, availability)
Car.search = (filters, result) => {
  let query = "SELECT * FROM Cars WHERE 1=1";
  let values = [];

  if (filters.pickup_location) {
    query += " AND pickup_location LIKE ?"; // To handle case insensitivity
    values.push(`%${filters.pickup_location}%`);
  }

  if (filters.car_model) {
    query += " AND car_model LIKE ?"; // To handle case insensitivity
    values.push(`%${filters.car_model}%`);
  }

  if (filters.date) {
    query += " AND availability_calendar LIKE ?"; // Assuming availability is stored as a range of dates
    values.push(`%${filters.date}%`);
  }

  console.log("Executing query:", query);
  console.log("With values:", values);

  db.query(query, values, (err, res) => {
    if (err) {
      console.error("Error searching for cars:", err);
      result(err, null);
      return;
    }

    // Debugging: Log raw response from database
    console.log("Raw DB response:", res);

    // Clean up the availability_calendar field (remove extra quotes)
    const cleanedCars = res.map((car) => {
      if (car.availability_calendar) {
        // Log availability_calendar before replacing
        console.log("Before replacing quotes:", car.availability_calendar);
        car.availability_calendar = car.availability_calendar.replace(/"/g, "");
        // Log after replacement
        console.log("After replacing quotes:", car.availability_calendar);
      }
      return car;
    });

    result(null, cleanedCars);
  });
};

module.exports = Car;
