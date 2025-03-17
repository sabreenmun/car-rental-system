import React from "react";
import "../styles/Help.css"; // Make sure you import the corresponding CSS

function Help() {
  return (
    <div className="help-page">
      <h1>How to Use DriveShare</h1>

      <div className="step-section">
        <h2>Step 1: Create an Account</h2>
        <p>
          Sign up with your email and password. You'll also need to answer 3
          security questions to ensure your account is secure.
        </p>
      </div>

      <div className="step-section">
        <h2>Step 2: Choose Your Role</h2>
        <p>
          When you sign up, you'll need to choose your role. Are you a car owner
          or a car renter? This will help guide your next steps.
        </p>
      </div>

      <div className="step-section">
        <h2>Step 3: If You're a Car Owner</h2>
        <p>
          List your car for rent. Add details like your car model, availability,
          pickup location, and rental price. You can manage your listings from
          the dashboard.
        </p>
      </div>

      <div className="step-section">
        <h2>Step 4: If You're a Car Renter</h2>
        <p>
          Browse available cars by location and date. Select a car that fits
          your needs, and make a booking! Once confirmed, you can pick up your
          rental at the listed location.
        </p>
      </div>
    </div>
  );
}

export default Help;
