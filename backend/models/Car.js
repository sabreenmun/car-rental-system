// car.js - Car Model
const db = require("../config/db");

const Car = {};

// Create a new car
// Create a new car
Car.create = (newCar, result) => {
  const query = `
    INSERT INTO Cars (owner_id, car_model, car_year, mileage, pickup_location, rental_price_per_day, availability_start_date, availability_end_date)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
  `;

  const values = [
    newCar.owner_id,
    newCar.car_model,
    newCar.car_year,
    newCar.mileage,
    newCar.pickup_location,
    newCar.rental_price_per_day,
    newCar.availability_start_date,
    newCar.availability_end_date,
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
    SET car_model = ?, car_year = ?, mileage = ?, pickup_location = ?, rental_price_per_day = ?, availability_start_date = ?, availability_end_date = ?
    WHERE car_id = ?
  `;

  const values = [
    updatedCar.car_model,
    updatedCar.car_year,
    updatedCar.mileage,
    updatedCar.pickup_location,
    updatedCar.rental_price_per_day,
    updatedCar.availability_start_date,
    updatedCar.availability_end_date,
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
// Search cars based on filters (location, model, availability)
Car.search = (filters, result) => {
  let query = "SELECT * FROM Cars WHERE 1=1";
  let values = [];

  // Filter by pickup location
  if (filters.pickup_location) {
    query += " AND pickup_location LIKE ?"; // To handle case insensitivity
    values.push(`%${filters.pickup_location}%`);
  }

  // Filter by car model
  if (filters.car_model) {
    query += " AND car_model LIKE ?"; // To handle case insensitivity
    values.push(`%${filters.car_model}%`);
  }

  // Filter by availability date range
  if (filters.date) {
    query += " AND ? BETWEEN availability_start_date AND availability_end_date"; // Check if the given date falls within the availability range
    values.push(filters.date); // Assuming `filters.date` is a date in 'YYYY-MM-DD' format
  }

  console.log("Executing query:", query);
  console.log("With values:", values);

  db.query(query, values, (err, res) => {
    if (err) {
      console.error("Error searching for cars:", err);
      result(err, null);
      return;
    }

    // Optionally, you can process the response here before sending it back
    // For example, filtering or formatting the response if needed

    result(null, res);
  });
};

module.exports = Car;
