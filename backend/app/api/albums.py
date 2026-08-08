from flask import jsonify
from . import api_bp
from ..models.album import Album


@api_bp.route('/albums')
def get_albums():
    albums = Album.query.order_by(Album.created_at.desc()).all()
    return jsonify({
        'code': 0,
        'message': 'ok',
        'data': [a.to_dict() for a in albums]
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
