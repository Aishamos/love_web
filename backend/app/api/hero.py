import os
from flask import jsonify, current_app
from sqlalchemy import func
from . import api_bp
from ..models.photo import Photo


@api_bp.route('/hero')
def get_hero():
    photo = Photo.query.order_by(func.rand()).first()
    if photo:
        # 优先用中等尺寸图（新照片），老照片没有该文件则回退原图
        medium = f"medium_{photo.filename}"
        if os.path.exists(os.path.join(current_app.config['UPLOAD_FOLDER'], medium)):
            image_url = f'/static/uploads/{medium}'
        else:
            image_url = f'/static/uploads/{photo.filename}'
        return jsonify({
            'code': 0,
            'message': 'ok',
            'data': {
                'imageUrl': image_url,
                'title': photo.region or '',
                'subtitle': photo.photo_date or '',
                'photo': photo.to_dict(),
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
