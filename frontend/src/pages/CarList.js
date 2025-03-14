import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";

function CarList() {
  const [cars, setCars] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCars = async () => {
      try {
        const response = await fetch("http://localhost:5000/api/cars"); // Backend API endpoint
        const data = await response.json();
        setCars(data); // Update the state with car listings
        setLoading(false);
      } catch (error) {
        console.error("Error fetching car listings", error);
        setLoading(false);
      }
    };

    fetchCars();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="car-listings">
      {cars.length === 0 ? (
        <p>No cars available for rent at the moment.</p>
      ) : (
        cars.map((car) => (
          <div className="car-card" key={car.id}>
            <img src={car.imageUrl} alt={car.model} />
            <h3>{car.model}</h3>
            <p>Year: {car.year}</p>
            <p>Mileage: {car.mileage} miles</p>
            <p>Price per day: ${car.rental_price_per_day}</p>
            <Link to={`/car-details/${car.id}`} className="btn-details">
              View Details
            </Link>
          </div>
        ))
      )}
    </div>
  );
}

export default CarList;
