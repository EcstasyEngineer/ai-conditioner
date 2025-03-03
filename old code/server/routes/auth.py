from flask import Blueprint, request, jsonify, session
from models import db, User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    is_super_req = data.get("superuser", False)

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        # Logged in
        session["user_id"] = user.user_id
        session["is_superuser"] = user.is_superuser
        if is_super_req and not user.is_superuser:
            return jsonify({"error": "Not authorized as super user", "redirect": "/contact"}), 403
        return jsonify({"success": True})
    return jsonify({"error": "Invalid credentials"}), 401

@auth_bp.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return jsonify({"success": True})
