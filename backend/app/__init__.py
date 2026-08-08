from flask import Flask, jsonify
from flask_cors import CORS
from datetime import timedelta
from werkzeug.exceptions import RequestEntityTooLarge
from .config import Config
from .models import db
from .utils.csrf import csrf_protect


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    if Config.ENV == 'production' and not Config.SECRET_KEY:
        raise RuntimeError(
            '生产环境必须设置 SECRET_KEY 环境变量（使用强随机值，如 python -c '
            '"import secrets; print(secrets.token_hex(32))"），拒绝启动。'
        )

    app.config['SECRET_KEY'] = Config.SECRET_KEY
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=15)
    app.config['SESSION_COOKIE_HTTPONLY'] = Config.SESSION_COOKIE_HTTPONLY
    app.config['SESSION_COOKIE_SAMESITE'] = Config.SESSION_COOKIE_SAMESITE
    app.config['SESSION_COOKIE_SECURE'] = Config.SESSION_COOKIE_SECURE

    CORS(
        app,
        resources={r'/api/*': {'origins': Config.ALLOWED_ORIGINS}},
        supports_credentials=True,
    )
    db.init_app(app)

    @app.errorhandler(RequestEntityTooLarge)
    def handle_large_upload(e):
        return jsonify({'code': 1, 'message': '图片超过 16MB 大小限制'}), 413

    from .api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    from .auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    # CSRF：所有 /api 下的非安全方法请求都必须携带有效 token
    app.before_request(csrf_protect)

    with app.app_context():
        db.create_all()

    return app
