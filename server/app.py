import os
from datetime import date
from flask import Flask, request, make_response, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_migrate import Migrate
from flask_cors import CORS
from functools import wraps
from models import db, User, MenuItem, Order

# Initialize Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URI", "sqlite:///cafe.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get("JWT_SECRET_KEY", "super-secret")
app.json.compact = False

# Initialize extensions
CORS(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)
db.init_app(app)

# Decorator for Admin Access
def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user is None:
            return jsonify({"error": "User not found"}), 404
        if user.role != 'admin':
            return jsonify({"error": "Admin access required"}), 403
        return fn(*args, **kwargs)
    return wrapper

@app.route("/")
def index():
    return "<h1>Welcome to the Cafe</h1>"

@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    existing_user = User.query.filter_by(email=data["email"]).first()
    if existing_user:
        return make_response(jsonify(error="Email already exists"), 422)

    hashed_password = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
    new_user = User(
        name=data["name"],
        email=data["email"],
        password=hashed_password,
        role=data.get("role", "customer"),
        phone_number=data["phone_number"]
    )
    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=new_user.id)
    return make_response(jsonify(new_user_id=new_user.id, access_token=access_token), 201)

@app.route("/users", methods=["GET"])
@admin_required
def get_all_users():
    try:
        users = User.query.all()
        return make_response(
            jsonify([{
                "user_id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role,
                "phone_number": user.phone_number
            } for user in users]), 200
        )
    except Exception as e:
        return make_response(jsonify({"error": "Internal Server Error"}), 500)

@app.route("/users/<int:user_id>", methods=["PUT"])
@admin_required
def update_user(user_id):
    data = request.get_json()
    user = User.query.get_or_404(user_id)

    if user.email != data["email"]:
        existing_user = User.query.filter_by(email=data["email"]).first()
        if existing_user:
            return make_response(jsonify(error="Email already exists"), 422)

    user.name = data["name"]
    user.email = data["email"]
    if "password" in data:
        user.password = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
    user.role = data.get("role", user.role)
    db.session.commit()
    return make_response(jsonify(message="User updated successfully"), 200)

@app.route("/users/<int:user_id>", methods=["GET"])
@admin_required
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return make_response(
        jsonify(
            {
                "user_id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role,
            }
        ),
        200,
    )

@app.route("/users/<int:user_id>", methods=["DELETE"])
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return make_response("", 204)

@app.route("/menu", methods=["POST"])
@admin_required
def create_menu_item():
    data = request.get_json()
    new_item = MenuItem(
        name=data["name"],
        price=data["price"],
        description=data.get("description", ""),
    )
    db.session.add(new_item)
    db.session.commit()
    return make_response(jsonify(new_item_id=new_item.id), 201)

@app.route("/menu", methods=["GET"])
def get_menu():
    try:
        items = MenuItem.query.all()
        return make_response(jsonify([item.to_dict() for item in items]), 200)
    except Exception as e:
        return make_response(jsonify({"error": "Internal Server Error"}), 500)

@app.route("/menu/<int:item_id>", methods=["GET"])
def get_menu_item(item_id):
    item = MenuItem.query.get_or_404(item_id)
    return make_response(jsonify(item.to_dict()), 200)

@app.route("/menu/<int:item_id>", methods=["PUT"])
@admin_required
def update_menu_item(item_id):
    data = request.get_json()
    item = MenuItem.query.get_or_404(item_id)
    item.name = data["name"]
    item.price = data["price"]
    item.description = data.get("description", item.description)
    db.session.commit()
    return make_response(jsonify(message="Menu item updated successfully"), 200)

@app.route("/menu/<int:item_id>", methods=["DELETE"])
@admin_required
def delete_menu_item(item_id):
    item = MenuItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return make_response("", 204)

@app.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json()
    new_order = Order(
        user_id=data["user_id"],
        order_date=date.today(),
        total_price=data["total_price"],
    )
    db.session.add(new_order)
    db.session.commit()
    return make_response(jsonify(new_order_id=new_order.id), 201)

@app.route("/orders/<int:order_id>", methods=["GET"])
@jwt_required()
def get_order(order_id):
    user_id = get_jwt_identity()
    order = Order.query.get_or_404(order_id)
    if order.user_id != user_id:
        return jsonify({"error": "Access denied"}), 403
    return make_response(
        jsonify(
            {
                "order_id": order.id,
                "user_id": order.user_id,
                "order_date": order.order_date.isoformat(),
                "total_price": order.total_price,
            }
        ),
        200,
    )

@app.route("/orders/<int:order_id>", methods=["PUT"])
@admin_required
def update_order(order_id):
    data = request.get_json()
    order = Order.query.get_or_404(order_id)
    order.user_id = data["user_id"]
    order.order_date = data["order_date"]
    order.total_price = data["total_price"]
    db.session.commit()
    return make_response(jsonify(message="Order updated successfully"), 200)

@app.route("/orders/<int:order_id>", methods=["DELETE"])
@jwt_required()
def delete_order(order_id):
    user_id = get_jwt_identity()
    order = Order.query.get_or_404(order_id)
    
    if order.user_id != user_id:
        user = User.query.get(user_id)
        if user.role != 'admin':
            return jsonify({"error": "Access denied"}), 403

    db.session.delete(order)
    db.session.commit()
    return make_response("", 204)

@app.route("/login/email", methods=["POST"])
def login_user_email():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    
    user = User.query.filter_by(email=email).first()
    
    if user and bcrypt.check_password_hash(user.password, password):
        token = create_access_token(identity=user.id)
        return jsonify({"token": token, "role": user.role, "success": True}), 200
    else:
        return jsonify({"error": "Invalid email or password"}), 401

@app.route("/login/phone", methods=["POST"])
def login_user_phone():
    data = request.get_json()
    phone = data.get("phone")
    password = data.get("password")
    
    user = User.query.filter_by(phone_number=phone).first()
    
    if user and bcrypt.check_password_hash(user.password, password):
        token = create_access_token(identity=user.id)
        return jsonify({"token": token, "role": user.role, "success": True}), 200
    else:
        return jsonify({"error": "Invalid phone number or password"}), 401

if __name__ == "__main__":
    app.run(debug=True, port=5000)
