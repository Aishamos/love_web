from flask import jsonify
from . import api_bp
from ..models import db
from ..models.photo import Photo


@api_bp.route('/photos')
def get_photos():
    album_id = request_args('albumId', int)
    page = request_args('page', int, 1)
    page_size = request_args('pageSize', int, 20)

    query = Photo.query.order_by(Photo.created_at.desc())
    if album_id:
        query = query.filter_by(album_id=album_id)

    pagination = query.paginate(page=page, per_page=page_size, error_out=False)

    return jsonify({
        'code': 0,
        'message': 'ok',
        'data': {
            'items': [p.to_dict() for p in pagination.items],
            'total': pagination.total,
            'page': page,
            'pageSize': page_size,
            'hasMore': pagination.has_next,
        }
    })


@api_bp.route('/photos/latest')
def get_latest_photos():
    count = request_args('count', int, 12)
    photos = Photo.query.order_by(Photo.created_at.desc()).limit(count).all()
    return jsonify({
        'code': 0,
        'message': 'ok',
        'data': [p.to_dict() for p in photos]
    })


def request_args(key, type_=str, default=None):
    from flask import request
    val = request.args.get(key)
    if val is None:
        return default
    try:
        return type_(val)
    except (ValueError, TypeError):
        return default
