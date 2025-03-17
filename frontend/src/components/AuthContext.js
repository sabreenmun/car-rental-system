import React, { createContext, useState, useEffect } from "react";

// Create a Context for Authentication
const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userRole, setUserRole] = useState(null);

  useEffect(() => {
    // Check if the token exists in localStorage when the app first loads
    const token = localStorage.getItem("token");
    const role = localStorage.getItem("user_role");

    if (token) {
      setIsLoggedIn(true);
      setUserRole(role);
    }
  }, []);

  const login = (role, token) => {
    localStorage.setItem("token", token);
    localStorage.setItem("user_role", role);
    setIsLoggedIn(true);
    setUserRole(role);
  };

  const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user_role");
    setIsLoggedIn(false);
    setUserRole(null);
  };

  return (
    <AuthContext.Provider value={{ isLoggedIn, userRole, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;
