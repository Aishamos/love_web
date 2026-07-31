import os
import uuid
from flask import request, jsonify
from werkzeug.utils import secure_filename
from . import api_bp
from ..auth import login_required
from ..models import db
from ..models.photo import Photo
from ..utils.image import create_thumbnail

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@api_bp.route('/upload', methods=['POST'])
@login_required
def upload_photos():
    files = request.files.getlist('files')
    season = request.form.get('season', '')
    region = request.form.get('region', '')
    photo_date = request.form.get('photoDate', '')
    album_id = request.form.get('albumId')

    if not files or len(files) == 0:
        return jsonify({'code': 1, 'message': '请选择图片'}), 400

    upload_dir = '/var/www/love_web/uploads'
    os.makedirs(upload_dir, exist_ok=True)

    results = []

    for file in files:
        if not file.filename or not allowed_file(file.filename):
            continue

        ext = file.filename.rsplit('.', 1)[1].lower()
        unique_name = f"{uuid.uuid4().hex}.{ext}"

        # 保存原图
        src_path = os.path.join(upload_dir, unique_name)
        file.save(src_path)

        # 生成缩略图
        thumb_name = f"thumb_{unique_name}"
        thumb_path = os.path.join(upload_dir, thumb_name)
        w, h = create_thumbnail(src_path, thumb_path)

        # 写入数据库
        photo = Photo(
            filename=unique_name,
            width=w,
            height=h,
            season=season,
            region=region,
            photo_date=photo_date,
            album_id=int(album_id) if album_id else None,
        )
        db.session.add(photo)
        results.append(photo)

    db.session.commit()

    return jsonify({
        'code': 0,
        'message': f'成功上传 {len(results)} 张图片',
        'data': [p.to_dict() for p in results],
    })
