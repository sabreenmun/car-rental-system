import { Route, Routes } from "react-router-dom";
import Home from "./pages/Home";
import About from "./pages/About";
import Help from "./pages/Help";
import Login from "./pages/Login";
import Register from "./pages/Register";
import "./styles/App.css";
import Navbar from './components/Navbar';
import Footer from "./components/Footer";
import CarList from "./pages/CarList";
import CreateListing from "./pages/CreateListing";
function App() {
  return (
    <div className="App">
      {/* Navbar will appear on all pages */}
      <Navbar />

      <div className="main-content">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/home" element={<Home />} />
          <Route path="/about" element={<About />} />
          <Route path="/help" element={<Help />} />
          <Route path="/login" element={<Login />} />
          <Route path="/search-cars" element={<CarList />} />
          <Route path="/register" element={<Register />} />
          <Route path="/create-listing" element = {<CreateListing/>}/>
        </Routes>
      </div>

      {/* Footer will appear on all pages */}
      <Footer />
    </div>
  );
}

export default App;
