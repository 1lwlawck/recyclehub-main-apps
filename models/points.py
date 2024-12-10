from app import db
from datetime import datetime


class Points(db.Model):
    __tablename__ = 'points'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    points = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relasi ke model User
    user = db.relationship('User', backref=db.backref('points', lazy=True))

    def __repr__(self):
        return f'<Points {self.points} for user {self.user_id}>'
