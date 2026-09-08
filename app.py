import os

from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from werkzeug.security import generate_password_hash

from config import Config
from extensions import db
from routes.auth_routes import auth_bp
from routes.protected_routes import protected_bp
from routes.admin_routes import admin_bp
from routes.category_routes import category_bp
from routes.product_routes import product_bp
from routes.cart_routes import cart_bp
from routes.order_routes import order_bp
from routes.wishlist_routes import wishlist_bp
from routes.review_routes import review_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    @app.route("/", methods=["GET"])
    def home():
        return jsonify({
            "message": "E-Commerce Backend API is running",
            "status": "success"
        }), 200

    db.init_app(app)
    JWTManager(app)

    from models.user import User
    from models.category import Category
    from models.product import Product
    from models.cart import CartItem
    from models.order import Order, OrderItem
    from models.wishlist import Wishlist
    from models.review import Review

    with app.app_context():
        db.create_all()

        admin_email = os.getenv("ADMIN_EMAIL")
        admin_password = os.getenv("ADMIN_PASSWORD")

        if admin_email and admin_password:
            admin = User.query.filter_by(email=admin_email).first()

            if not admin:
                admin = User(
                    username="admin",
                    email=admin_email,
                    password=generate_password_hash(admin_password),
                    role="admin"
                )

                db.session.add(admin)
                db.session.commit()

    app.register_blueprint(auth_bp)
    app.register_blueprint(protected_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(wishlist_bp)
    app.register_blueprint(review_bp)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "message": "Endpoint not found"
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "message": "Method not allowed"
        }), 405

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)