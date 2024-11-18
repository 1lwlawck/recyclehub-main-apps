from flask import Flask, render_template, redirect, url_for, session
from livereload import Server

app = Flask(__name__)
app.debug = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = "key"


# Halaman Awal 
@app.route('/')
def home():
    return render_template('page/beranda-page.html')

@app.route('/about')
def about():
    return render_template('page/tentangkami-page.html')

@app.route('/articles')
def articles():
    return render_template('page/artikel-page.html')

@app.route('/content')
def content():
    return render_template('sections/artikel-content.html')

@app.route('/contact')
def contact():  
    return render_template('page/kontakKami-page.html')



# Halaman Admin 

@app.route('/admin/dashboard')
def admin_dashboard():
    return render_template('admin/dashboard-admin.html')

@app.route('/admin/dropoff')
def admin_dropoff():
    return render_template('admin/dropoff-admin.html')

@app.route('/admin/riwayat')
def admin_riwayat():
    return render_template('admin/riwayat-admin.html')

@app.route('/admin/message')
def admin_message():
    return render_template('admin/message-admin.html')

# Route Logout
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('home'))



# Route untuk auth
@app.route('/login')
def login():
    return render_template('page/login-page.html')

@app.route('/register')
def register():
    return render_template('page/register-page.html')


if __name__ == "__main__":
    app.run(debug=True)
