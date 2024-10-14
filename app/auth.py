from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db
from app.admin.forms import LoginForm, RegisterForm

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()  # Inisiasi form Login
    if form.validate_on_submit():  # Validasi form, hanya berjalan saat POST
        email = form.email.data
        password = form.password.data

        # Mencari user berdasarkan email
        user = User.query.filter_by(email=email).first()

        # Jika user ditemukan dan password benar, login user
        if user and check_password_hash(user.password_hash, password):  # Perbaikan: gunakan check_password_hash
            login_user(user)
            return redirect(url_for('main.home'))

        # Jika login gagal, berikan pesan error
        flash('Password atau email salah!', 'error')

    # Jika request adalah GET, atau login gagal, render halaman login
    return render_template('/login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()  # Inisiasi form Register
    if form.validate_on_submit():  # Validasi form
        username = form.username.data
        email = form.email.data
        password = form.password.data

        # Cek apakah email sudah terdaftar
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email ini sudah dipakai', 'error')
            return redirect(url_for('auth.register'))

        # Simpan user baru
        new_user = User(username=username, email=email, password_hash=generate_password_hash(password))

        db.session.add(new_user)
        db.session.commit()

        # Berikan pesan sukses dan arahkan ke halaman login
        flash('Registrasi berhasil, silakan login', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
