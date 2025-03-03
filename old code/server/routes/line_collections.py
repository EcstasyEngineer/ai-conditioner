from flask import Blueprint, jsonify, request, session
from models import db, LineCollection

lines_bp = Blueprint("lines", __name__)

@lines_bp.route("/linecollections/<int:collection_id>", methods=["GET"])
def get_collection(collection_id):
    if not session.get("is_superuser"):
        return jsonify({"error": "Forbidden"}), 403
    coll = LineCollection.query.get(collection_id)
    if not coll:
        return jsonify({"error": "Not found"}), 404
    return jsonify({"title": coll.title, "description": coll.description, "lines": coll.lines})

@lines_bp.route("/linecollections/<int:collection_id>", methods=["PUT"])
def update_collection(collection_id):
    if not session.get("is_superuser"):
        return jsonify({"error": "Forbidden"}), 403
    coll = LineCollection.query.get(collection_id)
    if not coll:
        return jsonify({"error": "Not found"}), 404
    data = request.get_json()
    coll.title = data.get("title", coll.title)
    coll.description = data.get("description", coll.description)
    coll.lines = data.get("lines", coll.lines)
    db.session.commit()
    return jsonify({"success": True})

@lines_bp.route("/linecollections/generate", methods=["POST"])
def generate_lines():
    if not session.get("is_superuser"):
        return jsonify({"error": "Forbidden"}), 403
    # Future implementation for auto line generation
    return jsonify({"success": True, "lines": []})
