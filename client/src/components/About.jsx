import React from "react";
import Contact from "./Contact"; // Import the Contact component

const About = () => {
  return (
    <div className="container">
      <main className="main">
        <div className="content">
          <div className="image-container">
            <img src="https://i.pinimg.com/736x/51/ab/5f/51ab5fe403ac155caa499413d86d84c1.jpg" alt="About Us" />
          </div>
          <div className="text-container">
            <h1>About Our Cafe</h1>
            <p>
              Welcome to Our Cafe, your neighborhood's favorite spot for fresh coffee, delicious pastries, and a relaxing atmosphere. We pride ourselves on serving high-quality beverages and food, made with the finest ingredients.
            </p>
            <h2>Our Team</h2>
            <p>
              Our team is composed of passionate baristas, talented bakers, and friendly staff who are dedicated to creating the perfect cafe experience for you. We are committed to exceptional service and hospitality.
            </p>
            <h2>Our Story</h2>
            <p>
              Established in 2008, Our Cafe has become a beloved community hub. Our journey began with a passion for great coffee and a desire to create a welcoming space for people to relax and connect. Over the years, we have grown, but our commitment to quality and community remains at the heart of everything we do.
            </p>
          </div>
        </div>
      </main>
    </div>
  );
};

export default About;

