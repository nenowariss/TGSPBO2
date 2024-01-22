from tkinter import *
from tkinter import messagebox
import mysql.connector
from tkinter import ttk
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

class Data_Guru(Tk):
    def __init__(self):
        super().__init__()
        self.title("Registrasi Data Guru")
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
        self.tree = ttk.Treeview(self, columns=("kode_guru", "nama_guru", "kelompok_guru", "mata_pelajaran"), show="headings")
        self.tree.heading("kode_guru", text="kode_guru")
        self.tree.heading("nama_guru", text="nama_guru")
        self.tree.heading("kelompok_guru", text="kelompok_guru")
        self.tree.heading("mata_pelajaran", text="mata_pelajaran")
        self.tree.grid(row=5, column=0, columnspan=6, pady=10, padx=10)

        self.tampilan_gui()

    def tampilan_gui(self):
        Label(self, text="kode_guru").grid(row=0, column=0, padx=10, pady=10)
        self.kode_guru_entry = Entry(self, width=50)
        self.kode_guru_entry.grid(row=0, column=1, padx=10, pady=10)

        Label(self, text="nama_guru").grid(row=1, column=0, padx=10, pady=10)
        self.nama_guru_entry = Entry(self, width=50)
        self.nama_guru_entry.grid(row=1, column=1, padx=10, pady=10)

        Label(self, text="kelompok_guru").grid(row=2, column=0, padx=10, pady=10)
        self.kelompok_guru_entry = Entry(self, width=50)
        self.kelompok_guru_entry.grid(row=2, column=1, padx=10, pady=10)

        Label(self, text="mata_pelajaran").grid(row=3, column=0, padx=10, pady=10)
        self.mata_pelajaran_entry = Entry(self, width=50)
        self.mata_pelajaran_entry.grid(row=3, column=1, padx=10, pady=10)

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
        self.kode_guru_entry.delete(0, END)
        self.kode_guru_entry.insert(0, data[0])

        self.nama_guru_entry.delete(0, END)
        self.nama_guru_entry.insert(0, data[1])

        self.kelompok_guru_entry.delete(0, END)
        self.kelompok_guru_entry.insert(0, data[2])

        self.mata_pelajaran_entry.delete(0, END)
        self.mata_pelajaran_entry.insert(0, data[3])

    def update_data(self):
        # Ambil data dari entri
        kode_guru = self.kode_guru_entry.get()
        nama_guru = self.nama_guru_entry.get()
        kelompok_guru = self.kelompok_guru_entry.get()
        mata_pelajaran = self.mata_pelajaran_entry.get()

        # Update data di database
        query = "UPDATE guru SET kode_guru=%s, nama_guru=%s, kelompok_guru=%s, mata_pelajaran=%s WHERE kode_guru=%s"
        values = (kode_guru, nama_guru, kelompok_guru, mata_pelajaran, kode_guru)

        try:
            self.cursor.execute(query, values)
            self.db.commit()
            messagebox.showinfo("Sukses", "Data berhasil diupdate!")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

        # Hapus data pada treeview dan tampilkan data terbaru
        self.tampilkan_data()

        # Kosongkan entri setelah update
        self.kode_guru_entry.delete(0, END)
        self.nama_guru_entry.delete(0, END)
        self.kelompok_guru_entry.delete(0, END)
        self.mata_pelajaran_entry.delete(0, END)

    def delete_data(self):
        kode_guru = self.kode_guru_entry.get()

        # Hapus data di database
        query = "DELETE FROM guru WHERE kode_guru=%s"
        values = (kode_guru,)

        try:
            self.cursor.execute(query, values)
            self.db.commit()
            messagebox.showinfo("Sukses", "Data berhasil dihapus!")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

        # Hapus data pada treeview dan tampilkan data terbaru
        self.tampilkan_data()

        # Kosongkan entri setelah delete
        self.kode_guru_entry.delete(0, END)
        self.nama_guru_entry.delete(0, END)
        self.kelompok_guru_entry.delete(0, END)
        self.mata_pelajaran_entry.delete(0, END)

    def edit_data(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Peringatan", "Pilih data yang ingin diubah!")
            return

        kode_guru = self.kode_guru_entry.get()
        nama_guru = self.nama_guru_entry.get()
        kelompok_guru = self.kelompok_guru_entry.get()
        mata_pelajaran = self.mata_pelajaran_entry.get()

        selected_data = self.tree.item(selected_item)['values']
        if not all((kode_guru, nama_guru, kelompok_guru, mata_pelajaran)):
            messagebox.showerror("Error", "Isi semua kolom untuk mengubah data!")
            return

        query = "UPDATE guru SET kode_guru=%s, nama_guru=%s, kelompok_guru=%s, mata_pelajaran=%s WHERE kode_guru=%s"
        values = (kode_guru, nama_guru, kelompok_guru, mata_pelajaran, kode_guru)

        try:
            self.cursor.execute(query, values)
            self.db.commit()
            messagebox.showinfo("Sukses", "Data berhasil diubah!")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

        self.kode_guru_entry.delete(0, END)
        self.nama_guru_entry.delete(0, END)
        self.kelompok_guru_entry.delete(0, END)
        self.mata_pelajaran_entry.delete(0, END)

    def tampilkan_data(self):
        # Hapus data pada treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Ambil data dari database
        self.cursor.execute("SELECT * FROM guru")
        data = self.cursor.fetchall()

        # Masukkan data ke treeview
        for row in data:
            self.tree.insert("", "end", values=row)

    def cetak_ke_pdf(self):
        doc = SimpleDocTemplate("data_guru.pdf", pagesize=letter)
        styles = getSampleStyleSheet()
        
        # Membuat data untuk tabel PDF
        data = [["kode_guru", "nama_guru", "kelompok_guru", "mata_pelajaran"]]

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

        messagebox.showinfo("Sukses", "Data berhasil dicetak ke PDF(data_guru.pdf).")

if __name__ == "__main__":
    app = Data_Guru()
    app.mainloop()