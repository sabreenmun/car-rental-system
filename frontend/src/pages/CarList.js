import React, { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import "../styles/CarList.css";

function CarList() {
  const navigate = useNavigate();
  const location = useLocation();

  // State for storing cars and search filters
  const [cars, setCars] = useState([]);
  const [filters, setFilters] = useState({
    location: "",
    maxPrice: "",
  });
  const [loading, setLoading] = useState(true);

  // Get the user role from localStorage to check if they're an owner or renter
  const userRole = localStorage.getItem("user_role");

  // Parse query parameters from URL
  useEffect(() => {
    const queryParams = new URLSearchParams(location.search);
    const searchFilters = {
      location: queryParams.get("location") || "",
      startDate: queryParams.get("startDate") || "",
      endDate: queryParams.get("endDate") || "",
      price: queryParams.get("price") || "",
    };
    setFilters(searchFilters);
  }, [location]);

  // Fetch cars based on the filters
  useEffect(() => {
    const fetchCars = async () => {
      setLoading(true);

      // Construct the query parameters for the search filters
      const queryParams = new URLSearchParams(filters).toString();

      try {
        const response = await fetch(
          `http://localhost:5000/api/cars/search?${queryParams}`,
          {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
            },
          }
        );

        const data = await response.json();
        setCars(data.cars || []); // Ensure that data.cars is used and falls back to empty array if undefined
      } catch (error) {
        console.error("Error fetching cars:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchCars();
  }, [filters]); // Fetch cars whenever filters change

  // Function to handle the booking action
  const handleBook = (carId) => {
    if (userRole === "Renter") {
      navigate(`/booking-page/${carId}`); // Redirect renter to the booking page
    } else {
      alert("Only renters can book cars!");
    }
  };

  return (
    <div className="car-list">
      <form onSubmit={handleSearchSubmit} className="search-form">
        <input
          type="text"
          name="location"
          value={searchQuery.location}
          onChange={handleSearchChange}
          placeholder="Enter pickup location"
          required
        />
        <input
          type="date"
          name="startDate"
          value={searchQuery.startDate}
          onChange={handleSearchChange}
        />
        <input
          type="date"
          name="endDate"
          value={searchQuery.endDate}
          onChange={handleSearchChange}
        />
        <input
          type="number"
          name="price"
          value={searchQuery.price}
          onChange={handleSearchChange}
          placeholder="Max Price per Day"
          min="0"
        />
        {error && <p className="error-message">{error}</p>}
        <button type="submit" className="btn">
          Search
        </button>
      </form>
      <h2>Available Cars</h2>

      {/* Loading Spinner or Placeholder */}
      {loading ? (
        <p>Loading cars...</p>
      ) : (
        <div className="car-catalog">
          {cars.length === 0 ? (
            <p>No available cars at this moment</p>
          ) : (
            cars.map((car) => (
              <div key={car.car_id} className="car-item">
                <h3>{car.car_model}</h3>
                <p>
                  <strong>Price:</strong> ${car.rental_price_per_day} per day
                </p>
                <p>
                  <strong>Location:</strong> {car.pickup_location}
                </p>

                {/* Book button only for Renters */}
                <button
                  className="btn book-btn"
                  onClick={() => handleBook(car.car_id)}
                  disabled={userRole !== "Renter"}
                >
                  {userRole === "Renter" ? "Book" : "Only Renters Can Book"}
                </button>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
}

export default CarList;
