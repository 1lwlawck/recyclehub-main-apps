from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate

# Inisialisasi aplikasi Flask
app = Flask(__name__)

# Konfigurasi aplikasi
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/recycle_hub'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'super_secret_key_that_is_very_secure'

# Inisialisasi ekstensi Flask
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)

# Impor blueprint
from controllers.auth_controller import auth_blueprint
from controllers.admin_controller import admin_blueprint
from controllers.public_controller import public_blueprint  # Perbaiki nama blueprint
from controllers.email_controller import email_blueprint
from controllers.password_controller import password_blueprint

# Registrasi blueprint
app.register_blueprint(public_blueprint, url_prefix='/')  # Tambahkan prefix jika diperlukan
app.register_blueprint(admin_blueprint, url_prefix='/admin')
app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(email_blueprint, url_prefix='/email')
app.register_blueprint(password_blueprint, url_prefix='/password')

# Jalankan aplikasi
if __name__ == '__main__':
    app.run(debug=True)
