from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

protected_bp = Blueprint("protected", __name__)


@protected_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    user_id = get_jwt_identity()

    return jsonify({
        "message": "Access granted",
        "user_id": user_id
    }), 200