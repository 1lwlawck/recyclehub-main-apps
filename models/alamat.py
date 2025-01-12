from app import db
from datetime import datetime

class Alamat(db.Model):
    __tablename__ = 'alamat'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    provinsi = db.Column(db.String(100), nullable=False)
    kabupaten_kota = db.Column(db.String(100), nullable=False)
    kecamatan = db.Column(db.String(100), nullable=False)
    desa = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    kode_pos = db.Column(db.String(10), nullable=False)
    alamat_lengkap = db.Column(db.Text, nullable=False)

    user = db.relationship('User', backref=db.backref('alamat', lazy=True))

    def __repr__(self):
        return (f"<Alamat User ID: {self.user_id}, Provinsi: {self.provinsi}, Kabupaten/Kota: {self.kabupaten_kota}, "
                f"Kecamatan: {self.kecamatan}, Desa: {self.desa}, Kode Pos: {self.kode_pos}>")