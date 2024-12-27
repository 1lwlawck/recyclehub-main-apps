from flask import Blueprint, request, jsonify
from models.articles import Article
from app import db
from datetime import datetime
from utils import allowed_file, save_file
import os


articles_api = Blueprint('articles_api', __name__, url_prefix='/api/articles')


@articles_api.route('/new', methods=['POST'])
def create_article():
    try:
        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')

        # Simpan gambar profil penulis
        profile_file = request.files.get('profile_picture')
        profile_picture_name = save_file(profile_file, 'avatar_penulis') if profile_file and allowed_file(profile_file.filename) else 'default-avatar.png'

        # Simpan gambar artikel
        article_file = request.files.get('article_image')
        article_image_name = save_file(article_file, 'image_artikel') if article_file and allowed_file(article_file.filename) else 'default.jpg'

        # Simpan artikel baru
        new_article = Article(
            title=title,
            slug=title.lower().replace(' ', '-'),
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


@articles_api.route('/list', methods=['GET'])
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


@articles_api.route('/get/<int:article_id>', methods=['GET'])
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


@articles_api.route('/update/<int:article_id>', methods=['POST'])
def update_article(article_id):
    try:
        article = Article.query.get_or_404(article_id)

        # Update field artikel
        article.title = request.form.get('title')
        article.author = request.form.get('author')
        article.content = request.form.get('content')

        # Tangani unggahan gambar profil baru
        profile_file = request.files.get('profile_picture')
        if profile_file and allowed_file(profile_file.filename):
            article.profile_picture = save_file(profile_file, 'avatar_penulis')

        # Tangani unggahan gambar artikel baru
        article_file = request.files.get('article_image')
        if article_file and allowed_file(article_file.filename):
            article.article_image = save_file(article_file, 'image_artikel')

        db.session.commit()
        return jsonify({'message': 'Artikel berhasil diperbarui!'}), 200
    except Exception as e:
        return jsonify({'message': 'Gagal memperbarui artikel.', 'error': str(e)}), 500


@articles_api.route('/delete/<int:article_id>', methods=['DELETE'])
def delete_article(article_id):
    try:
        print(f"Trying to delete article with ID: {article_id}")
        article = Article.query.get_or_404(article_id)

        # Logging path yang digunakan untuk penghapusan
        if article.profile_picture and article.profile_picture != 'default-avatar.png':
            profile_path = f'static/uploads/avatar_penulis/{article.profile_picture}'
            print(f"Profile path: {profile_path}")
            if os.path.exists(profile_path):
                os.remove(profile_path)

        if article.article_image and article.article_image != 'default.jpg':
            article_path = f'static/uploads/image_artikel/{article.article_image}'
            print(f"Article image path: {article_path}")
            if os.path.exists(article_path):
                os.remove(article_path)

        db.session.delete(article)
        db.session.commit()

        return jsonify({'message': 'Artikel berhasil dihapus!'}), 200
    except Exception as e:
        print(f"Error deleting article: {str(e)}")
        return jsonify({'message': 'Gagal menghapus artikel.', 'error': str(e)}), 500

