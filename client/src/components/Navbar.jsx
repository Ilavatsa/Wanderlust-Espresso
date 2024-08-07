import React from 'react';
import { FaUserAlt } from 'react-icons/fa';
import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <nav className="navbar">
      <div className="logo">
        <span className="store-name">WANDERLUST ESPRESSO</span>
      </div>
      <ul className="navbar-links">
        <li>
          <Link to="/">Home</Link>
        </li>
        <li>
          <Link to="/menu">Menu</Link>
        </li>
        <li>
          <Link to="/about">About Us</Link>
        </li>
        <li>
          <Link to="/about#contact">Contact</Link>
        </li>
        <li>
          <Link to="/profile">
            <FaUserAlt /> Profile
          </Link>
        </li>
      </ul>
    </nav>
  );
}

export default Navbar;

