import React, { useState } from 'react';
import "../styles/SearchCars.css";
function SearchCars() {
  const [location, setLocation] = useState('');
  const [date, setDate] = useState('');
  const [carType, setCarType] = useState('');

  const handleSearch = () => {
    // In a real app, you would send a search request to a backend API or filter an array of cars
    console.log('Searching for cars...');
    console.log('Location:', location);
    console.log('Date:', date);
    console.log('Car Type:', carType);
  };

  return (
    <div>
      <h1>Search Cars</h1>
      <p>Find the perfect car for your trip! Use our filters to search by location, date, and type of car.</p>

      <div>
        <label>
          Location:
          <input
            type="text"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            placeholder="Enter location"
          />
        </label>
      </div>

      <div>
        <label>
          Date:
          <input
            type="date"
            value={date}
            onChange={(e) => setDate(e.target.value)}
          />
        </label>
      </div>

      <div>
        <label>
          Car Type:
          <select
            value={carType}
            onChange={(e) => setCarType(e.target.value)}
          >
            <option value="">Select car type</option>
            <option value="sedan">Sedan</option>
            <option value="suv">SUV</option>
            <option value="truck">Truck</option>
            <option value="convertible">Convertible</option>
          </select>
        </label>
      </div>

      <button onClick={handleSearch}>Search</button>
    </div>
  );
}

export default SearchCars;
