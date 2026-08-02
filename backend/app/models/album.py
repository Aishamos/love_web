from ..utils.time import now_local
from . import db


class Album(db.Model):
    __tablename__ = 'albums'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), default='')
    cover_filename = db.Column(db.String(255), default='')
    created_at = db.Column(db.DateTime, default=now_local)

    photos = db.relationship('Photo', back_populates='album', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'coverUrl': f'/static/uploads/{self.cover_filename}' if self.cover_filename else '',
            'photoCount': self.photos.count(),
        }
