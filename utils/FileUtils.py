import os
from werkzeug.utils import secure_filename
from time import time

UPLOAD_FOLDER = "static/uploads/avatars"
DEFAULT_AVATAR = "default-avatar.png"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename):
    """Validasi apakah file memiliki ekstensi yang diizinkan."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_new_avatar(file):
    """Simpan file avatar baru dengan nama unik."""
    filename = f"{int(time())}_{secure_filename(file.filename)}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    return filename
