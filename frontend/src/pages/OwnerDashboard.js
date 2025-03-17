import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";

function OwnerDashboard() {
  const [listings, setListings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Get the userId from localStorage (assuming user is logged in)
    const userId = localStorage.getItem("userId");

    if (!userId) {
      setError("User not logged in.");
      return;
    }

    // Fetch the owner's car listings from the backend (filter by owner_id)
    const fetchOwnerListings = async () => {
      try {
        const response = await fetch(
          `http://localhost:5000/api/cars?owner_id=${userId}`
        );
        if (response.ok) {
          const data = await response.json();
          setListings(data); // Set the owner's listings to the state
        } else {
          setError("Failed to load your car listings");
        }
      } catch (error) {
        console.log(error);
        setError("An error occurred while fetching your car listings");
      } finally {
        setLoading(false);
      }
    };

    fetchOwnerListings();
  }, []);

  const handleEdit = (carId) => {
    console.log(`Edit car with ID: ${carId}`);
    // Redirect to the edit page or open edit modal
  };

  const handleDelete = async (carId) => {
    const confirmDelete = window.confirm(
      "Are you sure you want to delete this listing?"
    );
    if (confirmDelete) {
      try {
        const response = await fetch(
          `http://localhost:5000/api/cars/${carId}`,
          {
            method: "DELETE",
          }
        );

        if (response.ok) {
          setListings(listings.filter((listing) => listing.id !== carId));
          alert("Listing deleted successfully");
        } else {
          alert("Failed to delete the listing");
        }
      } catch (error) {
        alert("An error occurred while deleting the listing");
      }
    }
  };

  if (loading) {
    return <div>Loading your car listings...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <div>
      <h1>Owner Dashboard</h1>
      <h2>Your Listings</h2>
      <ul>
        {listings.length > 0 ? (
          listings.map((listing) => (
            <li key={listing.id}>
              <h3>
                {listing.car_model} ({listing.car_year})
              </h3>
              <p>{listing.mileage} miles</p>
              <p>Price per day: ${listing.rental_price_per_day}</p>
              <p>
                Available from: {listing.availability_start_date} to{" "}
                {listing.availability_end_date}
              </p>
              <p>Pickup Location: {listing.pickup_location}</p>
              <button onClick={() => handleEdit(listing.id)}>Edit</button>
              <button onClick={() => handleDelete(listing.id)}>Delete</button>
            </li>
          ))
        ) : (
          <div>No listings available at the moment.</div>
        )}
      </ul>
      <Link to="/create-listing">
        <button>Create New Listing</button>
      </Link>
    </div>
  );
}

export default OwnerDashboard;
