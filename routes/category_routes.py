from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions import db
from models.category import Category
from models.user import User

category_bp = Blueprint("category", __name__)


@category_bp.route("/categories", methods=["POST"])
@jwt_required()
def create_category():

    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    if user.role != "admin":
        return jsonify({"message": "Admin access required"}), 403

    data = request.get_json()

    name = data.get("name")
    description = data.get("description")

    if not name:
        return jsonify({"message": "Category name is required"}), 400

    existing_category = Category.query.filter_by(name=name).first()

    if existing_category:
        return jsonify({"message": "Category already exists"}), 409

    category = Category(
        name=name,
        description=description
    )

    db.session.add(category)
    db.session.commit()

    return jsonify({
        "message": "Category created successfully",
        "category": {
            "id": category.id,
            "name": category.name,
            "description": category.description
        }
    }), 201


@category_bp.route("/categories", methods=["GET"])
def get_categories():

    categories = Category.query.all()

    return jsonify([
        {
            "id": category.id,
            "name": category.name,
            "description": category.description
        }
        for category in categories
    ]), 200