from app import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = 'orders'

    id_order = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Relasi ke tabel Users
    tanggal_pengantaran = db.Column(db.Date, nullable=False)  # Tanggal Pengantaran
    waktu_pengantaran = db.Column(db.Time, nullable=False)  # Waktu Pengantaran
    informasi_tambahan = db.Column(db.Text, nullable=True)  # Informasi Tambahan (Opsional)
    status_order = db.Column(db.String(50), default='Menunggu Konfirmasi')  # Status Order

    user = db.relationship('User', backref=db.backref('orders', lazy=True))  # Relasi ke User

    def __repr__(self):
        return f"<Order ID: {self.id_order}, User ID: {self.id_user}, Status: {self.status_order}>"

# Tambahkan relasi detail sampah jika sudah dirancang
class JenisSampah(db.Model):
    __tablename__ = 'jenis_sampah'

    id_jenis_sampah = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama_jenis_sampah = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<JenisSampah ID: {self.id_jenis_sampah}, Nama: {self.nama_jenis_sampah}>"

class DetailSampah(db.Model):
    __tablename__ = 'detail_sampah'

    id_detail = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_order = db.Column(db.Integer, db.ForeignKey('orders.id_order'), nullable=False)  # Relasi ke Order
    id_jenis_sampah = db.Column(db.Integer, db.ForeignKey('jenis_sampah.id_jenis_sampah'), nullable=False)  # Relasi ke Jenis Sampah
    perkiraan_berat = db.Column(db.Float, nullable=False)  # Berat Perkiraan
    foto_sampah = db.Column(db.String(255), nullable=True)  # Path Foto Sampah

    order = db.relationship('Order', backref=db.backref('details', lazy=True))
    jenis_sampah = db.relationship('JenisSampah', backref=db.backref('details', lazy=True))

    def __repr__(self):
        return f"<DetailSampah ID: {self.id_detail}, Order ID: {self.id_order}, Berat: {self.perkiraan_berat}>"
