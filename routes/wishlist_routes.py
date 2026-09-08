from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions import db
from models.wishlist import Wishlist
from models.product import Product


wishlist_bp = Blueprint("wishlist", __name__)


@wishlist_bp.route("/wishlist", methods=["POST"])
@jwt_required()
def add_to_wishlist():

    user_id = get_jwt_identity()
    data = request.get_json()

    product_id = data.get("product_id")

    if not product_id:
        return jsonify({
            "message": "Product ID is required"
        }), 400

    product = Product.query.get(product_id)

    if not product:
        return jsonify({
            "message": "Product not found"
        }), 404

    existing_item = Wishlist.query.filter_by(
        user_id=user_id,
        product_id=product_id
    ).first()

    if existing_item:
        return jsonify({
            "message": "Product already exists in wishlist"
        }), 409

    wishlist_item = Wishlist(
        user_id=user_id,
        product_id=product_id
    )

    db.session.add(wishlist_item)
    db.session.commit()

    return jsonify({
        "message": "Product added to wishlist successfully"
    }), 201


@wishlist_bp.route("/wishlist", methods=["GET"])
@jwt_required()
def get_wishlist():

    user_id = get_jwt_identity()

    wishlist_items = Wishlist.query.filter_by(
        user_id=user_id
    ).all()

    wishlist = []

    for item in wishlist_items:

        product = Product.query.get(item.product_id)

        if product:
            wishlist.append({
                "id": item.id,
                "product_id": product.id,
                "product_name": product.name,
                "price": product.price,
                "stock": product.stock
            })

    return jsonify(wishlist), 200


@wishlist_bp.route("/wishlist/<int:item_id>", methods=["DELETE"])
@jwt_required()
def remove_from_wishlist(item_id):

    user_id = get_jwt_identity()

    item = Wishlist.query.filter_by(
        id=item_id,
        user_id=user_id
    ).first()

    if not item:
        return jsonify({
            "message": "Wishlist item not found"
        }), 404

    db.session.delete(item)
    db.session.commit()

    return jsonify({
        "message": "Product removed from wishlist"
    }), 200