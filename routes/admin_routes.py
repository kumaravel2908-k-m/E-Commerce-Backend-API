from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions import db
from models.user import User


admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin", methods=["GET"])
@jwt_required()
def admin_only():

    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    if user.role != "admin":
        return jsonify({"message": "Admin access required"}), 403

    return jsonify({
        "message": "Welcome Admin",
        "user_id": user.id,
        "role": user.role
    }), 200

