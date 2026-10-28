
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector


# ==================================================
# 1. KONEKSI DATABASE
# ==================================================
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="siakad"
    )


# Menyimpan NIM asli saat data dipilih untuk diedit/dihapus
selected_nim = None


# ==================================================
# 2. FUNGSI MENAMPILKAN DATA
# ==================================================
def load_data():
    for row in tree.get_children():
        tree.delete(row)

    db = None
    cursor = None

    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM mahasiswa")
        rows = cursor.fetchall()

        for row in rows:
            tree.insert("", "end", values=row)

    except Exception as e:
        messagebox.showerror("Database Error", str(e))

    finally:
        if cursor:
            cursor.close()
        if db and db.is_connected():
            db.close()


# ==================================================
# 3. FUNGSI MENGAMBIL INPUT FORM
# ==================================================
def get_input():
    return (
        entry_nim.get().strip(),
        entry_nama.get().strip(),
        combo_jk.get().strip(),
        entry_tanggal.get().strip(),
        entry_tempat.get().strip(),
        entry_alamat.get().strip(),
        entry_tlp.get().strip(),
        entry_email.get().strip(),
        combo_jurusan.get().strip(),
        entry_angkatan.get().strip(),
        combo_status.get().strip()
    )


# ==================================================
# 4. FUNGSI TAMBAH DATA
# ==================================================
def tambah_data():
    data = get_input()

    if not all(data):
        messagebox.showwarning(
            "Peringatan", "Semua kolom wajib diisi!"
        )
        return

    db = None
    cursor = None

    try:
        db = connect_db()
        cursor = db.cursor()

        sql = """
            INSERT INTO mahasiswa
            (nim, nama_lengkap, jenis_kelamin, tanggal_lahir,
             tempat_lahir, alamat, no_telepon, email,
             jurusan, angkatan, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(sql, data)
        db.commit()

        messagebox.showinfo("Sukses", "Data mahasiswa berhasil ditambahkan!")
        clear_fields()
        load_data()

    except Exception as e:
        if db:
            db.rollback()
        messagebox.showerror("Error", f"Gagal menambah data:\n{e}")

    finally:
        if cursor:
            cursor.close()
        if db and db.is_connected():
            db.close()


# ==================================================
# 5. FUNGSI EDIT DATA
# ==================================================
def edit_data():
    global selected_nim

    if selected_nim is None:
        messagebox.showwarning(
            "Peringatan", "Pilih data mahasiswa yang ingin diedit!"
        )
        return

    data = get_input()

    if not all(data):
        messagebox.showwarning(
            "Peringatan", "Semua kolom wajib diisi!"
        )
        return

    db = None
    cursor = None

    try:
        db = connect_db()
        cursor = db.cursor()

        sql = """
            UPDATE mahasiswa SET
            nim=%s, nama_lengkap=%s, jenis_kelamin=%s,
            tanggal_lahir=%s, tempat_lahir=%s, alamat=%s,
            no_telepon=%s, email=%s, jurusan=%s,
            angkatan=%s, status=%s
            WHERE nim=%s
        """

        cursor.execute(sql, data + (selected_nim,))
        db.commit()

        if cursor.rowcount == 0:
            messagebox.showwarning(
                "Informasi", "Data tidak berubah atau tidak ditemukan."
            )
        else:
            messagebox.showinfo(
                "Sukses", "Data mahasiswa berhasil diperbarui!"
            )

        clear_fields()
        load_data()

    except Exception as e:
        if db:
            db.rollback()
        messagebox.showerror("Error", f"Gagal mengedit data:\n{e}")

    finally:
        if cursor:
            cursor.close()
        if db and db.is_connected():
            db.close()


# ==================================================
# 6. FUNGSI HAPUS DATA
# ==================================================
def hapus_data():
    global selected_nim

    if selected_nim is None:
        messagebox.showwarning(
            "Peringatan", "Pilih data mahasiswa yang ingin dihapus!"
        )
        return

    konfirmasi = messagebox.askyesno(
        "Konfirmasi",
        f"Yakin ingin menghapus mahasiswa dengan NIM {selected_nim}?"
    )

    if not konfirmasi:
        return

    db = None
    cursor = None

    try:
        db = connect_db()
        cursor = db.cursor()

        cursor.execute(
            "DELETE FROM mahasiswa WHERE nim = %s",
            (selected_nim,)
        )
        db.commit()

        messagebox.showinfo("Sukses", "Data mahasiswa berhasil dihapus!")
        clear_fields()
        load_data()

    except Exception as e:
        if db:
            db.rollback()
        messagebox.showerror("Error", f"Gagal menghapus data:\n{e}")

    finally:
        if cursor:
            cursor.close()
        if db and db.is_connected():
            db.close()


# ==================================================
# 7. MEMILIH DATA DARI TABEL
# ==================================================
def select_item(event):
    global selected_nim

    selected = tree.selection()

    if not selected:
        return

    values = tree.item(selected[0], "values")

    clear_fields()
    selected_nim = values[0]

    entry_nim.insert(0, values[0])
    entry_nama.insert(0, values[1])
    combo_jk.set(values[2])
    entry_tanggal.insert(0, values[3])
    entry_tempat.insert(0, values[4])
    entry_alamat.insert(0, values[5])
    entry_tlp.insert(0, values[6])
    entry_email.insert(0, values[7])
    combo_jurusan.set(values[8])
    entry_angkatan.insert(0, values[9])
    combo_status.set(values[10])


# ==================================================
# 8. MEMBERSIHKAN FORM
# ==================================================
def clear_fields():
    global selected_nim
    selected_nim = None

    for entry in (
        entry_nim, entry_nama, entry_tanggal, entry_tempat,
        entry_alamat, entry_tlp, entry_email, entry_angkatan
    ):
        entry.delete(0, tk.END)

    combo_jk.set("")
    combo_jurusan.set("")
    combo_status.set("")


# ==================================================
# 9. MEMBUAT JENDELA APLIKASI
# ==================================================
root = tk.Tk()
root.title("Aplikasi Data Mahasiswa - SIAKAD")
root.geometry("1200x700")
root.minsize(950, 600)

# Frame form input
frame_form = tk.LabelFrame(
    root, text=" Form Data Mahasiswa ", padx=10, pady=10
)
frame_form.pack(fill="x", padx=12, pady=8)

# Membuat label dan input dalam dua kelompok
fields = [
    ("NIM", 0), ("Nama Lengkap", 1),
    ("Jenis Kelamin", 2), ("Tanggal Lahir", 3),
    ("Tempat Lahir", 4), ("Alamat", 5),
    ("No Telepon", 6), ("Email", 7),
    ("Jurusan", 8), ("Angkatan", 9),
    ("Status", 10)
]

# Membuat label
for i, (label, _) in enumerate(fields):
    row = i // 2
    col = (i % 2) * 2

    tk.Label(frame_form, text=label).grid(
        row=row, column=col, sticky="w", padx=5, pady=4
    )

# Membuat input NIM dan nama
entry_nim = tk.Entry(frame_form)
entry_nim.grid(row=0, column=1, sticky="ew", padx=5, pady=4)

entry_nama = tk.Entry(frame_form)
entry_nama.grid(row=0, column=3, sticky="ew", padx=5, pady=4)

# Pilihan jenis kelamin
combo_jk = ttk.Combobox(
    frame_form,
    values=["Laki-laki", "Perempuan"],
    state="readonly"
)
combo_jk.grid(row=1, column=1, sticky="ew", padx=5, pady=4)

# Tanggal lahir dengan format YYYY-MM-DD
entry_tanggal = tk.Entry(frame_form)
entry_tanggal.grid(row=1, column=3, sticky="ew", padx=5, pady=4)

# Tempat lahir dan alamat
entry_tempat = tk.Entry(frame_form)
entry_tempat.grid(row=2, column=1, sticky="ew", padx=5, pady=4)

entry_alamat = tk.Entry(frame_form)
entry_alamat.grid(row=2, column=3, sticky="ew", padx=5, pady=4)

# Nomor telepon dan email
entry_tlp = tk.Entry(frame_form)
entry_tlp.grid(row=3, column=1, sticky="ew", padx=5, pady=4)

entry_email = tk.Entry(frame_form)
entry_email.grid(row=3, column=3, sticky="ew", padx=5, pady=4)

# Jurusan
combo_jurusan = ttk.Combobox(
    frame_form,
    values=[
        "Teknik Informatika",
        "Sistem Informasi",
        "Manajemen Informatika"
    ]
)
combo_jurusan.grid(row=4, column=1, sticky="ew", padx=5, pady=4)

# Angkatan
entry_angkatan = tk.Entry(frame_form)
entry_angkatan.grid(row=4, column=3, sticky="ew", padx=5, pady=4)

# Status mahasiswa
combo_status = ttk.Combobox(
    frame_form,
    values=["Aktif", "Cuti", "Tidak Aktif"],
    state="readonly"
)
combo_status.grid(row=5, column=1, sticky="ew", padx=5, pady=4)

# Membuat kolom input menyesuaikan ukuran jendela
frame_form.grid_columnconfigure(1, weight=1)
frame_form.grid_columnconfigure(3, weight=1)


# ==================================================
# 10. TOMBOL CRUD
# ==================================================
frame_btn = tk.Frame(root)
frame_btn.pack(fill="x", padx=12, pady=5)

tk.Button(
    frame_btn, text="Tambah", bg="#4CAF50", fg="white",
    command=tambah_data, width=12
).pack(side="left", padx=5)

tk.Button(
    frame_btn, text="Edit", bg="#2196F3", fg="white",
    command=edit_data, width=12
).pack(side="left", padx=5)

tk.Button(
    frame_btn, text="Hapus", bg="#f44336", fg="white",
    command=hapus_data, width=12
).pack(side="left", padx=5)

tk.Button(
    frame_btn, text="Clear", bg="#9E9E9E", fg="white",
    command=clear_fields, width=12
).pack(side="left", padx=5)


# ==================================================
# 11. TABEL DATA MAHASISWA
# ==================================================
frame_table = tk.Frame(root)
frame_table.pack(fill="both", expand=True, padx=12, pady=8)

columns = (
    "nim", "nama_lengkap", "jenis_kelamin", "tanggal_lahir",
    "tempat_lahir", "alamat", "no_telepon", "email",
    "jurusan", "angkatan", "status"
)

tree = ttk.Treeview(
    frame_table, columns=columns, show="headings"
)

headers = {
    "nim": "NIM",
    "nama_lengkap": "Nama Lengkap",
    "jenis_kelamin": "Jenis Kelamin",
    "tanggal_lahir": "Tanggal Lahir",
    "tempat_lahir": "Tempat Lahir",
    "alamat": "Alamat",
    "no_telepon": "No Telepon",
    "email": "Email",
    "jurusan": "Jurusan",
    "angkatan": "Angkatan",
    "status": "Status"
}

widths = {
    "nim": 100,
    "nama_lengkap": 150,
    "jenis_kelamin": 100,
    "tanggal_lahir": 100,
    "tempat_lahir": 100,
    "alamat": 180,
    "no_telepon": 110,
    "email": 150,
    "jurusan": 150,
    "angkatan": 80,
    "status": 90
}

for col in columns:
    tree.heading(col, text=headers[col])
    tree.column(col, width=widths[col], minwidth=70)

# Scrollbar horizontal
scroll_x = ttk.Scrollbar(
    frame_table, orient="horizontal", command=tree.xview
)
tree.configure(xscrollcommand=scroll_x.set)

# Scrollbar vertikal
scroll_y = ttk.Scrollbar(
    frame_table, orient="vertical", command=tree.yview
)
tree.configure(yscrollcommand=scroll_y.set)

tree.grid(row=0, column=0, sticky="nsew")
scroll_y.grid(row=0, column=1, sticky="ns")
scroll_x.grid(row=1, column=0, sticky="ew")

frame_table.grid_rowconfigure(0, weight=1)
frame_table.grid_columnconfigure(0, weight=1)

# Mengisi form ketika baris tabel diklik
tree.bind("<<TreeviewSelect>>", select_item)

# Memuat data saat aplikasi dibuka
load_data()

# Menjalankan aplikasi
root.mainloop()
