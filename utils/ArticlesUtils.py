import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """Periksa apakah file memiliki ekstensi yang diizinkan."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_file(file, subfolder, upload_folder='static/uploads'):
    """Simpan file di folder tertentu."""
    os.makedirs(os.path.join(upload_folder, subfolder), exist_ok=True)
    filename = secure_filename(file.filename)
    filepath = os.path.join(upload_folder, subfolder, filename)
    file.save(filepath)
    return filename
