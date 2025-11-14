from flask import Flask, render_template, request, redirect, url_for
from model import input_data, ambil_semua_data, masukkan_matakuliah, ambil_semua_matakuliah, masukkan_nilai, menghitung_nilai_mutu

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'student_management_system'

mysql = init_db(app)

@app.route('/')
def home():
    mahasiswa = ambil_semua_data()
    matakuliah = ambil_semua_matakuliah()
    return render_template('home.html', mahasiswa=mahasiswa, matakuliah=matakuliah)

@app.route('/tambah_mahasiswa', methods=['POST'])
def tambah_mahasiswa():
    if request.method == 'POST':
        npm = request.form['npm']
        nama = request.form['nama']
        email = request.form['email']
        input_data(npm, nama, email)
        return redirect(url_for('home'))

@app.route('/tambah_matakuliah', methods=['POST'])
def tambah_matakuliah():
    if request.method == 'POST':