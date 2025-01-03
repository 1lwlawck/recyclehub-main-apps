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
app.config['SESSION_TYPE'] = 'filesystem'  
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
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  



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
from controllers.AuthController import auth_blueprint
from controllers.AdminController import admin_blueprint
from controllers.PublicController import public_blueprint 
from controllers.PasswordController import password_blueprint
from controllers.UsersController import user_blueprint
from controllers.ChatbotController import chatbot_blueprint
from controllers.ArticleController import article_bp
from controllers.OrderController import order_blueprint
from controllers.MessageController import message_blueprint


# Impor blueprint API
from api.Authentication import auth_api_blueprint 
from api.Sentiment import sentiment_bp
from api.Users import users_api_blueprint
from api.Articles import articles_api
from api.Emails import email_blueprint
from api.Message import messages_api_blueprint


# Registrasi blueprint
app.register_blueprint(public_blueprint, url_prefix='/')  
app.register_blueprint(admin_blueprint, url_prefix='/admin')
app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(email_blueprint, url_prefix='/email')
app.register_blueprint(password_blueprint, url_prefix='/password')
app.register_blueprint(user_blueprint)
app.register_blueprint(chatbot_blueprint)
app.register_blueprint(article_bp)
app.register_blueprint(order_blueprint, url_prefix='/orders')
app.register_blueprint(message_blueprint)


# Registrasi blueprint API
app.register_blueprint(auth_api_blueprint)
app.register_blueprint(sentiment_bp, url_prefix='/api/sentiment')
app.register_blueprint(users_api_blueprint, url_prefix='/api/users')
app.register_blueprint(articles_api)
app.register_blueprint(messages_api_blueprint)

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



