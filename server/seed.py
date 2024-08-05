#!/usr/bin/env python3

from app import app
from models import db, User, MenuItem, Order, OrderItem
from datetime import date

with app.app_context():
    print("Deleting data...")
    OrderItem.query.delete()
    Order.query.delete()
    MenuItem.query.delete()
    User.query.delete()

    print("Creating users...")
    user1 = User(name="John Doe", email="john@example.com", password="password", role="customer", phone_number="1234567890")
    user2 = User(name="Jane Smith", email="jane@example.com", password="password", role="customer", phone_number="0987654321")
    admin = User(name="Admin User", email="admin@example.com", password="password", role="admin", phone_number="1122334455")
    users = [user1, user2, admin]

    print("Creating menu items...")
    coffee = [
        MenuItem(name="Caramel Hazelnut Iced Coffee", price=0.50, category="Coffee", stock_quantity=100, image_url="https://i.pinimg.com/564x/5c/fd/93/5cfd93bf09153e97707fff073ccd309c.jpg"),
        MenuItem(name="Americano", price=0.30, category="Coffee", stock_quantity=150, image_url="https://i.pinimg.com/564x/2d/02/00/2d02004d251ba299f9fb32549ee75e8d.jpg"),
        MenuItem(name="Iced Americano", price=0.40, category="Coffee", stock_quantity=120, image_url="https://i.pinimg.com/236x/cb/48/db/cb48db04009801523739569e0f33cfc3.jpg"),
        MenuItem(name="Salted Caramel Macchiato", price=1.20, category="Coffee", stock_quantity=90, image_url="https://i.pinimg.com/564x/d2/0c/e6/d20ce6b882f53f35c58738dab963434b.jpg"),
        MenuItem(name="Espresso", price=1.50, category="Coffee", stock_quantity=80, image_url="https://i.pinimg.com/564x/07/b7/e9/07b7e99bb01cca8732387d18919b2b4e.jpg"),
        MenuItem(name="Doppio", price=2.00, category="Coffee", stock_quantity=60, image_url="https://i.pinimg.com/564x/bf/41/7a/bf417a0b8d7f6044ab535cb4edb5d22b.jpg"),
        MenuItem(name="Latte", price=1.75, category="Coffee", stock_quantity=70, image_url="https://i.pinimg.com/564x/6a/86/c3/6a86c387495a30851e5843a582c7b6f2.jpg"),
        MenuItem(name="Mocha", price=3.00, category="Coffee", stock_quantity=50, image_url="https://i.pinimg.com/736x/20/f3/e0/20f3e0b60d361521322d7fad39db9c9d.jpg")
    ]

    pastries = [
        MenuItem(name="Pancakes", price=0.60, category="Pastries", stock_quantity=200, image_url="https://i.pinimg.com/564x/9b/2e/4f/9b2e4f6e5477b625e203dd34e95dadd0.jpg"),
        MenuItem(name="", price=0.70, category="Pastries", stock_quantity=180, image_url="https://i.pinimg.com/564x/cd/13/b9/cd13b98dfb9527f0d85b206fbbaebe28.jpg"),
        MenuItem(name="", price=1.10, category="Pastries", stock_quantity=150, image_url="https://i.pinimg.com/564x/49/a0/21/49a021b279e14539d69c9c2dfa19035b.jpg"),
        MenuItem(name="", price=1.20, category="Pastries", stock_quantity=130, image_url="https://i.pinimg.com/564x/0b/83/8d/0b838d8e0bde5a8e949ec17649142499.jpg"),
        MenuItem(name="", price=2.50, category="Pastries", stock_quantity=100, image_url="https://i.pinimg.com/564x/ad/bd/87/adbd87796b9fa15bd7d8dfa4c83c7385.jpg"),
        MenuItem(name="", price=0.80, category="Pastries", stock_quantity=170, image_url="https://i.pinimg.com/564x/c9/28/83/c92883a1c96a404ae49afc471e083f80.jpg"),
        MenuItem(name="", price=1.00, category="Pastries", stock_quantity=160, image_url="https://i.pinimg.com/564x/49/ac/c4/49acc4f709c9859dff7a7b7b0c054285.jpg"),
        MenuItem(name="", price=1.30, category="Pastries", stock_quantity=140, image_url="https://i.pinimg.com/564x/3a/f5/ed/3af5edcd35c2f0d06e03e8e68bf30310.jpg")
    ]

    sandwiches = [
        MenuItem(name="Carrot", price=0.40, category="Sandwiches", stock_quantity=200, image_url="https://i.pinimg.com/564x/ba/05/18/ba05185d357cd59a97110b9a8a57fc31.jpg", description="Fresh carrots"),
        MenuItem(name="Broccoli", price=0.90, category="Sandwiches", stock_quantity=150, image_url="https://i.pinimg.com/564x/29/b3/cb/29b3cbe08421127f03eb643250590c00.jpg", description="Organic broccoli"),
        MenuItem(name="Spinach", price=1.00, category="Sandwiches", stock_quantity=180, image_url="https://i.pinimg.com/564x/28/28/d4/2828d4a7304777d3b25cf982574f7c2e.jpg", description="Fresh spinach"),
        MenuItem(name="Potato", price=0.50, category="Sandwiches", stock_quantity=300, image_url="https://i.pinimg.com/564x/1f/32/99/1f3299b83c835c86e5e85ea9d0e4c7cd.jpg", description="Versatile kestral potatoes"),
        MenuItem(name="Tomato", price=0.70, category="Sandwiches", stock_quantity=220, image_url="https://i.pinimg.com/564x/79/7e/96/797e9652123593bd04cc0b1970403132.jpg", description="Juicy organic tomatoes"),
        MenuItem(name="Cucumber", price=0.60, category="Sandwiches", stock_quantity=170, image_url="https://i.pinimg.com/564x/12/bf/f2/12bff2e7ee771ac03adcbe64359ad718.jpg", description="Crisp cucumbers"),
        MenuItem(name="Bell Pepper", price=0.80, category="Sandwiches", stock_quantity=160, image_url="https://i.pinimg.com/564x/bd/15/f5/bd15f5863856d1c12cf840f788fd7af4.jpg", description="Sweet bell peppers"),
        MenuItem(name="Onion", price=0.30, category="Sandwiches", stock_quantity=250, image_url="https://i.pinimg.com/564x/8d/ed/fe/8dedfe5bfb6c6062625cef825b30d14c.jpg", description="Red onions")
    ]

    orders = [
        Order(user=user1, order_date=date.today(), total_price=30.00),
        Order(user=user2, order_date=date.today(), total_price=50.00),
        Order(user=user1, order_date=date.today(), total_price=25.00),
        Order(user=user2, order_date=date.today(), total_price=40.00)
    ]

    print("Adding data to the database...")
    db.session.add_all(users)
    db.session.add_all(coffee)
    db.session.add_all(pastries)
    db.session.add_all(sandwiches)
    db.session.add_all(orders)
    db.session.commit()
    print("Database seeding complete.")
