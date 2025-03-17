import "../styles/Navbar.css";
import React, { useContext } from "react";
import { Link, useNavigate } from "react-router-dom";
import AuthContext from "../components/AuthContext"; // Import the AuthContext

function Navbar() {
  const { isLoggedIn, userRole, logout } = useContext(AuthContext); // Access login state and logout function
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  return (
    <nav>
      <ul>
        <li>
          <Link to="/">Home</Link>
        </li>
        <li>
          <Link to="/about">About</Link>
        </li>
        <li>
          <Link to="/help">Help</Link>
        </li>

        {isLoggedIn && userRole === "Renter" && (
          <>
            <li>
              <Link to="/renter-dashboard">Renter Dashboard</Link>
            </li>
            <li>
              <Link to="/search-cars">Search Cars</Link>
            </li>
          </>
        )}

        {isLoggedIn && userRole === "Owner" && (
          <>
            <li>
              <Link to="/owner-dashboard">Owner Dashboard</Link>
            </li>
            <li>
              <Link to="/create-listing">Create Listing</Link>
            </li>
          </>
        )}

        {!isLoggedIn ? (
          <>
            <li>
              <Link to="/login">Login</Link>
            </li>
            <li>
              <Link to="/register">Register</Link>
            </li>
          </>
        ) : (
          <li>
            <button onClick={handleLogout}>Logout</button>
          </li>
        )}
      </ul>
    </nav>
  );
}

export default Navbar;
