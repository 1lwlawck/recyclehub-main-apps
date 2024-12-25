from flask import Blueprint, render_template, request, jsonify
from werkzeug.utils import secure_filename
from models.articles import Article
from app import db, app
from datetime import datetime
from slugify import slugify
import os

# Konfigurasi folder unggahan
app.config['UPLOAD_FOLDER'] = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Blueprint untuk Artikel
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

        # Buat folder jika belum ada
        os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'avatar_penulis'), exist_ok=True)
        os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'image_artikel'), exist_ok=True)

        # Tangani unggahan gambar profil penulis
        profile_file = request.files.get('profile_picture')
        profile_picture_name = None

        if profile_file and allowed_file(profile_file.filename):
            profile_filename = secure_filename(profile_file.filename)
            profile_file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'avatar_penulis', profile_filename))
            profile_picture_name = profile_filename  # Hanya simpan nama file ke database

        if not profile_picture_name:
            profile_picture_name = 'default-avatar.png'

        # Tangani unggahan gambar artikel
        article_file = request.files.get('article_image')
        article_image_name = None

        if article_file and allowed_file(article_file.filename):
            article_filename = secure_filename(article_file.filename)
            article_file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'image_artikel', article_filename))
            article_image_name = article_filename  # Hanya simpan nama file ke database

        if not article_image_name:
            article_image_name = 'default.jpg'

        # Simpan artikel baru
        slug = slugify(title)
        new_article = Article(
            title=title,
            slug=slug,
            author=author,
            profile_picture=profile_picture_name,
            content=content,
            article_image=article_image_name,
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
                "content": article.content[:100],
                "published_date": article.published_date.strftime('%d-%m-%Y'),
                "profile_picture": article.profile_picture or '/static/uploads/avatar_penulis/default-avatar.png',
                "article_image": article.article_image or '/static/uploads/image_artikel/default.jpg'
            }
            for article in articles
        ]
        return jsonify(articles_data), 200
    except Exception as e:
        return jsonify({'message': 'Gagal memuat data artikel.', 'error': str(e)}), 500

@article_bp.route('/get/<int:article_id>', methods=['GET'])
def get_article(article_id):
    try:
        article = Article.query.get_or_404(article_id)
        return jsonify({
            "id": article.id,
            "title": article.title,
            "author": article.author,
            "content": article.content,
            "profile_picture": article.profile_picture or '/static/uploads/avatar_penulis/default-avatar.png',
            "article_image": article.article_image or '/static/uploads/image_artikel/default.jpg',
            "published_date": article.published_date.strftime('%d-%m-%Y')
        }), 200
    except Exception as e:
        return jsonify({'message': 'Gagal memuat artikel.', 'error': str(e)}), 500


@article_bp.route('/update/<int:article_id>', methods=['POST'])
def update_article(article_id):
    try:
        article = Article.query.get_or_404(article_id)

        # Update field artikel
        article.title = request.form.get('title')
        article.author = request.form.get('author')
        article.content = request.form.get('content')

        # Buat folder jika belum ada
        os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'avatar_penulis'), exist_ok=True)
        os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'image_artikel'), exist_ok=True)

        # Tangani unggahan gambar profil baru
        profile_file = request.files.get('profile_picture')
        if profile_file and allowed_file(profile_file.filename):
            profile_filename = secure_filename(profile_file.filename)
            profile_file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'avatar_penulis', profile_filename))
            article.profile_picture = profile_filename  # Hanya simpan nama file ke database

        # Tangani unggahan gambar artikel baru
        article_file = request.files.get('article_image')
        if article_file and allowed_file(article_file.filename):
            article_filename = secure_filename(article_file.filename)
            article_file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'image_artikel', article_filename))
            article.article_image = article_filename  # Hanya simpan nama file ke database

        db.session.commit()

        return jsonify({'message': 'Artikel berhasil diperbarui!'}), 200
    except Exception as e:
        return jsonify({'message': 'Gagal memperbarui artikel.', 'error': str(e)}), 500


@article_bp.route('/delete/<int:article_id>', methods=['DELETE'])
def delete_article(article_id):
    try:
        article = Article.query.get_or_404(article_id)

        # Hapus file gambar terkait jika ada
        if article.profile_picture and article.profile_picture != 'default-avatar.png':
            profile_path = os.path.join(app.config['UPLOAD_FOLDER'], 'avatar_penulis', article.profile_picture)
            if os.path.exists(profile_path):
                os.remove(profile_path)

        if article.article_image and article.article_image != 'default.jpg':
            article_path = os.path.join(app.config['UPLOAD_FOLDER'], 'image_artikel', article.article_image)
            if os.path.exists(article_path):
                os.remove(article_path)

        db.session.delete(article)
        db.session.commit()
        return jsonify({'message': 'Artikel berhasil dihapus!'}), 200
    except Exception as e:
        return jsonify({'message': 'Gagal menghapus artikel.', 'error': str(e)}), 500




@article_bp.route('/<slug>', methods=['GET'])
def view_article(slug):
    try:
        article = Article.query.filter_by(slug=slug).first_or_404()
        return render_template('page/artikel-content-page.html', article=article)
    except Exception as e:
        return jsonify({'message': 'Gagal memuat artikel.', 'error': str(e)}), 500

