from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True , autoincrement=True)
    nama_user = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='public')
    is_verified = db.Column(db.Boolean, default=False)
    otp = db.Column(db.Integer, nullable=True)
    otp_expiry = db.Column(db.DateTime, nullable=True)
    reset_token = db.Column(db.String(255), nullable=True)
    reset_token_expiry = db.Column(db.DateTime, nullable=True)
    avatar = db.Column(db.String(255), nullable=True, default="default-avatar.png")  # Tambahkan kolom avatar

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)



