import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";

function OwnerDashboard() {
  const [listings, setListings] = useState([]);

  useEffect(() => {
    // Fetch the owner's car listings (from an API or localStorage)
    const fetchedListings = [
      { id: 1, carName: "Tesla Model S", available: true },
      { id: 2, carName: "BMW 3 Series", available: false },
    ];
    setListings(fetchedListings);
  }, []);

  return (
    <div>
      <h1>Owner Dashboard</h1>
      <h2>Your Listings</h2>
      <ul>
        {listings.map((listing) => (
          <li key={listing.id}>
            {listing.carName} -{" "}
            {listing.available ? "Available" : "Not Available"}
            <button>Edit</button>
            <button>Delete</button>
          </li>
        ))}
      </ul>
      <Link to="/create-listing">
        <button>Create New Listing</button>
      </Link>
    </div>
  );
}

export default OwnerDashboard;
