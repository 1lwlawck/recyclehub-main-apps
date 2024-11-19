from werkzeug.security import generate_password_hash
from models.models import db, User
from app import app

# Inisialisasi aplikasi Flask
with app.app_context():
    # Data dummy untuk diisi ke dalam tabel 'users'
    users = [
        {
            "email": "admin@example.com",
            "password": "admin123",  # Password mentah
            "role": "admin"
        },
        {
            "email": "superadmin@example.com",
            "password": "superadmin123",  # Password mentah
            "role": "superadmin"
        },
        {
            "email": "user@example.com",
            "password": "user123",  # Password mentah
            "role": "user"
        }
    ]

    # Loop melalui data user untuk menambahkannya ke database
    for user_data in users:
        # Hash password menggunakan bcrypt
        hashed_password = generate_password_hash(user_data["password"], method='sha256')

        # Buat instance user baru
        new_user = User(
            email=user_data["email"],
            password_hash=hashed_password,
            role=user_data["role"]
        )

        # Tambahkan ke sesi database
        db.session.add(new_user)

    # Commit semua perubahan ke database
    try:
        db.session.commit()
        print("Data berhasil ditambahkan ke database!")
    except Exception as e:
        db.session.rollback()
        print(f"Terjadi kesalahan saat menyimpan data: {e}")
