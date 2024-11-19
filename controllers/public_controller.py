from flask import Blueprint, render_template, session, redirect, url_for

public_blueprint = Blueprint('public', __name__)

@public_blueprint.route('/')
def home():
    return render_template('page/beranda-page.html')

@public_blueprint.route('/about')
def about():
    return render_template('page/tentangkami-page.html')

@public_blueprint.route('/articles')
def articles():
    return render_template('page/artikel-page.html')

@public_blueprint.route('/contact')
def contact():
    return render_template('page/kontakKami-page.html')

@public_blueprint.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('public.home'))
