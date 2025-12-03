from flask import Flask, render_template, request, redirect, url_for, flash, session
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

# Halaman Utama (Redirect ke Dashboard)
@app.route("/")
def index():
    if "login" not in session and "login_user" not in session:
        return redirect(url_for("login")) 
    return redirect(url_for("dashboard")) 

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user_type = request.form.get("user_type", "")  # 'admin' or 'user'

        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        # Admin login check
        if user_type == "admin":
            cursor.execute("SELECT * FROM admins WHERE username = %s", (username,))
            akun = cursor.fetchone()
            if akun and akun["password"] == password:
                session["login"] = True
                session["id_admin"] = akun["id"]
                session["username"] = akun["username"]
                return redirect(url_for("dashboard"))  # Redirect to dashboard for admin
            else:
                flash("Username atau kata sandi salah!", "danger")

        # User login check
        elif user_type == "user":
            try:
                username = int(username)  # Convert username to integer for user
            except ValueError:
                flash("Username harus berupa angka untuk user!", "danger")
                return redirect(url_for("login"))

            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            if user and user["password"] == password:
                session["login_user"] = True
                session["user_id"] = user["id"]
                session["user_username"] = user["username"]
                return redirect(url_for("nilai_list"))  # Redirect to nilai_list for user
            else:
                flash("Username atau kata sandi salah!", "danger")

        cursor.close()
        db.close()

    return render_template("login.html")

# CRUD MAHASISWA
@app.route("/mahasiswa/tambah", methods=["GET", "POST"])
def tambah_mahasiswa():
    if request.method == "POST":
        nama = request.form.get("nama", "").strip()
        npm = request.form.get("npm", "").strip()
        jurusan = request.form.get("jurusan", "").strip()
        angkatan = request.form.get("angkatan", "").strip()
        program_studi = request.form.get("program_studi", "").strip()

        if not nama or not npm or not jurusan or not angkatan or not program_studi:
            flash("Semua field wajib diisi.", "danger")
            return redirect(url_for("tambah_mahasiswa"))

        db = get_db_connection()
        cursor = db.cursor()

        try:
            cursor.execute("""
                INSERT INTO mahasiswa (npm, nama, jurusan, angkatan, program_studi) 
                VALUES (%s, %s, %s, %s, %s)
            """, (npm, nama, jurusan, angkatan, program_studi))
            db.commit()

            flash("Mahasiswa berhasil ditambahkan.", "success")
            cursor.close()
            db.close()
            return redirect(url_for("index"))

        except Exception as e:
            db.rollback()
            flash(f"Terjadi error saat menyimpan data: {e}", "danger")
            cursor.close()
            db.close()
            return redirect(url_for("tambah_mahasiswa"))

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

        try:
            cursor.execute("INSERT INTO mata_kuliah (nama_matkul, sks) VALUES (%s, %s)", (nama, sks))
            db.commit()
            cursor.execute("SELECT LAST_INSERT_ID()")
            id_matkul = cursor.fetchone()[0]
            
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
            db.rollback()
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
            jumlah_tugas = int(request.form["jumlah_tugas"])
            jumlah_quiz = int(request.form["jumlah_quiz"])

            cursor.execute("""
                INSERT INTO nilai_tugas_detail (id_matkul, npm, tugas_number)
                VALUES (%s, %s, %s)
            """, (id_matkul, id_mahasiswa, jumlah_tugas))
            cursor.execute("""
                INSERT INTO nilai_quiz_detail (id_matkul, npm, quiz_number)
                VALUES (%s, %s, %s)
            """, (id_matkul, id_mahasiswa, jumlah_quiz))

            db.commit()

            flash("Jumlah Tugas dan Quiz berhasil disimpan. Sekarang lanjutkan input nilai tugas dan quiz.", "success")
            return redirect(url_for("nilai_tugas_quiz_input", id_mahasiswa=id_mahasiswa, id_matkul=id_matkul))

        except Exception as e:
            flash(f"Terjadi error saat menyimpan jumlah tugas dan quiz: {e}", "danger")
            try:
                cursor.close()
                db.close()
            except:
                pass
            return redirect(url_for("nilai_input"))

    cursor.close()
    db.close()
    return render_template("nilai_input.html", mahasiswa=mahasiswa, matkul=matkul)


