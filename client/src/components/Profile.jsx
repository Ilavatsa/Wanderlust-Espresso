import React from 'react';

const CompanyProfile = ({ company }) => {
    return (
        <div className="profile-container">
            <div className="profile-content">
                <div className="profile-details-container">
                    <h2>Company Profile</h2>
                    <p><strong>Company Name:</strong> {company?.companyName || 'N/A'}</p>
                    <p><strong>Email:</strong> {company?.email || 'N/A'}</p>
                    <p><strong>Industry:</strong> {company?.industry || 'N/A'}</p>
                </div>
                <div className="profile-image-container">
                    <img
                        src="https://i.pinimg.com/564x/25/ae/6c/25ae6caefb45b4cd3880ffa14ced3bf4.jpg"
                        alt="Company Profile"
                        className="profile-image"
                    />
                </div>
            </div>
        </div>
    );
};

export default CompanyProfile;
