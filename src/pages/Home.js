import React from "react";
import { Link } from "react-router-dom";
import "./Home.css";

function Home() {
  return (
    <div className="home-page">
      <div className="main-area1">
        <h2>DriveConnect Solutions</h2>
        <h3>Peer-to-Peer Car Rentals</h3>
        <p>
          Lorem ipsum dolor sit amet, consectetur adipisicing elit. Beatae fuga
          laudantium quibusdam sequi totam veniam?
        </p>
        <Link to="/login">Login</Link>
      </div>
      <div className="main-area2">
        <h2>Recent Feedback</h2>
        {/* pop feedback items here*/}
      </div>
    </div>
  );
}

export default Home;
