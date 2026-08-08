import os

basedir = os.path.abspath(os.path.dirname(__file__))

ENV = os.environ.get('FLASK_ENV', 'development')


class Config:
    ENV = ENV
    # 生产环境必须通过环境变量 SECRET_KEY 提供强随机密钥（create_app 会校验）
    SECRET_KEY = os.environ.get(
        'SECRET_KEY', '' if ENV == 'production' else 'dev-secret-change-in-production'
    )
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'mysql+pymysql://love:love123@localhost:3306/love_web?charset=utf8mb4'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.environ.get(
        'UPLOAD_FOLDER',
        '/var/www/love_web/uploads'
    )
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload
    # CORS 允许来源（开发跨源用 localhost:3000，生产同源代理不受影响；
    # 部署时如确需跨源，通过环境变量 ALLOWED_ORIGINS=逗号分隔 覆盖）
    ALLOWED_ORIGINS = [
        o.strip()
        for o in os.environ.get(
            'ALLOWED_ORIGINS', 'http://localhost:3000,http://127.0.0.1:3000'
        ).split(',')
        if o.strip()
    ]
    # 会话 Cookie 加固
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = ENV == 'production'
