import React, { useState } from "react";
import { useNavigate } from "react-router-dom"; // Importing useNavigate from react-router-dom

function CreateListing() {
  const [formData, setFormData] = useState({
    car_model: "",
    car_year: "",
    mileage: "",
    pickup_location: "",
    rental_price_per_day: "",
    availability_start_date: "",
    availability_end_date: "",
  });
  const [error, setError] = useState(""); // For showing form errors
  const [success, setSuccess] = useState(""); // For showing success message
  const navigate = useNavigate(); // Navigation after form submission

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Form validation: Check if any required field is empty
    if (
      !formData.car_model ||
      !formData.car_year ||
      !formData.mileage ||
      !formData.pickup_location ||
      !formData.rental_price_per_day ||
      !formData.availability_start_date ||
      !formData.availability_end_date
    ) {
      setError("All fields must be filled out");
      setSuccess(""); // Reset success message if validation fails
      return; // Stop submission if any required field is empty
    }

    // Get the userId from localStorage (after login)
    const userId = localStorage.getItem("userId");

    // Add userId to the car data you're sending
    const carData = { ...formData, owner_id: userId };

    try {
      const response = await fetch("http://localhost:5000/api/cars", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(carData),
      });

      if (response.ok) {
        // Success: Display success message
        setSuccess("Car listing created successfully!");
        setError(""); // Reset error message
        // Optionally, navigate to another page (e.g., car listings or dashboard)
        setTimeout(() => {
          navigate("/car-list"); // Redirect after success
        }, 2000); // Delay redirect to allow the success message to be visible
      } else {
        // If the backend returns an error
        const data = await response.json();
        setError(data.error || "Error: Could not create car listing");
        setSuccess(""); // Reset success message if error occurs
      }
    } catch (error) {
      console.log("Error:", error);
      setError("An unexpected error occurred. Please try again.");
      setSuccess(""); // Reset success message if error occurs
    }
  };

  return (
    <div className="create-listing-form">
      <h2>Create Car Listing</h2>

      {/* Display success message if any */}
      {success && <p style={{ color: "green" }}>{success}</p>}

      {/* Display error message if any */}
      {error && <p style={{ color: "red" }}>{error}</p>}

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="car_model"
          value={formData.car_model}
          onChange={handleChange}
          placeholder="Car Model"
        />
        <input
          type="number"
          name="car_year"
          value={formData.car_year}
          onChange={handleChange}
          placeholder="Car Year"
        />
        <input
          type="number"
          name="mileage"
          value={formData.mileage}
          onChange={handleChange}
          placeholder="Mileage"
        />
        <input
          type="text"
          name="pickup_location"
          value={formData.pickup_location}
          onChange={handleChange}
          placeholder="Pickup Location"
        />
        <input
          type="number"
          name="rental_price_per_day"
          value={formData.rental_price_per_day}
          onChange={handleChange}
          placeholder="Rental Price Per Day"
        />
        <input
          type="date"
          name="availability_start_date"
          value={formData.availability_start_date}
          onChange={handleChange}
        />
        <input
          type="date"
          name="availability_end_date"
          value={formData.availability_end_date}
          onChange={handleChange}
        />
        <button type="submit">Create Listing</button>
      </form>
    </div>
  );
}

export default CreateListing;
