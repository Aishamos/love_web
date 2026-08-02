from ..utils.time import now_local
from . import db


class Photo(db.Model):
    __tablename__ = 'photos'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    alt = db.Column(db.String(255), default='')
    width = db.Column(db.Integer, default=0)
    height = db.Column(db.Integer, default=0)
    season = db.Column(db.String(20), default='')        # spring/summer/autumn/winter
    region = db.Column(db.String(100), default='')       # 地区，如 Tokyo
    photo_date = db.Column(db.String(20), default='')    # 拍摄时间，如 2025.03
    album_id = db.Column(db.Integer, db.ForeignKey('albums.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=now_local)

    album = db.relationship('Album', back_populates='photos')

    def to_dict(self):
        return {
            'id': self.id,
            'url': f'/static/uploads/{self.filename}',
            'thumbnailUrl': f'/static/uploads/thumb_{self.filename}',
            'alt': self.alt,
            'width': self.width,
            'height': self.height,
            'season': self.season,
            'region': self.region,
            'photoDate': self.photo_date,
            'albumId': self.album_id,
        }
