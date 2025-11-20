from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="penilaian_mahasiswa",
        auth_plugin="mysql_native_password"
    )

app = Flask(__name__)
app.secret_key = "rahasia"

# HALAMAN UTAMA
@app.route("/")
def index():
    # return render_template("index.html")
    return redirect(url_for("dashboard"))

# CRUD MAHASISWA
@app.route("/mahasiswa/tambah", methods=["GET", "POST"])
def tambah_mahasiswa():
    if request.method == "POST":
        nama = request.form.get("nama", "").strip()
        nim = request.form.get("nim", "").strip()

        if not nama or not nim:
            flash("Nama dan NIM wajib diisi.", "danger")
            return redirect(url_for("tambah_mahasiswa"))

        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO mahasiswa (nama, nim) VALUES (%s, %s)", (nama, nim))
        db.commit()
        cursor.close()
        db.close()
        flash("Mahasiswa berhasil ditambahkan.", "success")
        return redirect(url_for("index"))

    return render_template("tambah_mahasiswa.html")

# CRUD MATA KULIAH
@app.route("/matkul/tambah", methods=["GET", "POST"])
def tambah_matkul():
    if request.method == "POST":
        nama = request.form.get("nama", "").strip()
        sks = request.form.get("sks", "").strip()

        if not nama or not sks:
            flash("Nama mata kuliah dan SKS wajib diisi.", "danger")
            return redirect(url_for("tambah_matkul"))

        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO mata_kuliah (nama_matkul, sks) VALUES (%s, %s)", (nama, sks))
        db.commit()
        cursor.close()
        db.close()
        flash("Mata kuliah berhasil ditambahkan.", "success")
        return redirect(url_for("index"))

    return render_template("tambah_matkul.html")

# INPUT NILAI MAHASISWA
@app.route("/nilai/input", methods=["GET", "POST"])
def nilai_input():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM mahasiswa")
    mahasiswa = cursor.fetchall()

    cursor.execute("SELECT * FROM mata_kuliah")
    matkul = cursor.fetchall()

    if request.method == "POST":
        try:
            id_mahasiswa = request.form["id_mahasiswa"]
            id_matkul = request.form["id_matkul"]

            # nilai
            uas = float(request.form.get("uas", 0) or 0)
            uts = float(request.form.get("uts", 0) or 0)
            quiz1 = float(request.form.get("quiz1", 0) or 0)
            quiz2 = float(request.form.get("quiz2", 0) or 0)
            tugas1 = float(request.form.get("tugas1", 0) or 0)
            tugas2 = float(request.form.get("tugas2", 0) or 0)
            tugas3 = float(request.form.get("tugas3", 0) or 0)
            tugas4 = float(request.form.get("tugas4", 0) or 0)

            # absensi
            pertemuan = int(request.form.get("pertemuan", 0) or 0)
            hadir = int(request.form.get("hadir", 0) or 0)

            # hitung quiz & tugas
            rata_quiz = (quiz1 + quiz2) / 2 if (quiz1 or quiz2) else 0
            rata_tugas = (tugas1 + tugas2 + tugas3 + tugas4) / 4 if (tugas1 or tugas2 or tugas3 or tugas4) else 0

            # hitung absensi 
            nilai_absensi = (hadir / pertemuan) * 100 if pertemuan > 0 else 0

            # ambil persentase penilaian untuk matkul ini
            cursor.execute("SELECT * FROM penilaian_mata_kuliah WHERE id_matkul = %s", (id_matkul,))
            p = cursor.fetchone()

            if p is None:
                flash("Konfigurasi penilaian untuk mata kuliah ini belum ada. Hubungi admin.", "danger")
                cursor.close()
                db.close()
                return redirect(url_for("nilai_input"))

            pers_quiz = p.get("persentase_quiz", 0) or 0
            pers_tugas = p.get("persentase_tugas", 0) or 0
            pers_uts = p.get("persentase_uts", 0) or 0
            pers_uas = p.get("persentase_uas", 0) or 0
            pers_abs = p.get("persentase_absensi", 0) or 0
            pers_resp = p.get("persentase_responsi", 0) or 0

            # hitung nilai akhir 
            nilai_akhir = (
                rata_quiz * (pers_quiz / 100) +
                rata_tugas * (pers_tugas / 100) +
                uts * (pers_uts / 100) +
                uas * (pers_uas / 100) +
                nilai_absensi * (pers_abs / 100)
            )

            # jika ada responsi 
            if pers_resp > 0:
                responsi = float(request.form.get("responsi", 0) or 0)
                nilai_akhir += responsi * (pers_resp / 100)

            # huruf nilai
            if nilai_akhir == 100: 
                huruf = "A+"; 
                bobot = 4.0
            elif nilai_akhir >= 76: 
                huruf = "A"; 
                bobot = 4.0
            elif nilai_akhir >= 71: 
                huruf = "B+"; 
                bobot = 3.5
            elif nilai_akhir >= 66: 
                huruf = "B"; 
                bobot = 3.0
            elif nilai_akhir >= 61: 
                huruf = "C+"; 
                bobot = 2.5
            elif nilai_akhir >= 56: 
                huruf = "C"; 
                bobot = 2.0
            elif nilai_akhir >= 45: 
                huruf = "D"; 
                bobot = 1.0
            else: 
                huruf = "E"; bobot = 0.0

            # simpan nilai
            cursor.execute("""
                INSERT INTO nilai_akhir_mahasiswa
                (id_matkul, id_mahasiswa, nilai_akhir_total, huruf_mutu, bobot_mutu, komentar)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (id_matkul, id_mahasiswa, nilai_akhir, huruf, bobot,
                  "Tetap semangat dan terus tingkatkan proses belajar."))

            db.commit()
            flash("Nilai berhasil disimpan.", "success")
            cursor.close()
            db.close()
            return redirect(url_for("nilai_list"))

        except Exception as e:
            flash(f"Terjadi error saat menyimpan nilai: {e}", "danger")
            try:
                cursor.close()
                db.close()
            except:
                pass
            return redirect(url_for("nilai_input"))

    cursor.close()
    db.close()
    return render_template("nilai_input.html", mahasiswa=mahasiswa, matkul=matkul)


# LIST NILAI MAHASISWA
@app.route("/nilai/list")
def nilai_list():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT nm.id_nilai, m.nama, mk.nama_matkul, nm.nilai_akhir_total, nm.huruf_mutu
        FROM nilai_akhir_mahasiswa nm
        JOIN mahasiswa m ON nm.id_mahasiswa = m.id_mahasiswa
        JOIN mata_kuliah mk ON nm.id_matkul = mk.id_matkul
        ORDER BY nm.id_nilai DESC
    """)
    data = cursor.fetchall()
    cursor.close()
    db.close()

    return render_template("nilai_list.html", data=data)

@app.route("/dashboard")
def dashboard():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM mahasiswa")
    mahasiswa = cursor.fetchall()

    cursor.execute("SELECT * FROM mata_kuliah")
    matkul = cursor.fetchall()

    cursor.execute("""
        SELECT nm.id_nilai, m.nama, mk.nama_matkul, nm.nilai_akhir_total, nm.huruf_mutu
        FROM nilai_akhir_mahasiswa nm
        JOIN mahasiswa m ON nm.id_mahasiswa = m.id_mahasiswa
        JOIN mata_kuliah mk ON nm.id_matkul = mk.id_matkul
    """)
    nilai_akhir = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template('dashboard.html', mahasiswa=mahasiswa, matkul=matkul, nilai_akhir=nilai_akhir)


if __name__ == "__main__":
    app.run(debug=True)
