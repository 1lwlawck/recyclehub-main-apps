from flask import Flask , session
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from flask_session import Session
from sqlalchemy import text
import os 


# Inisialisasi aplikasi Flask
app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'  # Penyimpanan session di filesystem
Session(app)

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
from api.get_user_points_api import points_blueprint
from api.sentiment_api import sentiment_bp


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
app.register_blueprint(points_blueprint)
app.register_blueprint(sentiment_bp, url_prefix='/api/sentiment')

from models.user import User

DEFAULT_AVATAR = 'default-avatar.png'

@app.before_request
def ensure_avatar_in_session():
    if 'user' in session:
        user = User.query.get(session['user']['id'])
        if user:
            session['user']['avatar'] = user.avatar if user.avatar else DEFAULT_AVATAR

# Jalankan aplikasi
if __name__ == '__main__':
    app.run()
