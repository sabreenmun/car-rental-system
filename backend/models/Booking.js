// models/Booking.js
const db = require("../config/db");

class Booking {
  // Create a new booking
  static create(booking, callback) {
    const { car_id, renter_id, start_date, end_date, total_cost } = booking;
    const query = `
      INSERT INTO Bookings (car_id, renter_id, start_date, end_date, total_cost)
      VALUES (?, ?, ?, ?, ?)
    `;
    db.query(
      query,
      [car_id, renter_id, start_date, end_date, total_cost],
      callback
    );
  }

  // Get all bookings
  static getAll(callback) {
    const query = `
      SELECT B.*, C.car_model AS car_model, U.email AS renter_email
      FROM Bookings B
      JOIN Cars C ON B.car_id = C.car_id
      JOIN Users U ON B.renter_id = U.user_id
    `;
    db.query(query, callback);
  }

  static findById(booking_id, callback) {
    const query = `
      SELECT B.*, C.car_model AS car_model, U.email AS renter_email
      FROM Bookings B
      JOIN Cars C ON B.car_id = C.car_id
      JOIN Users U ON B.renter_id = U.user_id
      WHERE B.booking_id = ?
    `;
    db.query(query, [booking_id], (err, results) => {
      if (err) {
        return callback(err, null);
      }
      if (results.length === 0) {
        return callback(null, null); // No booking found
      }
      callback(null, results[0]); // ✅ Return first object instead of array
    });
  }
  
  

  // Update booking status
  static updateStatus = (id, booking_status, result) => {
    const query = `UPDATE Bookings SET booking_status = ? WHERE booking_id = ?`;

    db.query(query, [booking_status, id], (err, res) => {
      if (err) {
        result(err, null);
      } else {
        result(null, res);
      }
    });
  };

  // Delete a booking
  static delete(booking_id, callback) {
    const query = "DELETE FROM Bookings WHERE booking_id = ?";
    db.query(query, [booking_id], callback);
  }
}

module.exports = Booking;
