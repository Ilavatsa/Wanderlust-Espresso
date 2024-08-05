import React, { useState } from 'react';
import { FaUserAlt } from 'react-icons/fa';
import { Link, useNavigate } from 'react-router-dom';

function Navbar() {
  const [isUserDropdown, setIsUserDropdown] = useState(false);
  const navigate = useNavigate();

  function toggleUserDown() {
    setIsUserDropdown(!isUserDropdown);
  }

  function handleSignOut() {
    console.log('Signing out...');
    localStorage.removeItem('access_token');
    localStorage.removeItem('name');
    localStorage.removeItem('email');
    localStorage.removeItem('role');
    console.log('Redirecting to login page...');
    navigate('/login');
  }

  return (
    <nav className="navbar">
      <div className="logo">
        <span className="store-name">Cafe Delight</span>
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
          <Link to="/about#contact">Contact</Link> {/* Updated Link */}
        </li>
        <li className="navbar-user">
          <FaUserAlt onClick={toggleUserDown} />
          {isUserDropdown && (
            <ul className="dropdown">
              <li><Link to='/profile'>Profile</Link></li>
              <li><Link to='/login'>Login</Link></li>
              <li><Link to='/signup'>Sign-up</Link></li>
              <li><a href="#sign-out" onClick={handleSignOut}>Sign-out</a></li>
            </ul>
          )}
        </li>
      </ul>
    </nav>
  );
}

export default Navbar;

