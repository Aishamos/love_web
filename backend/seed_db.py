"""初始化数据库种子数据（示例相册；会清空照片与相册表，需显式确认）"""
import os
import sys

from app import create_app
from app.models import db


def main():
    confirmed = '--yes' in sys.argv or os.environ.get('SEED_CONFIRM') == '1'
    if not confirmed:
        print('⚠️  本脚本会清空 photos / albums 表并重建示例相册！')
        print('确认执行请使用: python seed_db.py --yes  （或设置环境变量 SEED_CONFIRM=1）')
        sys.exit(1)

    app = create_app()

    with app.app_context():
        from app.models.album import Album
        from app.models.photo import Photo

        Photo.query.delete()
        Album.query.delete()

        albums = [
            Album(title='Japan', description='Tokyo · 2025.03'),
            Album(title='Daily', description='日常记录'),
            Album(title='Travel', description='旅行照片'),
        ]
        db.session.add_all(albums)
        db.session.commit()

        print('数据库种子数据已创建：')
        print(f'  Albums: {len(albums)}')


if __name__ == '__main__':
    main()
