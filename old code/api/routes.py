import os
from flask import Blueprint, current_app, send_from_directory, request, jsonify
from ..database.database import get_session
from ..database.models import User, Line, Template, Theme
import uuid
from .generate_session import generate_session

api_bp = Blueprint('api', __name__)

@api_bp.route('/audio/<filename>')
def serve_audio(filename):
    audio_dir = os.path.join(current_app.root_path, '../data/audio')
    return send_from_directory(audio_dir, filename)

@api_bp.route('/api/generate_session', methods=['POST'])
def generate_session_route():
    return generate_session()

@api_bp.route('/api/test', methods=['GET'])
def test():
    response = {
        'status': 'Test successful.'
    }

    return jsonify(response)