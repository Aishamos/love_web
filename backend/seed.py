"""初始化数据库种子数据（危险操作，需显式确认）"""
import os
import secrets
import sys

from app import create_app
from app.models import db


def main():
    confirmed = '--yes' in sys.argv or os.environ.get('SEED_CONFIRM') == '1'
    if not confirmed:
        print('⚠️  本脚本会清空 photos / albums / users 表并重建种子数据！')
        print('确认执行请使用: python seed.py --yes  （或设置环境变量 SEED_CONFIRM=1）')
        sys.exit(1)

    app = create_app()

    with app.app_context():
        # 清除已有数据
        from app.models.album import Album
        from app.models.photo import Photo
        from app.models.user import User

        Photo.query.delete()
        Album.query.delete()
        User.query.delete()

        # 创建相册
        albums = [
            Album(title='Japan', description='Tokyo · 2025.03'),
            Album(title='Daily', description='日常记录'),
            Album(title='Travel', description='旅行照片'),
        ]
        db.session.add_all(albums)
        db.session.flush()

        # 管理员账号：用户名/密码均从环境变量读取；未提供密码时随机生成
        admin_username = os.environ.get('ADMIN_USERNAME', '0609')
        admin_password = os.environ.get('ADMIN_PASSWORD') or secrets.token_urlsafe(12)

        admin = User(username=admin_username, is_admin=True)
        admin.set_password(admin_password)
        db.session.add(admin)

        db.session.commit()

        print('Seed data created:')
        print(f'  Albums: {len(albums)}')
        print(f'  Admin user: {admin_username} / {admin_password}')
        if not os.environ.get('ADMIN_PASSWORD'):
            print('  （密码为随机生成，请立即保存；如需固定请设置环境变量 ADMIN_PASSWORD）')


if __name__ == '__main__':
    main()
