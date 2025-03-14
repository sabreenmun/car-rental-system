import React from "react";
import CarList from "./CarList"; // Import CarList component

function RenterDashboard() {
  return (
    <div className="renter-dashboard">
      <h2>Welcome to Your Renter Dashboard</h2>
      <p>Explore available cars for rent and make your selection.</p>

      {/* Include the CarList component to display available cars */}
      <CarList />
    </div>
  );
}

export default RenterDashboard;
