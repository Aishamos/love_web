from flask import jsonify
from sqlalchemy import func
from . import api_bp
from ..models import db
from ..models.album import Album
from ..models.photo import Photo


@api_bp.route('/albums')
def get_albums():
    # 一次 join + count 查出每个相册的照片数，避免 N+1
    rows = (
        db.session.query(Album, func.count(Photo.id))
        .outerjoin(Photo, Photo.album_id == Album.id)
        .group_by(Album.id)
        .order_by(Album.created_at.desc())
        .all()
    )
    return jsonify({
        'code': 0,
        'message': 'ok',
        'data': [album.to_dict(photo_count=count) for album, count in rows]
    })


@api_bp.route('/albums/<int:album_id>')
def get_album(album_id):
    album = Album.query.get(album_id)
    if album is None:
        return jsonify({'code': 1, 'message': '相册不存在'}), 404
    return jsonify({
        'code': 0,
        'message': 'ok',
        'data': album.to_dict()
    })
