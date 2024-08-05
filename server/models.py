from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates, relationship
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime

# Metadata with naming convention for foreign keys
metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)


# User model
class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='customer')
    phone_number = db.Column(db.String(15), nullable=True) 

    # Adding relationship
    orders = db.relationship('Order', back_populates='user')

    # Adding serialization rules
    serialize_rules = ('-orders.user',)

    @validates('email')
    def validate_email(self, key, value):
        if '@' not in value:
            raise ValueError("Failed simple email validation")
        return value

    @validates('phone_number')
    def validate_phone_number(self, key, value):
        if value and (len(value) < 10 or len(value) > 15):
            raise ValueError("Phone number must be between 10 and 15 characters")
        return value

    def __repr__(self):
        return f'<User id={self.id} name={self.name} email={self.email} role={self.role}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'phone_number': self.phone_number  
        }

# MenuItem model
class MenuItem(db.Model, SerializerMixin):
    __tablename__ = 'menu_items'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(150), nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(200), nullable=True)
    description = db.Column(db.Text, nullable=True)

    # Adding relationship
    order_items = db.relationship('OrderItem', back_populates='menu_item')

    # Adding serialization rules
    serialize_rules = ('-order_items.menu_item',)

    def __repr__(self):
        return f'<MenuItem id={self.id} name={self.name} category={self.category} price={self.price}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'category': self.category,
            'stock_quantity': self.stock_quantity,
            'image_url': self.image_url,
            'description': self.description
        }

# Order model
class Order(db.Model, SerializerMixin):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    total_price = db.Column(db.Float, nullable=False)

    # Adding relationships
    order_items = db.relationship('OrderItem', back_populates='order')
    user = db.relationship('User', back_populates='orders')

    # Adding serialization rules (also add -password in the serialization rules)
    serialize_rules = ('-order_items.order', '-user.orders')

    def __repr__(self):
        return f'<Order id={self.id} user_id={self.user_id} order_date={self.order_date} total_price={self.total_price}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'order_date': self.order_date,
            'total_price': self.total_price,
            'order_items': [item.to_dict() for item in self.order_items]
        }

# Association table for Order-MenuItem Many-to-Many relationship
class OrderItem(db.Model, SerializerMixin):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_items.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    # Adding relationships
    menu_item = relationship('MenuItem', back_populates='order_items')
    order = relationship('Order', back_populates='order_items')

    # Adding serialization rules
    serialize_rules = ('-menu_item.order_items', '-order.order_items')

    def __repr__(self):
        return f'<OrderItem order_id={self.order_id} menu_item_id={self.menu_item_id} quantity={self.quantity}>'

    def to_dict(self):
        return {
            'order_id': self.order_id,
            'menu_item_id': self.menu_item_id,
            'quantity': self.quantity,
            'menu_item': self.menu_item.to_dict(),  # Include menu item details for convenience
        }
