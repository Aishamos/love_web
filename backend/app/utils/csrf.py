import secrets

from flask import jsonify, request, session


def ensure_csrf_token():
    """确保当前会话存在 CSRF token，并返回。"""
    token = session.get('csrf_token')
    if not token:
        token = secrets.token_hex(32)
        session['csrf_token'] = token
    return token


def csrf_protect():
    """before_request 钩子：拦截 /api 下的写请求，校验 X-CSRF-Token。"""
    if not request.path.startswith('/api/'):
        return None
    if request.method in ('GET', 'HEAD', 'OPTIONS', 'TRACE'):
        return None

    expected = session.get('csrf_token')
    actual = request.headers.get('X-CSRF-Token')
    if not expected or not actual or not secrets.compare_digest(expected, actual):
        return jsonify({'code': 1, 'message': 'CSRF 校验失败，请刷新页面后重试'}), 403
    return None
