from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions import db
from models.cart import CartItem
from models.product import Product

cart_bp = Blueprint("cart", __name__)


@cart_bp.route("/cart", methods=["POST"])
@jwt_required()
def add_to_cart():

    user_id = get_jwt_identity()
    data = request.get_json()

    product_id = data.get("product_id")
    quantity = data.get("quantity")

    if not product_id or quantity is None:
        return jsonify({
            "message": "Product ID and quantity are required"
        }), 400

    try:
        quantity = int(quantity)
    except (ValueError, TypeError):
        return jsonify({
            "message": "Quantity must be an integer"
        }), 400

    if quantity <= 0:
        return jsonify({
            "message": "Quantity must be greater than 0"
        }), 400

    product = Product.query.get(product_id)

    if not product:
        return jsonify({
            "message": "Product not found"
        }), 404

    if quantity > product.stock:
        return jsonify({
            "message": "Not enough stock available"
        }), 400

    existing_item = CartItem.query.filter_by(
        user_id=user_id,
        product_id=product_id
    ).first()

    if existing_item:

        new_quantity = existing_item.quantity + quantity

        if new_quantity > product.stock:
            return jsonify({
                "message": "Not enough stock available"
            }), 400

        existing_item.quantity = new_quantity

    else:

        cart_item = CartItem(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity
        )

        db.session.add(cart_item)

    db.session.commit()

    return jsonify({
        "message": "Product added to cart successfully"
    }), 201


@cart_bp.route("/cart", methods=["GET"])
@jwt_required()
def get_cart():

    user_id = get_jwt_identity()

    cart_items = CartItem.query.filter_by(
        user_id=user_id
    ).all()

    cart = []

    for item in cart_items:

        product = Product.query.get(item.product_id)

        cart.append({
            "id": item.id,
            "product_id": product.id,
            "product_name": product.name,
            "price": product.price,
            "quantity": item.quantity,
            "total": product.price * item.quantity
        })

    return jsonify(cart), 200


@cart_bp.route("/cart/<int:item_id>", methods=["PUT"])
@jwt_required()
def update_cart(item_id):

    user_id = get_jwt_identity()

    item = CartItem.query.filter_by(
        id=item_id,
        user_id=user_id
    ).first()

    if not item:
        return jsonify({
            "message": "Cart item not found"
        }), 404

    data = request.get_json()
    quantity = data.get("quantity")

    if quantity is None:
        return jsonify({
            "message": "Quantity is required"
        }), 400

    try:
        quantity = int(quantity)
    except (ValueError, TypeError):
        return jsonify({
            "message": "Quantity must be an integer"
        }), 400

    if quantity <= 0:
        return jsonify({
            "message": "Quantity must be greater than 0"
        }), 400

    product = Product.query.get(item.product_id)

    if quantity > product.stock:
        return jsonify({
            "message": "Not enough stock available"
        }), 400

    item.quantity = quantity

    db.session.commit()

    return jsonify({
        "message": "Cart updated successfully"
    }), 200


@cart_bp.route("/cart/<int:item_id>", methods=["DELETE"])
@jwt_required()
def remove_from_cart(item_id):

    user_id = get_jwt_identity()

    item = CartItem.query.filter_by(
        id=item_id,
        user_id=user_id
    ).first()

    if not item:
        return jsonify({
            "message": "Cart item not found"
        }), 404

    db.session.delete(item)
    db.session.commit()

    return jsonify({
        "message": "Product removed from cart"
    }), 200