import React from "react";
import { Link } from "react-router-dom";
import "./Header.css";

const Header = () => {
  return (
    <header className="header">
      <div className="header-container">
        <div className="header-left">
          <Link to="/" className="nav-link home-link">
            Home
          </Link>
        </div>
        <div className="header-right">
          <Link to="/signup" className="nav-link">
            Sign Up
          </Link>
          <Link to="/signin" className="nav-link">
            Sign In
          </Link>
        </div>
      </div>
    </header>
  );
};

export default Header;
