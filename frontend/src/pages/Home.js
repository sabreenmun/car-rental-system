import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "../styles/Home.css";

function Home() {
  const [searchQuery, setSearchQuery] = useState({
    location: "",
    startDate: "",
    endDate: "",
    price: "",
  });
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSearchChange = (e) => {
    const { name, value } = e.target;
    setSearchQuery((prevState) => ({
      ...prevState,
      [name]: value,
    }));
  };

  const handleSearchSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (!searchQuery.location) {
      setError("Please enter a pickup location.");
      return;
    }

    try {
      const queryParams = new URLSearchParams({
        location: searchQuery.location,
        startDate: searchQuery.startDate,
        endDate: searchQuery.endDate,
        price: searchQuery.price,
      }).toString();

      // Pass query parameters directly to the car-list page
      navigate(`/car-list?${queryParams}`);
    } catch (error) {
      setError("Error fetching cars. Please try again later.");
      console.error(error);
    }
  };

  return (
    <div className="home-page">
      <div className="main-area1">
        <h1>Welcome to DriveShare</h1>
        <h2>Peer-to-Peer Car Rentals</h2>
        <p>
          Rent a car directly from local owners or list your own to earn money.
        </p>

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

        <div className="home-buttons">
          <Link to="/login" className="btn">
            Login
          </Link>
          <Link to="/register" className="btn">
            Join Now
          </Link>
        </div>
      </div>

      <div className="main-area2">
        <h2>Recent Feedback</h2>
        <ul className="feedback-list">
          {["Bob M.", "Mark I.", "Jessica M.", "Ashley M."].map(
            (user, index) => (
              <li key={index} className="feedback-item">
                <p>
                  <strong>{user}</strong>: Great experience! Highly recommend.
                </p>
                <p>⭐ 5/5</p>
              </li>
            )
          )}
        </ul>
      </div>
    </div>
  );
}

export default Home;
