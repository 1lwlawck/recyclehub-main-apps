from app import db
from datetime import datetime
from slugify import slugify

class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(255), unique=True, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    profile_picture = db.Column(db.String(300), nullable=True)
    role = db.Column(db.String(100), nullable=True)
    content = db.Column(db.Text, nullable=False)
    featured_image = db.Column(db.String(300), nullable=True)
    published_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Article {self.title}>'
