from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "sistem_nilai_mahasiswa"

mysql = MySQL(app)

def insert_data(npm, nama, email):
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