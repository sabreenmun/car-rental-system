import { Route, Routes } from "react-router-dom";
import { AuthProvider } from "./components/AuthContext"; // Import the AuthProvider
import Home from "./pages/Home";
import About from "./pages/About";
import Help from "./pages/Help";
import Login from "./pages/Login";
import Register from "./pages/Register";
import CarList from "./pages/CarList";
import CreateListing from "./pages/CreateListing";
import OwnerDashboard from "./pages/OwnerDashboard";
import RenterDashboard from "./pages/RenterDashboard";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import BookingPage from "./pages/BookingPage";
import "./styles/App.css";

function App() {
  return (
    <AuthProvider>
      <div className="App">
        {/* Navbar will appear on all pages */}
        <Navbar />

        <div className="main-content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/about" element={<About />} />
            <Route path="/help" element={<Help />} />
            <Route path="/login" element={<Login />} />
            <Route path="/car-list" element={<CarList />} />
            <Route path="/register" element={<Register />} />
            <Route path="/create-listing" element={<CreateListing />} />
            <Route path="/booking-page" element={<BookingPage />} />

            {/* Add Owner and Renter Dashboards */}
            <Route path="/owner-dashboard" element={<OwnerDashboard />} />
            <Route path="/renter-dashboard" element={<RenterDashboard />} />
          </Routes>
        </div>

        {/* Footer will appear on all pages */}
        <Footer />
      </div>
    </AuthProvider>
  );
}

export default App;
