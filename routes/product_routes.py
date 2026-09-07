from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions import db
from models.product import Product
from models.category import Category
from models.user import User

product_bp = Blueprint("product", __name__)


def get_admin_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return None, jsonify({"message": "User not found"}), 404

    if user.role != "admin":
        return None, jsonify({"message": "Admin access required"}), 403

    return user, None, None


@product_bp.route("/products", methods=["POST"])
@jwt_required()
def create_product():

    user, error, status = get_admin_user()

    if error:
        return error, status

    data = request.get_json()

    name = data.get("name")
    description = data.get("description")
    price = data.get("price")
    stock = data.get("stock")
    category_id = data.get("category_id")

    if not name or price is None or stock is None or not category_id:
        return jsonify({
            "message": "Name, price, stock and category_id are required"
        }), 400

    try:
        price = float(price)
        stock = int(stock)
    except (ValueError, TypeError):
        return jsonify({
            "message": "Price must be a number and stock must be an integer"
        }), 400

    if price < 0:
        return jsonify({
            "message": "Price cannot be negative"
        }), 400

    if stock < 0:
        return jsonify({
            "message": "Stock cannot be negative"
        }), 400

    category = Category.query.get(category_id)

    if not category:
        return jsonify({
            "message": "Category not found"
        }), 404

    product = Product(
        name=name,
        description=description,
        price=price,
        stock=stock,
        category_id=category_id
    )

    db.session.add(product)
    db.session.commit()

    return jsonify({
        "message": "Product created successfully",
        "product": {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "stock": product.stock,
            "category_id": product.category_id
        }
    }), 201


@product_bp.route("/products", methods=["GET"])
def get_products():

    search = request.args.get("search")
    category_id = request.args.get("category_id")
    min_price = request.args.get("min_price")
    max_price = request.args.get("max_price")

    query = Product.query

    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))

    if category_id:
        query = query.filter_by(category_id=category_id)

    if min_price:
        query = query.filter(Product.price >= float(min_price))

    if max_price:
        query = query.filter(Product.price <= float(max_price))

    products = query.all()

    return jsonify([
        {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "stock": product.stock,
            "category_id": product.category_id
        }
        for product in products
    ]), 200


@product_bp.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):

    product = Product.query.get(product_id)

    if not product:
        return jsonify({
            "message": "Product not found"
        }), 404

    return jsonify({
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "stock": product.stock,
        "category_id": product.category_id
    }), 200


@product_bp.route("/products/<int:product_id>", methods=["PUT"])
@jwt_required()
def update_product(product_id):

    user, error, status = get_admin_user()

    if error:
        return error, status

    product = Product.query.get(product_id)

    if not product:
        return jsonify({
            "message": "Product not found"
        }), 404

    data = request.get_json()

    product.name = data.get("name", product.name)
    product.description = data.get("description", product.description)

    new_price = data.get("price", product.price)
    new_stock = data.get("stock", product.stock)

    try:
        new_price = float(new_price)
        new_stock = int(new_stock)
    except (ValueError, TypeError):
        return jsonify({
            "message": "Price must be a number and stock must be an integer"
        }), 400

    if new_price < 0:
        return jsonify({
            "message": "Price cannot be negative"
        }), 400

    if new_stock < 0:
        return jsonify({
            "message": "Stock cannot be negative"
        }), 400

    product.price = new_price
    product.stock = new_stock

    if data.get("category_id") is not None:

        category = Category.query.get(data["category_id"])

        if not category:
            return jsonify({
                "message": "Category not found"
            }), 404

        product.category_id = data["category_id"]

    db.session.commit()

    return jsonify({
        "message": "Product updated successfully"
    }), 200


@product_bp.route("/products/<int:product_id>", methods=["DELETE"])
@jwt_required()
def delete_product(product_id):

    user, error, status = get_admin_user()

    if error:
        return error, status

    product = Product.query.get(product_id)

    if not product:
        return jsonify({
            "message": "Product not found"
        }), 404

    db.session.delete(product)
    db.session.commit()

    return jsonify({
        "message": "Product deleted successfully"
    }), 200