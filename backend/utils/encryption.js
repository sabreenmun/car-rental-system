// utils/encryption.js
const bcrypt = require('bcrypt');
const saltRounds = 10;

// Hash a password
const hashPassword = (password) => {
  return bcrypt.hashSync(password, saltRounds);
};

// Verify a password
const verifyPassword = (password, hash) => {
  return bcrypt.compareSync(password, hash);
};

module.exports = { hashPassword, verifyPassword };