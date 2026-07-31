from flask import jsonify
from . import api_bp
from ..models.photo import Photo


@api_bp.route('/hero')
def get_hero():
    latest = Photo.query.order_by(Photo.created_at.desc()).first()
    if latest:
        return jsonify({
            'code': 0,
            'message': 'ok',
            'data': {
                'imageUrl': f'/static/uploads/{latest.filename}',
                'title': latest.region or 'Gallery',
                'subtitle': latest.photo_date or '',
            }
        })
    return jsonify({
        'code': 0,
        'message': 'ok',
        'data': {
            'imageUrl': 'https://images.unsplash.com/photo-1517841905240-472988babdf9',
            'title': 'Tokyo',
            'subtitle': '2025.03',
        }
    })
