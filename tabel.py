from tkinter import *
from tkinter import messagebox
import mysql.connector
from tkinter import ttk
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

class Data_Siswa(Tk):
    def __init__(self):
        super().__init__()
        self.title("Registrasi Data Siswa")
        self.geometry("850x700")

        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="registerasi"
        )

        # Membuat kursor
        self.cursor = self.db.cursor()

        # Menambahkan Treeview
        self.tree = ttk.Treeview(self, columns=("nis", "nama", "jurusan", "alamat"), show="headings")
        self.tree.heading("nis", text="nis")
        self.tree.heading("nama", text="nama")
        self.tree.heading("jurusan", text="jurusan")
        self.tree.heading("alamat", text="alamat")
        self.tree.grid(row=5, column=0, columnspan=6, pady=10, padx=10)

        self.tampilan_gui()

    def tampilan_gui(self):
        Label(self, text="nis").grid(row=0, column=0, padx=10, pady=10)
        self.nis_entry = Entry(self, width=50)
        self.nis_entry.grid(row=0, column=1, padx=10, pady=10)

        Label(self, text="nama").grid(row=1, column=0, padx=10, pady=10)
        self.nama_entry = Entry(self, width=50)
        self.nama_entry.grid(row=1, column=1, padx=10, pady=10)

        Label(self, text="jurusan").grid(row=2, column=0, padx=10, pady=10)
        self.jurusan_entry = Entry(self, width=50)
        self.jurusan_entry.grid(row=2, column=1, padx=10, pady=10)

        Label(self, text="alamat").grid(row=3, column=0, padx=10, pady=10)
        self.alamat_entry = Entry(self, width=50)
        self.alamat_entry.grid(row=3, column=1, padx=10, pady=10)

        # Menambahkan tombol refresh data
        Button(self, text="Refresh Data", command=self.tampilkan_data).grid(row=4, column=1, columnspan=2, pady=10, padx=10)

        # Menambahkan tombol Update Data
        Button(self, text="Update Data", command=self.update_data).grid(row=4, column=0, columnspan=2, pady=5)

        # Menambahkan tombol Delete Data
        Button(self, text="Delete Data", command=self.delete_data).grid(row=6, column=1, columnspan=2, pady=10)

        # Menambahkan tombol Edit Data
        Button(self, text="Edit Data", command=self.edit_data).grid(row=6, column=0, columnspan=2, pady=10, padx=10)

        #Menambahkan tombol print data
        Button(self, text="Print Data", command=self.cetak_ke_pdf).grid(row=6,column=3, columnspan=2, pady=10, padx=10)

        self.tampilkan_data()

        # Menambahkan event handler untuk item yang dipilih
        self.tree.bind("<ButtonRelease-1>", self.pilih_data)

    def pilih_data(self, event):
        item = self.tree.selection()[0]
        data = self.tree.item(item, 'values')

        # Tampilkan data di entri
        self.nis_entry.delete(0, END)
        self.nis_entry.insert(0, data[0])

        self.nama_entry.delete(0, END)
        self.nama_entry.insert(0, data[1])

        self.jurusan_entry.delete(0, END)
        self.jurusan_entry.insert(0, data[2])

        self.alamat_entry.delete(0, END)
        self.alamat_entry.insert(0, data[3])

    def update_data(self):
        # Ambil data dari entri
        nis = self.nis_entry.get()
        nama = self.nama_entry.get()
        jurusan = self.jurusan_entry.get()
        alamat = self.alamat_entry.get()

        # Update data di database
        query = "UPDATE siswa SET nama=%s, jurusan=%s, alamat=%s WHERE nis=%s"
        values = (nama, jurusan, alamat, nis)

        try:
            self.cursor.execute(query, values)
            self.db.commit()
            messagebox.showinfo("Sukses", "Data berhasil diupdate!")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

        # Hapus data pada treeview dan tampilkan data terbaru
        self.tampilkan_data()

        # Kosongkan entri setelah update
        self.nis_entry.delete(0, END)
        self.nama_entry.delete(0, END)
        self.jurusan_entry.delete(0, END)
        self.alamat_entry.delete(0, END)

    def delete_data(self):
        nis = self.nis_entry.get()

        # Hapus data di database
        query = "DELETE FROM siswa WHERE nis=%s"
        values = (nis,)

        try:
            self.cursor.execute(query, values)
            self.db.commit()
            messagebox.showinfo("Sukses", "Data berhasil dihapus!")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

        # Hapus data pada treeview dan tampilkan data terbaru
        self.tampilkan_data()

        # Kosongkan entri setelah delete
        self.nis_entry.delete(0, END)
        self.nama_entry.delete(0, END)
        self.jurusan_entry.delete(0, END)
        self.alamat_entry.delete(0, END)

    def edit_data(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Peringatan", "Pilih data yang ingin diubah!")
            return

        nis = self.nis_entry.get()
        nama = self.nama_entry.get()
        jurusan = self.jurusan_entry.get()
        alamat = self.alamat_entry.get()

        selected_data = self.tree.item(selected_item)['values']
        if not all((nis, nama, jurusan, alamat)):
            messagebox.showerror("Error", "Isi semua kolom untuk mengubah data!")
            return

        query = "UPDATE siswa SET nis = %s, nama = %s, jurusan = %s, alamat = %s WHERE nis = %s"
        values = (nis, nama, jurusan, alamat, selected_data[0])

        try:
            self.cursor.execute(query, values)
            self.db.commit()
            messagebox.showinfo("Sukses", "Data berhasil diubah!")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

        self.nis_entry.delete(0, END)
        self.nama_entry.delete(0, END)
        self.jurusan_entry.delete(0, END)
        self.alamat_entry.delete(1.0, END)

    def tampilkan_data(self):
        # Hapus data pada treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Ambil data dari database
        self.cursor.execute("SELECT * FROM siswa")
        data = self.cursor.fetchall()

        # Masukkan data ke treeview
        for row in data:
            self.tree.insert("", "end", values=row)

    def cetak_ke_pdf(self):
        doc = SimpleDocTemplate("data_siswa.pdf", pagesize=letter)
        styles = getSampleStyleSheet()
        
        # Membuat data untuk tabel PDF
        data = [["NIS", "Nama", "Jurusan", "Alamat"]]

        for row_id in self.tree.get_children():
            row_data = [self.tree.item(row_id, 'values')[0],
                        self.tree.item(row_id, 'values')[1],
                        self.tree.item(row_id, 'values')[2],
                        self.tree.item(row_id, 'values')[3]]

            data.append(row_data)
        # Membuat tabel PDF
        table = Table(data)
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                ('GRID', (0, 0), (-1, -1), 1, colors.black)]))

        # Menambahkan tabel ke dokumen PDF
        doc.build([table])

        messagebox.showinfo("Sukses", "Data berhasil dicetak ke PDF(data_siswa.pdf).")

if __name__ == "__main__":
    app = Data_Siswa()
    app.mainloop()