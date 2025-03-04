import React from "react";
import { Link, useLocation } from "react-router-dom";
import "./Header.css";

const Header = () => {
  const location = useLocation();
  const currentPath = location.pathname;

  return (
    <header className="header">
      <div className="header-container">
        <div className="header-left">
          <Link
            to="/"
            className={`nav-link ${currentPath === "/" ? "active" : ""}`}
          >
            Search
          </Link>
          <Link
            to="/semantic"
            className={`nav-link ${
              currentPath === "/semantic" ? "active" : ""
            }`}
          >
            Semantic Search
          </Link>
        </div>
        <div className="header-right">
          <Link
            to="/signup"
            className={`nav-link ${currentPath === "/signup" ? "active" : ""}`}
          >
            Sign Up
          </Link>
          <Link
            to="/signin"
            className={`nav-link ${currentPath === "/signin" ? "active" : ""}`}
          >
            Sign In
          </Link>
        </div>
      </div>
    </header>
  );
};

export default Header;
