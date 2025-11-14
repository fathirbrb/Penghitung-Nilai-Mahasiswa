from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "sistem_nilai_mahasiswa"

mysql = MySQL(app)

def input_data(npm, nama, email):
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO mahasiswa (npm, nama, nilai) VALUES (%s, %s, %s)",
        (nama, npm, email),
    )
    mysql.connection.commit()
    cur.close()


def ambil_semua_data():
    cur = mysql.connection.cursor
    cur.execute("SELECT * FROM mahasiswa")
    hasil = cur.fetchall()
    cur.close()
    return hasil


def masukkan_matakuliah(nama_matakuliah, sks):
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO matakuliah (kode_mk, nama_mk, sks) VALUES (%s, %s, %s)",
        (nama_matakuliah, sks),
    )
    mysql.connection.commit()
    cur.close()


def ambil_semua_matakuliah():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM matakuliah")
    hasil = cur.fetchall()
    cur.close()
    return hasil

def masukkan_nilai(npm, kode_mk, nilai):
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO nilai(npm, kode_mk, nilai) VALUES (%s, %s, %s)",
        (npm, kode_mk, nilai),
    )
    mysql.connection.commit()
    cur.close()

def menghitung_nilai_mutu(nilai):
    if nilai >= 76:
        return "A"
    if nilai <= 75 and nilai >= 66:
        return "B"
    if nilai <= 65 and nilai >= 56:
        return "C"
    if nilai <= 55 and nilai >= 46:
        return "D"
    else:
        return "E"
    
if __name__ == "__main__":
    app.run(debug=True)

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