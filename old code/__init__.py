from flask import Flask
from .api.routes import api_bp

def create_app():
    app = Flask(__name__)

    # Register API blueprint
    app.register_blueprint(api_bp)

    return app
