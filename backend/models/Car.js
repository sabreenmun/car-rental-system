const db = require("../config/db");

class Car {
  // Create a new car listing
  static create(car, callback) {
    const {
      owner_id,
      car_model,
      car_year,
      mileage,
      pickup_location,
      rental_price_per_day,
      availability_calendar,
    } = car;

    const query = `
      INSERT INTO Cars (owner_id, car_model, car_year, mileage, pickup_location, rental_price_per_day, availability_calendar, created_at, updated_at)
      VALUES (?, ?, ?, ?, ?, ?, ?, NOW(), NOW())
    `;
    
    db.query(
      query,
      [
        owner_id,
        car_model,
        car_year,
        mileage,
        pickup_location,
        rental_price_per_day,
        JSON.stringify(availability_calendar) // Ensure availability is stored as a JSON string
      ],
      callback
    );
  }

  // Find a car by its ID
  static findById(car_id, callback) {
    const query = "SELECT * FROM Cars WHERE car_id = ?";
    db.query(query, [car_id], callback);
  }

  // Find cars by the owner ID
  static findByOwner(owner_id, callback) {
    const query = "SELECT * FROM Cars WHERE owner_id = ?";
    db.query(query, [owner_id], callback);
  }

  // Update a car's details (like availability, price, etc.)
  static update(car_id, updatedCar, callback) {
    const {
      car_model,
      car_year,
      mileage,
      pickup_location,
      rental_price_per_day,
      availability_calendar,
    } = updatedCar;

    const query = `
      UPDATE Cars
      SET car_model = ?, car_year = ?, mileage = ?, pickup_location = ?, rental_price_per_day = ?, availability_calendar = ?, updated_at = NOW()
      WHERE car_id = ?
    `;

    db.query(
      query,
      [
        car_model,
        car_year,
        mileage,
        pickup_location,
        rental_price_per_day,
        JSON.stringify(availability_calendar),
        car_id
      ],
      callback
    );
  }

  // Delete a car listing
  static delete(car_id, callback) {
    const query = "DELETE FROM Cars WHERE car_id = ?";
    db.query(query, [car_id], callback);
  }

  // Search cars based on different criteria (location, car model, etc.)
  static search(filters, callback) {
    const { location, car_model, date } = filters;
    let query = "SELECT * FROM Cars WHERE 1=1";

    const queryParams = [];

    if (location) {
      query += " AND pickup_location LIKE ?";
      queryParams.push(`%${location}%`);
    }
    if (car_model) {
      query += " AND car_model LIKE ?";
      queryParams.push(`%${car_model}%`);
    }
    if (date) {
      query += " AND JSON_CONTAINS(availability_calendar, ?)";
      queryParams.push(JSON.stringify([date])); // Assuming `availability_calendar` is a JSON array
    }

    db.query(query, queryParams, callback);
  }
}

module.exports = Car;
