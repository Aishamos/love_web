from ..utils.time import now_local
from . import db


class Todo(db.Model):
    __tablename__ = 'todos'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)
    done = db.Column(db.Boolean, default=False)
    donetime = db.Column(db.DateTime, nullable=True)  # 完成时间
    created_at = db.Column(db.DateTime, default=now_local)

    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'done': self.done,
            'doneTime': self.donetime.isoformat() if self.donetime else None,
        }
