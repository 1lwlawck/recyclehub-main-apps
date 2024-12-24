from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
from models.articles import Article
from app import db, app
from datetime import datetime
from slugify import slugify
import os

# Konfigurasi folder unggahan
app.config['UPLOAD_FOLDER'] = 'static/uploads/avatar_penulis'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Membuat Blueprint untuk Artikel
article_bp = Blueprint('article', __name__, url_prefix='/articles')


def allowed_file(filename):
    """Periksa apakah file memiliki ekstensi yang diizinkan."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@article_bp.route('/new', methods=['POST'])
def create_article():
    try:
        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')

        # Tangani unggahan file
        file = request.files.get('profile_picture')
        profile_picture_name = None

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)  # Pastikan aman
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            profile_picture_name = filename  # Hanya simpan nama file

        # Buat artikel baru
        slug = slugify(title)
        new_article = Article(
            title=title,
            slug=slug,
            author=author,
            profile_picture=profile_picture_name,
            content=content,
            published_date=datetime.utcnow()
        )
        db.session.add(new_article)
        db.session.commit()

        return jsonify({'message': 'Artikel berhasil ditambahkan!'}), 201
    except Exception as e:
        return jsonify({'message': 'Gagal menambahkan artikel.', 'error': str(e)}), 500


@article_bp.route('/list', methods=['GET'])
def get_articles():
    try:
        articles = Article.query.all()
        articles_data = [
            {
                "id": article.id,
                "title": article.title,
                "author": article.author,
                "content": article.content[:100],  # Cuplikan konten
                "published_date": article.published_date.strftime('%d-%m-%Y'),
                "profile_picture": article.profile_picture or '/static/uploads/avatar_penulis/default-avatar.png'
            }
            for article in articles
        ]
        return jsonify(articles_data), 200
    except Exception as e:
        return jsonify({'message': 'Gagal memuat data artikel.', 'error': str(e)}), 500


@article_bp.route('/delete/<int:article_id>', methods=['DELETE'])
def delete_article(article_id):
    try:
        article = Article.query.get_or_404(article_id)
        if article.profile_picture and os.path.exists(f"static/{article.profile_picture}"):
            os.remove(f"static/{article.profile_picture}")  # Hapus gambar dari folder
        db.session.delete(article)
        db.session.commit()
        return jsonify({'message': 'Artikel berhasil dihapus!'}), 200
    except Exception as e:
        return jsonify({'message': 'Gagal menghapus artikel.', 'error': str(e)}), 500


@article_bp.route('/<slug>')
def view_article(slug):
    try:
        article = Article.query.filter_by(slug=slug).first_or_404()
        return render_template('page/artikel-content-page.html', article=article)
    except Exception as e:
        return jsonify({'message': 'Gagal memuat artikel.', 'error': str(e)}), 500
