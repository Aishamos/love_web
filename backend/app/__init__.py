from flask import Flask, jsonify
from flask_cors import CORS
from datetime import timedelta
from werkzeug.exceptions import RequestEntityTooLarge
from .config import Config
from .models import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['SECRET_KEY'] = Config.SECRET_KEY
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=15)

    CORS(app, supports_credentials=True)
    db.init_app(app)

    @app.errorhandler(RequestEntityTooLarge)
    def handle_large_upload(e):
        return jsonify({'code': 1, 'message': '图片超过 16MB 大小限制'}), 413

    from .api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    from .auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    with app.app_context():
        db.create_all()

    return app
