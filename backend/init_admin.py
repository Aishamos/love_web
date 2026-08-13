"""初始化或重置管理员账号密码（不删除照片与相册数据）"""
import os
import secrets
import sys

from app import create_app
from app.models import db
from app.models.user import User


def main():
    confirmed = '--yes' in sys.argv or os.environ.get('SEED_CONFIRM') == '1'
    if not confirmed:
        print('本脚本会创建或重置管理员账号密码，不影响照片与相册数据。')
        print('确认执行请使用: python init_admin.py --yes  （或设置环境变量 SEED_CONFIRM=1）')
        sys.exit(1)

    app = create_app()

    with app.app_context():
        username = os.environ.get('ADMIN_USERNAME', '0609')
        password = os.environ.get('ADMIN_PASSWORD') or secrets.token_urlsafe(12)

        admin = User.query.filter_by(username=username).first()
        if admin is None:
            admin = User(username=username, is_admin=True)
            db.session.add(admin)
        admin.set_password(password)
        db.session.commit()

        print('管理员账号已就绪：')
        print(f'  Admin user: {username} / {password}')
        if not os.environ.get('ADMIN_PASSWORD'):
            print('  （密码为随机生成，请立即保存；如需固定请设置环境变量 ADMIN_PASSWORD）')


if __name__ == '__main__':
    main()
