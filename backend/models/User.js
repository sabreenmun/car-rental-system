// models/User.js
const db = require("../config/db");

class User {
  static create(user, callback) {
    const {
      email,
      password_hash,
      security_question_1,
      security_answer_1,
      security_question_2,
      security_answer_2,
      security_question_3,
      security_answer_3,
      user_type,
    } = user;
    const query = `
      INSERT INTO Users (email, password_hash, security_question_1, security_answer_1, security_question_2, security_answer_2, security_question_3, security_answer_3, user_type)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    `;
    db.query(
      query,
      [
        email,
        password_hash,
        security_question_1,
        security_answer_1,
        security_question_2,
        security_answer_2,
        security_question_3,
        security_answer_3,
        user_type,
      ],
      callback
    );
  }

  static findByEmail(email, callback) {
    const query = "SELECT * FROM Users WHERE email = ?";
    db.query(query, [email], callback);
  }

  static updatePassword(email, newPasswordHash, callback) {
    const query = "UPDATE Users SET password_hash = ? WHERE email = ?";
    db.query(query, [newPasswordHash, email], callback);
  }
}

module.exports = User;
