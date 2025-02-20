from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import urllib.request
import os
from datetime import datetime
from functools import wraps
import math

app = Flask(__name__)

# KONEKSI KE DB NYA
app.secret_key = 'penitipanbarang'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'penitipan_barang'
mysql = MySQL(app)

# DIREKTORI UNTUK MENYIMPAN FOTO BARANG
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def login_required(f):
    @wraps(f)
    def paksa_login(*args, **kwargs):
        if 'loggedin' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return paksa_login

# INDEX
@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    cursor = mysql.connection.cursor()

    page = request.args.get('page', 1, type=int)
    per_page = 10
    offset = (page - 1) * per_page

    mencari_katakunci = request.args.get('katakunci', '')

    if mencari_katakunci:
        query = """SELECT * FROM barang WHERE nama_pemilik LIKE %s OR nama_barang LIKE %s OR jenis_barang LIKE %s LIMIT %s OFFSET %s"""
        cursor.execute(query, ('%' + mencari_katakunci + '%',) * 3 + (per_page, offset))
    else:
        cursor.execute("SELECT * FROM barang LIMIT %s OFFSET %s", (per_page, offset))

    data = cursor.fetchall()

    if mencari_katakunci:
        cursor.execute("SELECT COUNT(*) FROM barang WHERE nama_pemilik LIKE %s OR nama_barang LIKE %s OR jenis_barang LIKE %s", ('%' + mencari_katakunci + '%',) * 3)
    else:
        cursor.execute("SELECT COUNT(*) FROM barang")
    
    total_data = cursor.fetchone()[0]
    total_pages = math.ceil(total_data / per_page)

    cursor.close()

    return render_template('index.html', barang=data, page=page, total_pages=total_pages, katakunci=mencari_katakunci, total_data=total_data)

# RESGITRASI
@app.route('/registrasi', methods=('GET', 'POST'))
def registrasi():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # NGECEK USERNAME ATAU EMAIL
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM user WHERE username=%s OR email=%s', (username, email, ))
        akun = cursor.fetchone()
        if akun is None:
            cursor.execute('INSERT INTO user VALUES (NULL, %s, %s, %s)', (username, generate_password_hash(password), email))
            mysql.connection.commit()
            flash('Registrasi Anda Berhasil','success')
            return redirect(url_for('login'))
        else:
            flash('Username atau Email Sudah Ada', 'danger')
    return render_template('registrasi.html')

# LOGIN
@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # NGECEK DATA USERNAME
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM user WHERE username=%s', (username,))
        akun = cursor.fetchone()

        if akun is None:
            flash('Login Gagal, Cek Username Anda', 'danger')
        elif not check_password_hash(akun[2], password):
            flash('Login Gagal, Cek Password Anda', 'danger')
        else:
            session['loggedin'] = True
            session['username'] = akun[1]

            return redirect(url_for('index'))

    return render_template('login.html')

# LOGOUT
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('login'))

# MENAMBAHKAN DATA
@app.route('/tambah', methods=['POST'])
def tambah():
    flash('Data Berhasil Ditambahkan')
    if request.method == 'POST':
        nama_pemilik = request.form['nama_pemilik']
        nama_barang = request.form['nama_barang']
        jenis_barang = request.form['jenis_barang']
        waktu_dititip = datetime.now()
        foto_barang = request.files['foto_barang']

        if foto_barang and allowed_file(foto_barang.filename):
            filename = secure_filename(foto_barang.filename)
            foto_barang.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            cursor = mysql.connection.cursor()
            cursor.execute("""INSERT INTO barang (nama_pemilik, nama_barang, jenis_barang, waktu_dititip, foto_barang) VALUES (%s, %s, %s, %s, %s)""", (nama_pemilik, nama_barang, jenis_barang, waktu_dititip, filename))  # Simpan filename
            mysql.connection.commit()
            cursor.close()
        else:
            flash('Harus File Ekstensi Seperti PNG, JPG, JPEG, GIF')
            return redirect(request.url)

        return redirect(url_for('index'))

# MENAMPILKAN GAMBAR
@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

# MENGUBAH DATA
@app.route('/edit', methods=['POST', 'GET'])
def edit():
    cursor = mysql.connection.cursor()
    
    if request.method == 'POST':
        id_barang = request.form['id_barang'] 
        nama_pemilik = request.form['nama_pemilik']
        nama_barang = request.form['nama_barang']
        jenis_barang = request.form['jenis_barang']
        waktu_dititip = request.form['waktu_dititip']
        foto_barang = request.files['foto_barang']

        if foto_barang and allowed_file(foto_barang.filename):
            filename = secure_filename(foto_barang.filename)
            foto_barang.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            foto_path = filename
        else:
            cursor.execute("SELECT foto_barang FROM barang WHERE id_pemilik=%s", (id_barang,))
            foto_path = cursor.fetchone()[0]

        cursor.execute("""UPDATE barang SET 
                            nama_pemilik=%s, 
                            nama_barang=%s, 
                            jenis_barang=%s, 
                            waktu_dititip=%s, 
                            foto_barang=%s 
                            WHERE id_pemilik=%s""", 
                        (nama_pemilik, nama_barang, jenis_barang, waktu_dititip, foto_path, id_barang))
        mysql.connection.commit()
        flash("Data Berhasil Di Perbarui")
        return redirect(url_for('index'))

# MENGUBAH PASSWORD
@app.route('/ubah_password', methods=['GET', 'POST'])
@login_required
def ubah_password():
    if request.method == 'POST':
        password_lama = request.form['password_lama']
        password_baru = request.form['password_baru']
        konfirmasi_password = request.form['konfirmasi_password']

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM user WHERE username=%s', (session['username'],))
        akun = cursor.fetchone()

        if akun is None:
            flash('User  tidak ditemukan', 'danger')
        elif not check_password_hash(akun[2], password_lama):
            flash('Password lama salah', 'danger')
        elif password_baru != konfirmasi_password:
            flash('Password baru dan konfirmasi tidak sama', 'danger')
        else:
            cursor.execute('UPDATE user SET password=%s WHERE username=%s', (generate_password_hash(password_baru), session['username']))
            mysql.connection.commit()
            flash('Password berhasil diubah', 'success')
            return redirect(url_for('index'))

    return render_template('index.html')

# MENGHAPUS DATA
@app.route('/hapus/<string:id_barang>', methods = ['GET'])
def hapus(id_barang):
    flash("Data Telah Berhasil Dihapus")
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM barang WHERE id_pemilik=%s", (id_barang, ))
    mysql.connection.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)