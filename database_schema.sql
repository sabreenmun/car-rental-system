-- Create the database
CREATE DATABASE IF NOT EXISTS DriveShare;
USE DriveShare;

-- Users Table
CREATE TABLE IF NOT EXISTS Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    security_question_1 VARCHAR(255) NOT NULL,
    security_answer_1 VARCHAR(255) NOT NULL,
    security_question_2 VARCHAR(255) NOT NULL,
    security_answer_2 VARCHAR(255) NOT NULL,
    security_question_3 VARCHAR(255) NOT NULL,
    security_answer_3 VARCHAR(255) NOT NULL,
    user_type ENUM('owner', 'renter') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Cars Table
CREATE TABLE IF NOT EXISTS Cars (
    car_id INT AUTO_INCREMENT PRIMARY KEY,
    owner_id INT NOT NULL,
    car_model VARCHAR(255) NOT NULL,
    car_year INT NOT NULL,
    mileage INT NOT NULL,
    pickup_location VARCHAR(255) NOT NULL,
    rental_price_per_day DECIMAL(10, 2) NOT NULL,
    availability_calendar JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- Bookings Table
CREATE TABLE IF NOT EXISTS Bookings (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    car_id INT NOT NULL,
    renter_id INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    total_cost DECIMAL(10, 2) NOT NULL,
    booking_status ENUM('pending', 'confirmed', 'completed', 'cancelled') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (car_id) REFERENCES Cars(car_id) ON DELETE CASCADE,
    FOREIGN KEY (renter_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- Payments Table
CREATE TABLE IF NOT EXISTS Payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    payment_status ENUM('pending', 'completed') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (booking_id) REFERENCES Bookings(booking_id) ON DELETE CASCADE
);

-- Messages Table
CREATE TABLE IF NOT EXISTS Messages (
    message_id INT AUTO_INCREMENT PRIMARY KEY,
    sender_id INT NOT NULL,
    receiver_id INT NOT NULL,
    message_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (receiver_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- Reviews Table
CREATE TABLE IF NOT EXISTS Reviews (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT NOT NULL,
    reviewer_id INT NOT NULL,
    reviewee_id INT NOT NULL,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    review_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (booking_id) REFERENCES Bookings(booking_id) ON DELETE CASCADE,
    FOREIGN KEY (reviewer_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (reviewee_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- Rental History Table
CREATE TABLE IF NOT EXISTS RentalHistory (
    rental_history_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    booking_id INT NOT NULL,
    role ENUM('owner', 'renter') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (booking_id) REFERENCES Bookings(booking_id) ON DELETE CASCADE
);

-- Availability Table (Optional, if not using JSON in Cars table)
CREATE TABLE IF NOT EXISTS Availability (
    availability_id INT AUTO_INCREMENT PRIMARY KEY,
    car_id INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (car_id) REFERENCES Cars(car_id) ON DELETE CASCADE
);

-- Indexes for better performance
CREATE INDEX idx_users_email ON Users(email);
CREATE INDEX idx_cars_owner_id ON Cars(owner_id);
CREATE INDEX idx_bookings_car_id ON Bookings(car_id);
CREATE INDEX idx_bookings_renter_id ON Bookings(renter_id);
CREATE INDEX idx_payments_booking_id ON Payments(booking_id);
CREATE INDEX idx_messages_sender_id ON Messages(sender_id);
CREATE INDEX idx_messages_receiver_id ON Messages(receiver_id);
CREATE INDEX idx_reviews_booking_id ON Reviews(booking_id);
CREATE INDEX idx_rental_history_user_id ON RentalHistory(user_id);
CREATE INDEX idx_rental_history_booking_id ON RentalHistory(booking_id);
CREATE INDEX idx_availability_car_id ON Availability(car_id);