import React from "react";
import carpic from "../images/mercedes.jpeg";
import "../styles/About.css"; // Import the CSS file

function About() {
  return (
    <div className="about-page">
      <div className="main-area1">
        <h2>Who We Are</h2>
        <p>
          DriveShare is a peer-to-peer car rental platform that connects car owners 
          with individuals looking for short-term vehicle rentals. We aim to provide a 
          seamless, secure, and efficient experience for both renters and owners.
        </p>
        <img src={carpic} alt="Luxury Car" className="about-image" />
      </div>

      <div className="main-area2">
        <h2>Our Future</h2>
        <p>
          We envision expanding our services globally, integrating AI-driven recommendations, 
          and enhancing security features to provide an even better experience for our users.
        </p>
      </div>
    </div>
  );
}

export default About;
