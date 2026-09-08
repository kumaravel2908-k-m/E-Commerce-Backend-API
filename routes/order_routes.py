from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions import db
from models.cart import CartItem
from models.product import Product
from models.order import Order, OrderItem


order_bp = Blueprint("order", __name__)


@order_bp.route("/orders", methods=["POST"])
@jwt_required()
def create_order():

    user_id = get_jwt_identity()

    cart_items = CartItem.query.filter_by(
        user_id=user_id
    ).all()

    if not cart_items:
        return jsonify({
            "message": "Cart is empty"
        }), 400

    total_amount = 0

    for item in cart_items:

        product = Product.query.get(item.product_id)

        if not product:
            return jsonify({
                "message": "Product not found"
            }), 404

        if item.quantity > product.stock:
            return jsonify({
                "message": f"Not enough stock for {product.name}"
            }), 400

        total_amount += product.price * item.quantity

    order = Order(
        user_id=user_id,
        total_amount=total_amount,
        status="Pending"
    )

    db.session.add(order)
    db.session.flush()

    for item in cart_items:

        product = Product.query.get(item.product_id)

        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=item.quantity,
            price=product.price
        )

        db.session.add(order_item)

        product.stock -= item.quantity

    for item in cart_items:
        db.session.delete(item)

    db.session.commit()

    return jsonify({
        "message": "Order placed successfully",
        "order": {
            "id": order.id,
            "total_amount": order.total_amount,
            "status": order.status
        }
    }), 201

@order_bp.route("/orders", methods=["GET"])
@jwt_required()
def get_orders():

    user_id = get_jwt_identity()

    orders = Order.query.filter_by(
        user_id=user_id
    ).all()

    return jsonify([
        {
            "id": order.id,
            "total_amount": order.total_amount,
            "status": order.status
        }
        for order in orders
    ]), 200

@order_bp.route("/orders/<int:order_id>", methods=["GET"])
@jwt_required()
def get_order(order_id):

    user_id = get_jwt_identity()

    order = Order.query.filter_by(
        id=order_id,
        user_id=user_id
    ).first()

    if not order:
        return jsonify({
            "message": "Order not found"
        }), 404

    order_items = OrderItem.query.filter_by(
        order_id=order.id
    ).all()

    items = []

    for item in order_items:

        product = Product.query.get(item.product_id)

        items.append({
            "product_id": item.product_id,
            "product_name": product.name if product else "Product unavailable",
            "quantity": item.quantity,
            "price": item.price,
            "total": item.price * item.quantity
        })

    return jsonify({
        "id": order.id,
        "total_amount": order.total_amount,
        "status": order.status,
        "items": items
    }), 200