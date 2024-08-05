import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

function CategoryPage() {
    const { category } = useParams();
    const [items, setItems] = useState([]);
    const [categoryName, setCategoryName] = useState('');

    useEffect(() => {
        fetch(`http://127.0.0.1:5000/menu/${category}`)
            .then(response => response.json())
            .then(data => {
                setItems(data);
                setCategoryName(category);
            })
            .catch(error => console.error('Error fetching items:', error));
    }, [category]);

    return (
        <div>
            <h2>{categoryName.charAt(0).toUpperCase() + categoryName.slice(1)}</h2>
            <div className="menu-container">
                {items.map(item => (
                    <div key={item.id} className="menu-card">
                        <h3 className='menu-name'>{item.name}</h3>
                        <img className="menu-img" src={item.image_url} alt={item.name} />
                        <div className='menu-details'>
                            <p>${item.price}</p>
                            <p>{item.description}</p>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default CategoryPage;
