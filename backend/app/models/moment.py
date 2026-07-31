from . import db


class Moment(db.Model):
    __tablename__ = 'moments'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), default='')
    date_str = db.Column(db.String(20), nullable=False)       # 如 "2025.03"
    photo_count = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'location': self.location,
            'date': self.date_str,
            'photoCount': self.photo_count,
        }
