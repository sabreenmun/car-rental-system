// BookingPage.js
import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
//import "../styles/BookingPage.css";

function BookingPage() {
  const { carId } = useParams();
  const [carDetails, setCarDetails] = useState(null);

  useEffect(() => {
    const fetchCarDetails = async () => {
      // Fetch car details using the carId from the backend
      const response = await fetch(`http://localhost:5000/api/cars/${carId}`);
      const data = await response.json();
      setCarDetails(data);
    };

    fetchCarDetails();
  }, [carId]);

  return (
    <div className="booking-page">
      {carDetails ? (
        <div>
          <h2>Book {carDetails.car_model}</h2>
          <p><strong>Price:</strong> ${carDetails.rental_price_per_day} per day</p>
          <p><strong>Location:</strong> {carDetails.pickup_location}</p>
          <button className="btn confirm-booking-btn">Confirm Booking</button>
        </div>
      ) : (
        <p>Loading car details...</p>
      )}
    </div>
  );
}

export default BookingPage;
