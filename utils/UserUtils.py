import os
from flask import session, flash
from models.user import User

UPLOAD_FOLDER = "static/uploads/avatars"
DEFAULT_AVATAR = "default-avatar.png"

def get_user_by_id(user_id):
    """Ambil user berdasarkan ID dengan validasi keberadaan."""
    user = User.query.get(user_id)
    if not user:
        flash("User tidak ditemukan.", "personal_profile_error")
        return None
    return user


def delete_old_avatar(user):
    """Hapus avatar lama jika bukan default."""
    if user.avatar and user.avatar != DEFAULT_AVATAR:
        old_avatar_path = os.path.join(UPLOAD_FOLDER, user.avatar)
        if os.path.exists(old_avatar_path):
            os.remove(old_avatar_path)


def update_user_session(user):
    """Perbarui session dengan data user terbaru."""
    session["user"] = {
        "id": user.id,
        "nama_user": user.nama_user,
        "email": user.email,
        "role": user.role,
        "avatar": user.avatar if user.avatar else DEFAULT_AVATAR,
    }
