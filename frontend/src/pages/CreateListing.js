import React, { useState } from "react";

function CreateListing() {
  // State variables for car details
  const [carModel, setCarModel] = useState("");
  const [carYear, setCarYear] = useState("");
  const [mileage, setMileage] = useState("");
  const [pickupLocation, setPickupLocation] = useState("");
  const [rentalPricePerDay, setRentalPricePerDay] = useState("");
  const [availabilityCalendar, setAvailabilityCalendar] = useState("");

  // Handle form submission
  const handleSubmit = (e) => {
    e.preventDefault();
    // You would likely send this data to an API or store it in a database
    const listingData = {
      carModel,
      carYear,
      mileage,
      pickupLocation,
      rentalPricePerDay,
      availabilityCalendar,
    };

    console.log("New Listing Created:", listingData);

    // Optionally, you could reset the form after submission
    setCarModel("");
    setCarYear("");
    setMileage("");
    setPickupLocation("");
    setRentalPricePerDay("");
    setAvailabilityCalendar("");
  };

  return (
    <div>
      <h1>Create New Listing</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="carModel">Car Model</label>
          <input
            type="text"
            id="carModel"
            value={carModel}
            onChange={(e) => setCarModel(e.target.value)}
            required
          />
        </div>

        <div>
          <label htmlFor="carYear">Car Year</label>
          <input
            type="number"
            id="carYear"
            value={carYear}
            onChange={(e) => setCarYear(e.target.value)}
            required
          />
        </div>

        <div>
          <label htmlFor="mileage">Mileage</label>
          <input
            type="number"
            id="mileage"
            value={mileage}
            onChange={(e) => setMileage(e.target.value)}
            required
          />
        </div>

        <div>
          <label htmlFor="pickupLocation">Pickup Location</label>
          <input
            type="text"
            id="pickupLocation"
            value={pickupLocation}
            onChange={(e) => setPickupLocation(e.target.value)}
            required
          />
        </div>

        <div>
          <label htmlFor="rentalPricePerDay">Rental Price per Day ($)</label>
          <input
            type="number"
            id="rentalPricePerDay"
            value={rentalPricePerDay}
            onChange={(e) => setRentalPricePerDay(e.target.value)}
            required
          />
        </div>

        <div>
          <label htmlFor="availabilityCalendar">Availability Calendar</label>
          <input
            type="text"
            id="availabilityCalendar"
            value={availabilityCalendar}
            onChange={(e) => setAvailabilityCalendar(e.target.value)}
            placeholder="Enter availability (e.g., 2025-04-01 to 2025-04-10)"
            required
          />
        </div>

        <button type="submit">Create Listing</button>
      </form>
    </div>
  );
}

export default CreateListing;
