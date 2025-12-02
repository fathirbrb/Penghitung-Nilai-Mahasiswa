from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

# Fungsi untuk menghubungkan ke database
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="penilaian_mahasiswa",
        auth_plugin="mysql_native_password"
    )

app = Flask(__name__)
app.secret_key = "rahasia"  # Gantilah dengan secret key yang lebih aman

# Halaman Utama (Redirect ke Dashboard)
@app.route("/")
def index():
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
        cursor.execute("INSERT INTO mahasiswa (nama, npm) VALUES (%s, %s)", (nama, nim))
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

        # Validasi input
        if not nama or not sks:
            flash("Nama mata kuliah dan SKS wajib diisi.", "danger")
            return redirect(url_for("tambah_matkul"))

        db = get_db_connection()
        cursor = db.cursor()

        try:
            # Simpan mata kuliah
            cursor.execute("INSERT INTO mata_kuliah (nama_matkul, sks) VALUES (%s, %s)", (nama, sks))
            db.commit()

            # Ambil id_matkul mata kuliah yang baru ditambahkan
            cursor.execute("SELECT LAST_INSERT_ID()")
            id_matkul = cursor.fetchone()[0]

            # Simpan persentase penilaian untuk mata kuliah ini
            persentase_absensi = float(request.form["persentase_absensi"])
            persentase_tugas = float(request.form["persentase_tugas"])
            persentase_quiz = float(request.form["persentase_quiz"])
            persentase_uts = float(request.form["persentase_uts"])
            persentase_uas = float(request.form["persentase_uas"])
            persentase_responsi = float(request.form.get("persentase_responsi", 0))

            cursor.execute("""
                INSERT INTO persentase_matkul 
                (id_matkul, persentase_absensi, persentase_tugas, persentase_quiz, 
                persentase_uts, persentase_uas, persentase_responsi) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (id_matkul, persentase_absensi, persentase_tugas, persentase_quiz,
                  persentase_uts, persentase_uas, persentase_responsi))
            db.commit()

            flash("Data mata kuliah dan persentase berhasil disimpan.", "success")
            cursor.close()
            db.close()
            return redirect(url_for("index"))

        except Exception as e:
            db.rollback()  # Rollback jika terjadi error
            flash(f"Terjadi error saat menyimpan data: {e}", "danger")
            cursor.close()
            db.close()
            return redirect(url_for("tambah_matkul"))

    return render_template("tambah_matkul.html")


# Menyimpan persentase penilaian untuk mata kuliah
@app.route("/matkul/persentase/<int:id_matkul>", methods=["GET", "POST"])
def tambah_persentase(id_matkul):
    if request.method == "POST" and "simpan_persentase" in request.form:
        persentase_absensi = float(request.form["persentase_absensi"])
        persentase_tugas = float(request.form["persentase_tugas"])
        persentase_quiz = float(request.form["persentase_quiz"])
        persentase_uts = float(request.form["persentase_uts"])
        persentase_uas = float(request.form["persentase_uas"])
        persentase_responsi = float(request.form.get("persentase_responsi", 0))

        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO persentase_matkul 
            (id_matkul, persentase_absensi, persentase_tugas, persentase_quiz, 
            persentase_uts, persentase_uas, persentase_responsi) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (id_matkul, persentase_absensi, persentase_tugas, persentase_quiz,
              persentase_uts, persentase_uas, persentase_responsi))
        db.commit()
        cursor.close()

        flash("Persentase berhasil disimpan.", "success")
        return redirect(url_for("index"))

    return render_template("tambah_persentase.html", id_matkul=id_matkul)

# INPUT NILAI MAHASISWA (Langkah 1: Simpan jumlah tugas dan quiz terlebih dahulu)
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

            # Ambil jumlah tugas dan quiz yang sudah ditentukan sebelumnya
            cursor.execute("""
                SELECT tugas_number FROM nilai_tugas_detail WHERE id_matkul = %s
            """, (id_matkul,))
            jumlah_tugas = cursor.fetchone()["tugas_number"]

            cursor.execute("""
                SELECT quiz_number FROM nilai_quiz_detail WHERE id_matkul = %s
            """, (id_matkul,))
            jumlah_quiz = cursor.fetchone()["quiz_number"]

            # Menyimpan nilai tugas
            for i in range(1, jumlah_tugas + 1):
                nilai_tugas = float(request.form.get(f"tugas_{i}", 0))
                cursor.execute("""
                    INSERT INTO nilai_tugas_detail (id_matkul, npm, tugas_number, nilai_tugas)
                    VALUES (%s, %s, %s, %s)
                """, (id_matkul, id_mahasiswa, i, nilai_tugas))

            # Menyimpan nilai quiz
            for i in range(1, jumlah_quiz + 1):
                nilai_quiz = float(request.form.get(f"quiz_{i}", 0))
                cursor.execute("""
                    INSERT INTO nilai_quiz_detail (id_matkul, npm, quiz_number, nilai_quiz)
                    VALUES (%s, %s, %s, %s)
                """, (id_matkul, id_mahasiswa, i, nilai_quiz))

            db.commit()
            flash("Nilai tugas dan quiz berhasil disimpan.", "success")
            return redirect(url_for("nilai_input"))

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

# INPUT NILAI TUGAS, QUIZ, UTS, UAS, ABSENSI (Langkah 2: Input nilai tugas dan quiz)
@app.route("/nilai/input/nilai", methods=["GET", "POST"])
def nilai_tugas_quiz_input():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    id_mahasiswa = request.args.get("id_mahasiswa")
    id_matkul = request.args.get("id_matkul")

    # Mengambil jumlah tugas dan quiz yang disimpan sebelumnya
    cursor.execute("""
        SELECT tugas_number FROM nilai_tugas_detail WHERE npm = %s AND id_matkul = %s
    """, (id_mahasiswa, id_matkul))
    jumlah_tugas = cursor.fetchone()["tugas_number"]

    cursor.execute("""
        SELECT quiz_number FROM nilai_quiz_detail WHERE npm = %s AND id_matkul = %s
    """, (id_mahasiswa, id_matkul))
    jumlah_quiz = cursor.fetchone()["quiz_number"]

    if request.method == "POST":
        try:
            # Menyimpan nilai tugas
            for i in range(1, jumlah_tugas + 1):
                nilai_tugas = float(request.form.get(f"tugas_{i}", 0))
                cursor.execute("""
                    INSERT INTO nilai_tugas_detail (id_matkul, npm, tugas_number, nilai_tugas)
                    VALUES (%s, %s, %s, %s)
                """, (id_matkul, id_mahasiswa, i, nilai_tugas))

            # Menyimpan nilai quiz
            for i in range(1, jumlah_quiz + 1):
                nilai_quiz = float(request.form.get(f"quiz_{i}", 0))
                cursor.execute("""
                    INSERT INTO nilai_quiz_detail (id_matkul, npm, quiz_number, nilai_quiz)
                    VALUES (%s, %s, %s, %s)
                """, (id_matkul, id_mahasiswa, i, nilai_quiz))

            db.commit()

            flash("Nilai tugas dan quiz berhasil disimpan.", "success")
            return redirect(url_for("nilai_input"))

        except Exception as e:
            flash(f"Terjadi error saat menyimpan nilai tugas dan quiz: {e}", "danger")
            try:
                cursor.close()
                db.close()
            except:
                pass
            return redirect(url_for("nilai_input"))

    cursor.close()
    db.close()
    return render_template("nilai_tugas_quiz_input.html", jumlah_tugas=jumlah_tugas, jumlah_quiz=jumlah_quiz)

# LIST NILAI MAHASISWA
@app.route("/nilai/list")
def nilai_list():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # Mengambil data nilai akhir mahasiswa yang benar
    cursor.execute("""
        SELECT nm.id_nilai, m.nama, mk.nama_matkul, nm.nilai_akhir_total, nm.huruf_matkul
        FROM nilai_akhir_mahasiswa nm
        JOIN mahasiswa m ON nm.npm = m.npm  -- Ganti id_mahasiswa dengan npm
        JOIN mata_kuliah mk ON nm.id_matkul = mk.id_matkul
        ORDER BY nm.id_nilai DESC
    """)
    data = cursor.fetchall()
    cursor.close()
    db.close()

    return render_template("nilai_list.html", data=data)


# Dashboard Admin
@app.route("/dashboard")
def dashboard():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM mahasiswa")
    mahasiswa = cursor.fetchall()

    cursor.execute("SELECT * FROM mata_kuliah")
    matkul = cursor.fetchall()

    # Query untuk mengambil data nilai akhir mahasiswa yang benar
    cursor.execute("""
        SELECT nm.id_nilai, m.nama, mk.nama_matkul, nm.nilai_akhir_total, nm.huruf_matkul
        FROM nilai_akhir_mahasiswa nm
        JOIN mahasiswa m ON nm.npm = m.npm  -- Ganti id_mahasiswa dengan npm
        JOIN mata_kuliah mk ON nm.id_matkul = mk.id_matkul
    """)
    nilai_akhir = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template('dashboard.html', mahasiswa=mahasiswa, matkul=matkul, nilai_akhir=nilai_akhir)


if __name__ == "__main__":
    app.run(debug=True)
