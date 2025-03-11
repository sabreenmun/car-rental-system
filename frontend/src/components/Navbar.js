import React, { useState, useEffect } from "react";
import { NavLink, Link, useNavigate } from "react-router-dom";
import "../styles/Navbar.css";

function Navbar() {
  const [menuOpen, setMenuOpen] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userRole, setUserRole] = useState(null); // Track user role
  const navigate = useNavigate();

  useEffect(() => {
    // Check if the user is logged in (look for the JWT token in localStorage)
    const token = localStorage.getItem('token');
    const role = localStorage.getItem('user_role');
    
    if (token) {
      setIsLoggedIn(true); // User is logged in
      setUserRole(role);   // Set the user role if logged in
    } else {
      setIsLoggedIn(false); // User is not logged in
      setUserRole(null);    // No role assigned
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token'); // Remove token from localStorage
    localStorage.removeItem('user_role'); // Remove user role from localStorage
    setIsLoggedIn(false); // Update login state to false
    setUserRole(null); // Clear the user role
    navigate('/login'); // Redirect to login page
  };

  return (
    <nav>
      <Link to="/" className="title">
        DriveShare
      </Link>
      <div
        className="menu"
        onClick={() => setMenuOpen(!menuOpen)}
      >
        <span></span>
        <span></span>
        <span></span>
      </div>
      <ul className={menuOpen ? "open" : ""}>
        <li>
          <NavLink to="/home">Home</NavLink>
        </li>
        <li>
          <NavLink to="/about">About</NavLink>
        </li>
        <li>
          <NavLink to="/help">Help</NavLink>
        </li>
        <li>
          <NavLink to="/search-cars">Search Cars</NavLink>
        </li>

        {/* Conditionally render login and register links if the user is not logged in */}
        {!isLoggedIn ? (
          <>
            <li>
              <NavLink to="/login">Login</NavLink>
            </li>
            <li>
              <NavLink to="/register">Register</NavLink>
            </li>
          </>
        ) : (
          <>
            {/* Show dashboard link based on user role */}
            {userRole === 'Owner' && (
              <>
                <li>
                  <NavLink to="/owner-dashboard">Owner Dashboard</NavLink>
                </li>
                <li>
                  <NavLink to="/create-listing">Create Listing</NavLink>
                </li>
              </>
            )}
            {/* Show Renter's dashboard link */}
            {userRole === 'Renter' && (
              <li>
                <NavLink to="/renter-dashboard">Renter Dashboard</NavLink>
              </li>
            )}

            {/* Logout button */}
            <li>
              <button onClick={handleLogout}>Logout</button>
            </li>
          </>
        )}
      </ul>
    </nav>
  );
}

export default Navbar;
