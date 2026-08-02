"""初始化数据库种子数据"""
from app import create_app
from app.models import db

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

    # 创建管理员用户
    admin = User(username='0609', is_admin=True)
    admin.set_password('0609')
    db.session.add(admin)

    db.session.commit()

    print('Seed data created:')
    print(f'  Albums: {len(albums)}')
    print(f'  Admin user: 0609 / 0609')
    print()
    print('Run: pip install pymysql && python seed.py')
