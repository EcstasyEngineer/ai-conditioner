from flask import Flask
from flask_cors import CORS
from models import db
from routes.auth import auth_bp
from routes.sessions import sessions_bp
from routes.line_collections import lines_bp

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SECRET_KEY"] = "yoursecret"
    db.init_app(app)
    with app.app_context():
        db.create_all()
    CORS(app)

    app.register_blueprint(auth_bp, url_prefix="/api")
    app.register_blueprint(sessions_bp, url_prefix="/api")
    app.register_blueprint(lines_bp, url_prefix="/api")

    # Static routes for contact page
    @app.route("/contact")
    def contact():
        return "<h1>Contact Us</h1><p>Please contact admin@example.com for access.</p>"

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
