import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

function CreateListing() {
  const [car_model, setCarModel] = useState("");
  const [car_year, setCarYear] = useState("");
  const [mileage, setMileage] = useState("");
  const [pickup_location, setPickupLocation] = useState("");
  const [rental_price_per_day, setRentalPricePerDay] = useState("");
  const [availability_calendar, setAvailabilityCalendar] = useState(""); // This can be a JSON or a string of dates
  const [errorMessage, setErrorMessage] = useState("");
  const navigate = useNavigate();

  // Check if the user is an owner
  const isOwner = JSON.parse(localStorage.getItem("user"))?.user_type === "Owner";

  // If the user is not an owner, redirect them to another page
  if (!isOwner) {
    navigate("/home"); // Redirect to home or any other page if the user is not an owner
  }

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Prepare the car data to send to the server
    const carData = {
      owner_id: JSON.parse(localStorage.getItem("user")).user_id, // Assuming user_id is stored in localStorage
      car_model: car_model,
      car_year: car_year,
      mileage: mileage,
      pickup_location: pickup_location,
      rental_price_per_day: rental_price_per_day,
      availability_calendar: availability_calendar,
    };

    try {
      const response = await axios.post("http://localhost:5000/api/cars", carData);
      if (response.status === 201) {
        alert("Car listing created successfully!");
        navigate("/dashboard"); // Redirect to the owner's dashboard or a success page
      }
    } catch (error) {
      setErrorMessage("Error creating car listing. Please try again.");
    }
  };

  return (
    <div className="create-listing-page">
      <h2>Create a New Car Listing</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Car Model:</label>
          <input
            type="text"
            value={car_model}
            onChange={(e) => setCarModel(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Car Year:</label>
          <input
            type="number"
            value={car_year}
            onChange={(e) => setCarYear(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Mileage:</label>
          <input
            type="number"
            value={mileage}
            onChange={(e) => setMileage(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Pickup Location:</label>
          <input
            type="text"
            value={pickup_location}
            onChange={(e) => setPickupLocation(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Rental Price per Day:</label>
          <input
            type="number"
            value={rental_price_per_day}
            onChange={(e) => setRentalPricePerDay(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Availability Calendar (e.g., ["2025-03-10", "2025-03-11"]):</label>
          <input
            type="text"
            value={availability_calendar}
            onChange={(e) => setAvailabilityCalendar(e.target.value)}
            required
          />
        </div>
        <button type="submit">Create Listing</button>
      </form>
      {errorMessage && <p style={{ color: "red" }}>{errorMessage}</p>}
    </div>
  );
}

export default CreateListing;
