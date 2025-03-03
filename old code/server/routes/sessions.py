from flask import Blueprint, jsonify, request, session
from models import db, UserSession

sessions_bp = Blueprint("sessions", __name__)

@sessions_bp.route("/sessions/default", methods=["GET"])
def default_sessions():
    # Return hardcoded or pre-defined sessions
    default_data = [
        {"session_id": 1, "title": "Basic Relaxation", "duration_min":5, "duration_max":10, "themes":["Relaxation"]},
        # ...
    ]
    return jsonify(default_data)

@sessions_bp.route("/sessions/my", methods=["GET"])
def my_sessions():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    user_sess = UserSession.query.filter_by(user_id=user_id).all()
    data = []
    for s in user_sess:
        data.append({"session_id": s.session_id, "title": s.title, "metadata": s.metadata})
    return jsonify(data)

@sessions_bp.route("/sessions", methods=["POST"])
def create_session():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401
    data = request.get_json()
    new_sess = UserSession(user_id=user_id, title=data.get("title"), metadata=data.get("metadata", {}))
    db.session.add(new_sess)
    db.session.commit()
    return jsonify({"success": True, "session_id": new_sess.session_id})

@sessions_bp.route("/sessions/<int:session_id>", methods=["PUT"])
def update_session(session_id):
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401
    sess = UserSession.query.get(session_id)
    if not sess or sess.user_id != user_id:
        return jsonify({"error": "Not found or not authorized"}), 404
    data = request.get_json()
    sess.title = data.get("title", sess.title)
    sess.metadata = data.get("metadata", sess.metadata)
    db.session.commit()
    return jsonify({"success": True})

@sessions_bp.route("/sessions/<int:session_id>", methods=["DELETE"])
def delete_session(session_id):
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401
    sess = UserSession.query.get(session_id)
    if not sess or sess.user_id != user_id:
        return jsonify({"error": "Not found or not authorized"}), 404
    db.session.delete(sess)
    db.session.commit()
    return jsonify({"success": True})
