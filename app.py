from flask import Flask
from flask_jwt_extended import JWTManager

from config import Config
from extensions import db
from routes.auth_routes import auth_bp
from routes.protected_routes import protected_bp
from routes.admin_routes import admin_bp
from routes.category_routes import category_bp
from routes.product_routes import product_bp
from routes.cart_routes import cart_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    JWTManager(app)

    from models.user import User
    from models.category import Category
    from models.product import Product
    from models.cart import CartItem

    with app.app_context():
        db.create_all()

    app.register_blueprint(auth_bp)
    app.register_blueprint(protected_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(cart_bp)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)