from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
import os 
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

# Inisialisasi aplikasi Flask
app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Debugging: Cek apakah DATABASE_URI berhasil dibaca
print("DATABASE_URI from .env:", os.getenv('DATABASE_URI'))

# Konfigurasi aplikasi
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS') == 'True'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


# Inisialisasi ekstensi Flask
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

from sqlalchemy import text

# Uji koneksi database
try:
    with app.app_context():
        db.session.execute(text('SELECT 1')) 
        print("Database connection successful!")
except Exception as e:
    print(f"Database connection failed: {e}")



# Impor blueprint
from controllers.auth_controller import auth_blueprint
from controllers.admin_controller import admin_blueprint
from controllers.public_controller import public_blueprint 
from controllers.email_controller import email_blueprint
from controllers.password_controller import password_blueprint
from controllers.users_controller import user_blueprint
from controllers.chatbot_controller import chatbot_blueprint

# Impor blueprint API
from api.auth_api import auth_api_blueprint 
from api.resend_email import resend_email_blueprint
from api.forgot_password import password_api_blueprint



# Registrasi blueprint
app.register_blueprint(public_blueprint, url_prefix='/')  
app.register_blueprint(admin_blueprint, url_prefix='/admin')
app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(email_blueprint, url_prefix='/email')
app.register_blueprint(password_blueprint, url_prefix='/password')
app.register_blueprint(user_blueprint)
app.register_blueprint(chatbot_blueprint)

# Registrasi blueprint API
app.register_blueprint(auth_api_blueprint)
app.register_blueprint(resend_email_blueprint)
app.register_blueprint(password_api_blueprint)


# Jalankan aplikasi
if __name__ == '__main__':
    app.run(debug=True)