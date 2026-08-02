import os
import uuid
from flask import request, jsonify, current_app
from . import api_bp
from ..auth import login_required
from ..models import db
from ..models.photo import Photo
from ..models.album import Album
from ..utils.image import create_thumbnail

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@api_bp.route('/upload', methods=['POST'])
@login_required
def upload_photos():
    files = request.files.getlist('files')
    remark = request.form.get('remark', '')
    region = request.form.get('region', '')
    photo_date = request.form.get('photoDate', '')
    album_id = request.form.get('albumId')

    if not files or len(files) == 0:
        return jsonify({'code': 1, 'message': '请选择图片'}), 400

    upload_dir = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_dir, exist_ok=True)

    # 相册容错：非数字或不存在则不归入相册
    album_id_int = None
    if album_id:
        try:
            album_id_int = int(album_id)
            if Album.query.get(album_id_int) is None:
                album_id_int = None
        except (TypeError, ValueError):
            album_id_int = None

    results = []

    for file in files:
        if not file.filename or not allowed_file(file.filename):
            continue

        ext = file.filename.rsplit('.', 1)[1].lower()
        unique_name = f"{uuid.uuid4().hex}.{ext}"

        src_path = os.path.join(upload_dir, unique_name)
        thumb_path = os.path.join(upload_dir, f"thumb_{unique_name}")

        try:
            file.save(src_path)
        except Exception:
            if os.path.exists(src_path):
                os.remove(src_path)
            return jsonify({'code': 1, 'message': '保存图片失败，请重试'}), 500

        try:
            w, h = create_thumbnail(src_path, thumb_path)
        except Exception:
            # 缩略图失败（损坏/伪造图片），清理已保存文件避免孤儿
            if os.path.exists(src_path):
                os.remove(src_path)
            if os.path.exists(thumb_path):
                os.remove(thumb_path)
            return jsonify({'code': 1, 'message': '图片文件损坏或无法处理'}), 400

        # Hero 用的中等尺寸图（1600px），失败不影响上传（Hero 会回退原图）
        try:
            create_thumbnail(src_path, os.path.join(upload_dir, f"medium_{unique_name}"), size=(1600, 1600))
        except Exception:
            pass

        photo = Photo(
            filename=unique_name,
            width=w,
            height=h,
            remark=remark,
            region=region,
            photo_date=photo_date,
            album_id=album_id_int,
        )
        db.session.add(photo)
        results.append(photo)

    db.session.commit()

    if not results:
        return jsonify({'code': 1, 'message': '没有可上传的图片'}), 400

    return jsonify({
        'code': 0,
        'message': f'成功上传 {len(results)} 张图片',
        'data': [p.to_dict() for p in results],
    })
