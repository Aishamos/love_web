from functools import wraps
from flask import session, jsonify, request, Blueprint
from .models.user import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username', '')
    password = data.get('password', '')

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        session['authenticated'] = True
        session.permanent = True
        return jsonify({'code': 0, 'message': 'ok'})
    return jsonify({'code': 1, 'message': '用户名或密码错误'}), 401


@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('authenticated', None)
    return jsonify({'code': 0, 'message': 'ok'})


@auth_bp.route('/check')
def check_auth():
    if session.get('authenticated'):
        return jsonify({'code': 0, 'message': 'ok'})
    return jsonify({'code': 1, 'message': '未登录'}), 401


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('authenticated'):
            return jsonify({'code': 1, 'message': '请先登录'}), 401
        return f(*args, **kwargs)
    return decorated
