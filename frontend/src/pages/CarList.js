import { Link } from "react-router-dom";
import "../styles/CarList.css";
import axios from "axios";
import React, { useState, useEffect } from "react";

function CarList() {
  const [cars, setCars] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch cars data from the backend when the component mounts
  useEffect(() => {
    const fetchCars = async () => {
      try {
        // Make API request to fetch cars
        const response = await axios.get("http://localhost:5000/api/cars");
        setCars(response.data); // Update state with the fetched cars
        setLoading(false); // Set loading to false after data is fetched
      } catch (error) {
        setError("Failed to fetch cars"); // Set error if the request fails
        setLoading(false); // Set loading to false even if there is an error
      }
    };

    fetchCars(); // Call the function to fetch cars
  }, []); // Empty array means this effect runs only once when the component mounts

  if (loading) {
    return <div>Loading cars...</div>; // Show loading message while data is being fetched
  }

  if (error) {
    return <div>{error}</div>; // Show error message if something went wrong
  }

  return (
    <div className="car-list-page">
      {/* Title Section */}
      <div className="car-list-header">
        <h1>Browse Available Cars</h1>
        <p>
          Find the perfect car for your next adventure. Rent from local owners
          today!
        </p>
      </div>

      {/* Cars List */}
      <div className="car-list">
        {cars.map((car) => (
          <div key={car.car_id} className="car-item">
            {" "}
            {/* Use car_id instead of id */}
            <div className="car-info">
              <h3>{car.car_model}</h3> {/* Use car_model from backend */}
              <p>Owner: {car.owner}</p> {/* Use owner email from backend */}
              <p>Price: ${car.rental_price_per_day}/day</p>{" "}
              {/* Use rental_price_per_day */}
              <Link to={`/car/${car.car_id}`} className="btn">
                Rent Now
              </Link>{" "}
              {/* Use car_id */}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default CarList;