@app.route("/nilai/input/nilai", methods=["GET", "POST"])
def nilai_tugas_quiz_input():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    id_mahasiswa = request.args.get("id_mahasiswa")
    id_matkul = request.args.get("id_matkul")

    cursor.execute("""
        SELECT tugas_number FROM nilai_tugas_detail WHERE npm = %s AND id_matkul = %s
    """, (id_mahasiswa, id_matkul))
    result_tugas = cursor.fetchone()
    if result_tugas:
        jumlah_tugas = result_tugas["tugas_number"]
    else:
        flash("Jumlah tugas tidak ditemukan!", "danger")
        return redirect(url_for("nilai_input"))

    cursor.execute("""
        SELECT quiz_number FROM nilai_quiz_detail WHERE npm = %s AND id_matkul = %s
    """, (id_mahasiswa, id_matkul))
    result_quiz = cursor.fetchone()
    if result_quiz:
        jumlah_quiz = result_quiz["quiz_number"]
    else:
        flash("Jumlah quiz tidak ditemukan!", "danger")
        return redirect(url_for("nilai_input"))

    if request.method == "POST":
        try:
        #simpan nilai tugas
            for i in range(1, jumlah_tugas + 1):
                nilai_tugas = float(request.form.get(f"tugas_{i}", 0))  # Ambil nilai tugas dari form
                cursor.execute("""
                    INSERT INTO nilai_tugas_detail (id_matkul, npm, tugas_number, nilai_tugas)
                    VALUES (%s, %s, %s, %s)
                """, (id_matkul, id_mahasiswa, i, nilai_tugas))

            #simpan nilai quiz
            for i in range(1, jumlah_quiz + 1):
                nilai_quiz = float(request.form.get(f"quiz_{i}", 0))  # Ambil nilai quiz dari form
                cursor.execute("""
                    INSERT INTO nilai_quiz_detail (id_matkul, npm, quiz_number, nilai_quiz)
                    VALUES (%s, %s, %s, %s)
                """, (id_matkul, id_mahasiswa, i, nilai_quiz))

            #simpan nilai UTS, UAS, Responsi, dan Absensi
            uts = float(request.form.get("uts", 0))
            uas = float(request.form.get("uas", 0))
            responsi = float(request.form.get("responsi", 0))
            jumlah_pertemuan = int(request.form.get("jumlah_pertemuan", 0))
            jumlah_hadir = int(request.form.get("jumlah_hadir", 0))

            #simpan data absensi
            cursor.execute("""
                INSERT INTO absensi (id_matkul, npm, jumlah_pertemuan, jumlah_hadir)
                VALUES (%s, %s, %s, %s)
            """, (id_matkul, id_mahasiswa, jumlah_pertemuan, jumlah_hadir))

            db.commit()
            flash("Nilai berhasil disimpan.", "success")
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
    return render_template("nilai_tugas_quiz_input.html", jumlah_tugas=jumlah_tugas, jumlah_quiz=jumlah_quiz)


# LIST NILAI MAHASISWA
@app.route("/nilai/list")
def nilai_list():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT nm.id_nilai, m.nama, mk.nama_matkul, nm.nilai_akhir_total, nm.huruf_matkul
        FROM nilai_akhir_mahasiswa nm
        JOIN mahasiswa m ON nm.npm = m.npm
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
    if "login" not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for("login"))
    
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM mahasiswa")
    mahasiswa = cursor.fetchall()

    cursor.execute("SELECT * FROM mata_kuliah")
    matkul = cursor.fetchall()
    cursor.execute("""
        SELECT nm.id_nilai, m.nama, mk.nama_matkul, nm.nilai_akhir_total, nm.huruf_matkul
        FROM nilai_akhir_mahasiswa nm
        JOIN mahasiswa m ON nm.npm = m.npm
        JOIN mata_kuliah mk ON nm.id_matkul = mk.id_matkul
    """)
    nilai_akhir = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template('dashboard.html', mahasiswa=mahasiswa, matkul=matkul, nilai_akhir=nilai_akhir)


if __name__ == "__main__":
    app.run(debug=True)
