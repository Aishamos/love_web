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
