import React from "react";
import { Link } from "react-router-dom";
import "../styles/Home.css";

function Home() {
  const recentReviews = [
    { id: 1, user: "Reem M.", comment: "Great experience! The car was clean and smooth to drive.", rating: 5 },
    { id: 2, user: "Mariam I.", comment: "Super easy booking process. Will use again!", rating: 4 },
    { id: 3, user: "Sabreen M.", comment: "Owner was very responsive. Car was in great condition.", rating: 5 },
    { id: 3, user: "Doaa M.", comment: "Had a great experience on here. Highly recommend!", rating: 5 }
  ];

  return (
    <div className="home-page">
      {/* Main Section */}
      <div className="main-area1">
        <h1>Welcome to DriveShare</h1>
        <h2>Peer-to-Peer Car Rentals</h2>
        <p>
          Rent a car directly from local owners, or list your own car to earn money.
          A secure and seamless rental experience designed for everyone.
        </p>
        <div className="home-buttons">
          <Link to="/login" className="btn">Login</Link>
          <Link to="/register" className="btn">Join Now</Link>
        </div>
      </div>

      {/* Recent Feedback Section */}
      <div className="main-area2">
        <h2>Recent Feedback</h2>
        <ul className="feedback-list">
          {recentReviews.map((review) => (
            <li key={review.id} className="feedback-item">
              <p><strong>{review.user}</strong>: {review.comment}</p>
              <p>⭐ {review.rating}/5</p>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default Home;
