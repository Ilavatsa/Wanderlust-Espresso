import React from 'react';
import '../App.css';  // Ensure the path to app.css is correct

function Home() {
  return (
    <div className="home-container">
      <img 
        src="https://i.pinimg.com/564x/75/a7/26/75a72667562362fc353f35b5789dcd1a.jpg" 
        alt="Cafe" 
        className="home-image"  // Apply the CSS class
      />
      <div className="home-content">
        <h1>Welcome to Our Cafe!</h1>
        <p>Enjoy our delicious coffee and snacks.</p>
      </div>
    </div>
  );
}

export default Home;


