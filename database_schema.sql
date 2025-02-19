--database creation
CREATE DATABASE IF NOT EXISTS drive_share;
USE drive_share;

--table to store users
CREATE TABLE Users (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    PasswordHash VARCHAR(255) NOT NULL,
    UserType ENUM('Owner', 'Renter') NOT NULL,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--table to store security questions
CREATE TABLE SecurityQuestions (
    QuestionID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL,
    Question1 VARCHAR(255) NOT NULL,
    Answer1 VARCHAR(255) NOT NULL,
    Question2 VARCHAR(255) NOT NULL,
    Answer2 VARCHAR(255) NOT NULL,
    Question3 VARCHAR(255) NOT NULL,
    Answer3 VARCHAR(255) NOT NULL,
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);

--table to store cars
CREATE TABLE Cars (
    CarID INT AUTO_INCREMENT PRIMARY KEY,
    OwnerID INT NOT NULL,
    Model VARCHAR(100) NOT NULL,
    Year INT NOT NULL,
    Mileage INT NOT NULL,
    AvailabilityStart DATE NOT NULL,
    AvailabilityEnd DATE NOT NULL,
    PickupLocation VARCHAR(255) NOT NULL,
    PricePerDay DECIMAL(10, 2) NOT NULL,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (OwnerID) REFERENCES Users(UserID) ON DELETE CASCADE
);

--table to store bookings
CREATE TABLE Bookings (
    BookingID INT AUTO_INCREMENT PRIMARY KEY,
    CarID INT NOT NULL,
    RenterID INT NOT NULL,
    StartDate DATE NOT NULL,
    EndDate DATE NOT NULL,
    TotalPrice DECIMAL(10, 2) NOT NULL,
    Status ENUM('Pending', 'Confirmed', 'Cancelled') DEFAULT 'Pending',
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (CarID) REFERENCES Cars(CarID) ON DELETE CASCADE,
    FOREIGN KEY (RenterID) REFERENCES Users(UserID) ON DELETE CASCADE
);

--table to store payment
CREATE TABLE Payments (
    PaymentID INT AUTO_INCREMENT PRIMARY KEY,
    BookingID INT NOT NULL,
    Amount DECIMAL(10, 2) NOT NULL,
    PaymentStatus ENUM('Pending', 'Completed') DEFAULT 'Pending',
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (BookingID) REFERENCES Bookings(BookingID) ON DELETE CASCADE
);

--table to store reviews and ratings
CREATE TABLE Reviews (
    ReviewID INT AUTO_INCREMENT PRIMARY KEY,
    BookingID INT NOT NULL,
    ReviewerID INT NOT NULL,
    RevieweeID INT NOT NULL,
    Rating INT CHECK (Rating BETWEEN 1 AND 5),
    Comment TEXT,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (BookingID) REFERENCES Bookings(BookingID) ON DELETE CASCADE,
    FOREIGN KEY (ReviewerID) REFERENCES Users(UserID) ON DELETE CASCADE,
    FOREIGN KEY (RevieweeID) REFERENCES Users(UserID) ON DELETE CASCADE
);

-- table to store messages
CREATE TABLE Messages (
    MessageID INT AUTO_INCREMENT PRIMARY KEY,
    SenderID INT NOT NULL,
    ReceiverID INT NOT NULL,
    Message TEXT NOT NULL,
    SentAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (SenderID) REFERENCES Users(UserID) ON DELETE CASCADE,
    FOREIGN KEY (ReceiverID) REFERENCES Users(UserID) ON DELETE CASCADE
);