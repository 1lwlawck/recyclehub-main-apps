from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email , Length, EqualTo , Regexp

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message="Format email tidak valid")])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Ingat Saya')
    submit = SubmitField('Masuk')


class RegistrationForm(FlaskForm):
    nama_user = StringField('Nama Lengkap', validators=[
        DataRequired(message="Nama lengkap wajib diisi."),
        Length(min=3, max=100, message="Nama harus antara 3 hingga 100 karakter.")
    ])
    email = StringField('Email', validators=[
        DataRequired(message="Email wajib diisi."),
        Email(message="Format email tidak valid.")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Password wajib diisi."),
        Length(min=8, message="Password harus memiliki minimal 8 karakter.")
    ])
    confirm_password = PasswordField('Konfirmasi Password', validators=[
        DataRequired(message="Konfirmasi password wajib diisi."),
        EqualTo('password', message="Password tidak cocok.")
    ])
    submit = SubmitField('Buat Akun Anda')


class ForgotPasswordForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[
            DataRequired(message="Email tidak boleh kosong."),
            Email(message="Masukkan email yang valid."),
            Length(max=100, message="Email tidak boleh lebih dari 100 karakter.")
        ]
    )
    submit = SubmitField('Kirim Reset Link')

class ResetPasswordForm(FlaskForm):
    new_password = PasswordField(
        'Kata Sandi Baru',
        validators=[
            DataRequired(message="Kata sandi baru tidak boleh kosong."),
            Length(min=8, message="Kata sandi harus minimal 8 karakter."),
        ],
        render_kw={
            "placeholder": "Masukkan kata sandi baru",
            "class": "mt-1 block w-full px-3 py-2 border-2 border-black rounded-md text-gray-800 focus:outline-none focus:ring-green-500 focus:border-green-500",
        },
    )
    confirm_password = PasswordField(
        'Konfirmasi Kata Sandi',
        validators=[
            DataRequired(message="Konfirmasi kata sandi tidak boleh kosong."),
            EqualTo('new_password', message="Konfirmasi kata sandi tidak cocok."),
        ],
        render_kw={
            "placeholder": "Konfirmasi kata sandi baru",
            "class": "mt-1 block w-full px-3 py-2 border-2 border-black rounded-md text-gray-800 focus:outline-none focus:ring-green-500 focus:border-green-500",
        },
    )
    submit = SubmitField(
        'Reset Kata Sandi',
        render_kw={
            "class": "w-full py-2 px-4 bg-green-600 hover:bg-green-700 text-white font-bold rounded-md border-2 border-black shadow-[4px_4px_0px_rgba(0,0,0,1)] transition-transform transform hover:scale-105",
        },
    )

class OTPForm(FlaskForm):
    otp = StringField(
        'Kode OTP',
        validators=[
            DataRequired(message='Kode OTP wajib diisi.'),
            Regexp('^[0-9]*$', message='Kode OTP hanya boleh berisi angka.')
        ]
    )
    submit = SubmitField('Verifikasi')
    resend = SubmitField('Kirim Ulang')


