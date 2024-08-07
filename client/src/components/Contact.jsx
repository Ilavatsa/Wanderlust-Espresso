import React from 'react';
import { FaInstagramSquare, FaFacebookSquare } from 'react-icons/fa';
import { BiLogoTelegram } from 'react-icons/bi';
import { AiFillTikTok } from 'react-icons/ai';

const Contact = () => {
  return (
    <div id="contact">
      <h1>Contact Our Company</h1>
      <div className="company-info">
        <p>Email: <a href="mailto:info@company.com">info@company.com</a></p>
        <p>Phone: <a href="tel +254710413311">+254710413311</a></p>
        <p>Location: 123 Business St, Suite 456, City, Country</p>
      </div>
      <h2>Connect with Us</h2>
      <div className="social-media-links">
        <a
          href="https://www.instagram.com/company_username"
          target="_blank"
          rel="noopener noreferrer"
        >
          <FaInstagramSquare />
        </a>
        <a
          href="https://www.facebook.com/company_username"
          target="_blank"
          rel="noopener noreferrer"
        >
          <FaFacebookSquare />
        </a>
        <a
          href="https://t.me/company_username"
          target="_blank"
          rel="noopener noreferrer"
        >
          <BiLogoTelegram />
        </a>
        <a
          href="https://www.tiktok.com/@company_username"
          target="_blank"
          rel="noopener noreferrer"
        >
          <AiFillTikTok />
        </a>
      </div>
    </div>
  );
};

export default Contact;
