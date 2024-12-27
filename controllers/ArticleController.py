from flask import Blueprint, render_template
from models.articles import Article

article_bp = Blueprint('article', __name__, url_prefix='/articles')


@article_bp.route('/<slug>', methods=['GET'])
def view_article(slug):
    try:
        article = Article.query.filter_by(slug=slug).first_or_404()
        return render_template('page/artikel-content-page.html', article=article)
    except Exception as e:
        return render_template('error.html', message='Gagal memuat artikel.', error=e)
