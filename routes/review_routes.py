from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions import db
from models.review import Review
from models.product import Product


review_bp = Blueprint("review", __name__)


@review_bp.route("/products/<int:product_id>/reviews", methods=["POST"])
@jwt_required()
def create_review(product_id):

    user_id = get_jwt_identity()
    data = request.get_json()

    rating = data.get("rating")
    comment = data.get("comment")

    if rating is None or not comment:
        return jsonify({
            "message": "Rating and comment are required"
        }), 400

    try:
        rating = int(rating)
    except (ValueError, TypeError):
        return jsonify({
            "message": "Rating must be an integer"
        }), 400

    if rating < 1 or rating > 5:
        return jsonify({
            "message": "Rating must be between 1 and 5"
        }), 400

    product = Product.query.get(product_id)

    if not product:
        return jsonify({
            "message": "Product not found"
        }), 404

    existing_review = Review.query.filter_by(
        user_id=user_id,
        product_id=product_id
    ).first()

    if existing_review:
        return jsonify({
            "message": "You have already reviewed this product"
        }), 409

    review = Review(
        user_id=user_id,
        product_id=product_id,
        rating=rating,
        comment=comment
    )

    db.session.add(review)
    db.session.commit()

    return jsonify({
        "message": "Review added successfully",
        "review": {
            "id": review.id,
            "product_id": review.product_id,
            "rating": review.rating,
            "comment": review.comment
        }
    }), 201


@review_bp.route("/products/<int:product_id>/reviews", methods=["GET"])
def get_reviews(product_id):

    product = Product.query.get(product_id)

    if not product:
        return jsonify({
            "message": "Product not found"
        }), 404

    reviews = Review.query.filter_by(
        product_id=product_id
    ).all()

    return jsonify([
        {
            "id": review.id,
            "user_id": review.user_id,
            "rating": review.rating,
            "comment": review.comment
        }
        for review in reviews
    ]), 200


@review_bp.route("/reviews/<int:review_id>", methods=["PUT"])
@jwt_required()
def update_review(review_id):

    user_id = get_jwt_identity()

    review = Review.query.filter_by(
        id=review_id,
        user_id=user_id
    ).first()

    if not review:
        return jsonify({
            "message": "Review not found"
        }), 404

    data = request.get_json()

    if "rating" in data:
        try:
            rating = int(data["rating"])
        except (ValueError, TypeError):
            return jsonify({
                "message": "Rating must be an integer"
            }), 400

        if rating < 1 or rating > 5:
            return jsonify({
                "message": "Rating must be between 1 and 5"
            }), 400

        review.rating = rating

    if "comment" in data:
        if not data["comment"]:
            return jsonify({
                "message": "Comment cannot be empty"
            }), 400

        review.comment = data["comment"]

    db.session.commit()

    return jsonify({
        "message": "Review updated successfully"
    }), 200


@review_bp.route("/reviews/<int:review_id>", methods=["DELETE"])
@jwt_required()
def delete_review(review_id):

    user_id = get_jwt_identity()

    review = Review.query.filter_by(
        id=review_id,
        user_id=user_id
    ).first()

    if not review:
        return jsonify({
            "message": "Review not found"
        }), 404

    db.session.delete(review)
    db.session.commit()

    return jsonify({
        "message": "Review deleted successfully"
    }), 200