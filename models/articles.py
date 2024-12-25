from app import db
from datetime import datetime
from slugify import slugify

class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    profile_picture = db.Column(db.String(255), nullable=True)  # Gambar profil penulis
    article_image = db.Column(db.String(255), nullable=True)  # Gambar artikel
    published_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<Article {self.title}>'
