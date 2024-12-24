from flask import Blueprint, render_template, session, redirect, url_for
from models.articles import Article

public_blueprint = Blueprint('public', __name__)

@public_blueprint.route('/')
def home():
    return render_template('page/beranda-page.html')

@public_blueprint.route('/about')
def about():
    return render_template('page/tentangkami-page.html')

@public_blueprint.route('/articles')
def articles():
    # Ambil data artikel dari database
    articles = Article.query.all()
    return render_template('page/artikel-page.html', articles=articles)

@public_blueprint.route('/contact')
def contact():
    return render_template('page/kontakKami-page.html')

@public_blueprint.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('public.home'))

@public_blueprint.route('/feedback')
def feedback():
    return render_template('page/feedback-page.html')

