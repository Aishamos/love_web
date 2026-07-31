from flask import jsonify
from sqlalchemy import func
from . import api_bp
from ..models.photo import Photo


@api_bp.route('/moments')
def get_moments():
    rows = (
        Photo.query
        .with_entities(
            Photo.region,
            Photo.photo_date,
            func.count(Photo.id).label('cnt')
        )
        .filter(Photo.region != '', Photo.photo_date != '')
        .group_by(Photo.region, Photo.photo_date)
        .order_by(Photo.photo_date.desc())
        .all()
    )

    moments = [
        {
            'id': i + 1,
            'title': row.region,
            'location': row.region,
            'date': row.photo_date,
            'photoCount': row.cnt,
        }
        for i, row in enumerate(rows)
    ]

    return jsonify({
        'code': 0,
        'message': 'ok',
        'data': moments,
    })
