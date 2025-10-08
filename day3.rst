======================================
🧩 Arkademy GSI Lab 18.0 - Day 3
======================================

**Topik:** Development Basic Odoo 18 CE  

**Durasi:** 09.00 – 17.00 WIB  

**Versi:** Odoo 18.0 Community Edition

--------------------------------------
🎯 Tujuan Pembelajaran
--------------------------------------

Pada akhir sesi hari ketiga, peserta akan mampu:

- Membuat laporan PDF menggunakan paperformat, action, dan template.
- Menghasilkan laporan dalam format Excel untuk data perpustakaan.
- Mengaplikasikan semua konsep yang telah dipelajari melalui latihan terstruktur.
- Memahami dasar-dasar fungsionalitas Odoo seperti Sale Order dan Website.

11. Reporting
--------------------------------------

Odoo menyediakan mekanisme pelaporan yang kuat untuk menghasilkan laporan dalam format PDF dan Excel.  
Pada sesi ini, kita akan membuat laporan untuk **Transaksi Peminjaman** (``library.loan``) dalam format PDF dan Excel.

11.1. Reports (PDF)
=====================================

Laporan PDF di Odoo dibuat menggunakan **QWeb**, sebuah template engine berbasis XML.  
Langkah-langkahnya meliputi pembuatan **paperformat**, mendefinisikan **action report**, dan membuat **template QWeb**.

11.1.1. Membuat Paperformat
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Paperformat** digunakan untuk menentukan ukuran kertas, margin, dan orientasi laporan PDF.  
Buat file baru bernama ``reports/library_report.xml``:

.. code-block:: xml

   <odoo>
       <record id="paperformat_library_loan" model="report.paperformat">
           <field name="name">Library Loan Report Format</field>
           <field name="format">A4</field>
           <field name="orientation">Portrait</field>
           <field name="margin_top">30</field>
           <field name="margin_bottom">20</field>
           <field name="margin_left">10</field>
           <field name="margin_right">10</field>
           <field name="header_spacing">30</field>
           <field name="dpi">90</field>
       </record>
   </odoo>

**Penjelasan:**

- ``format``: Menentukan ukuran kertas (misalnya A4, Letter).
- ``margin_*``: Margin atas, bawah, kiri, dan kanan dalam satuan milimeter.
- ``header_spacing``: Jarak header dari tepi atas.
- ``dpi``: Resolusi cetak untuk laporan.

11.1.2. Membuat Template QWeb
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Template QWeb** mendefinisikan struktur dan konten laporan.  
Tambahkan template berikut di file ``reports/library_report.xml``:

.. code-block:: xml

   <template id="report_library_loan_template">
       <t t-call="web.html_container">
           <t t-foreach="docs" t-as="loan">
               <t t-call="web.external_layout">
                   <div class="page">
                       <h2>Laporan Peminjaman Buku</h2>
                       <table class="table table-bordered">
                           <tr>
                               <th>Peminjam</th>
                               <td><t t-esc="loan.borrower_id.name"/></td>
                           </tr>
                           <tr>
                               <th>Buku</th>
                               <td><t t-esc="loan.book_id.name"/></td>
                           </tr>
                           <tr>
                               <th>Tanggal Pinjam</th>
                               <td><t t-esc="loan.borrow_date" t-options="{'widget': 'date'}"/></td>
                           </tr>
                           <tr>
                               <th>Tanggal Kembali</th>
                               <td><t t-esc="loan.return_date" t-options="{'widget': 'date'}"/></td>
                           </tr>
                           <tr>
                               <th>Status</th>
                               <td><t t-esc="loan.state"/></td>
                           </tr>
                       </table>
                   </div>
               </t>
           </t>
       </t>
   </template>

**Penjelasan:**

- ``t-call="web.html_container"``: Memanggil layout dasar Odoo untuk laporan.
- ``t-foreach="docs"``: Mengiterasi setiap record ``library.loan`` yang dipilih.
- ``t-esc``: Menampilkan nilai field dengan escape untuk keamanan.
- ``t-options="{'widget': 'date'}"``: Memformat tanggal agar lebih rapi.

Dokumentasi lengkap tentang QWeb dapat ditemukan di:
https://www.odoo.com/documentation/18.0/developer/reference/backend/reports.html

11.1.3. Membuat Action Report
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Action report** menghubungkan model dengan template laporan dan paperformat.  
Tambahkan kode berikut di file ``reports/library_report.xml``:

.. code-block:: xml

   <record id="action_report_library_loan" model="ir.actions.report">
       <field name="name">Laporan Peminjaman Buku</field>
       <field name="model">library.loan</field>
       <field name="report_type">qweb-pdf</field>
       <field name="report_name">fahriza_latihan.report_library_loan_template</field>
       <field name="paperformat_id" ref="paperformat_library_loan"/>
       <field name="print_report_name">('Laporan Peminjaman - %s' % (object.borrower_id.name))</field>
       <field name="binding_model_id" ref="fahriza_library.model_library_loan" />
       <field name="binding_type">report</field>
   </record>

**Penjelasan:**

- ``report_type``: Menentukan jenis laporan, dalam hal ini PDF berbasis QWeb.
- ``report_name``: Nama unik template laporan (akan didefinisikan di bawah).
- ``print_report_name``: Nama file PDF saat diunduh, bisa dinamis berdasarkan data record.

11.1.5. Registrasi File di Manifest
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Tambahkan file laporan ke ``__manifest__.py``:

.. code-block:: python

   'data': [
       'data/fahriza_latihan_data.xml',
       'security/library_groups.xml',
       'security/ir.model.access.csv',
       'security/library_record_rules.xml',
       'views/library_book_views.xml',
       'views/library_category_views.xml',
       'views/library_author_views.xml',
       'views/res_partner_views.xml',
       'views/library_loan_views.xml',
       'views/library_member_views.xml',
       'wizard/library_borrow_wizard_views.xml',
       'reports/library_report.xml',
   ],

💡 **Latihan:**

1. Buat file ``reports/library_report.xml`` dengan kode di atas.
2. Tambahkan tombol cetak ke form view ``library.loan``.
3. Daftarkan file laporan di ``__manifest__.py``.
4. Restart Odoo dan upgrade modul.
5. Buka menu **Perpustakaan → Transaksi Peminjaman**, pilih satu transaksi, dan klik tombol **Cetak Laporan**. Perhatikan hasil PDF yang dihasilkan.

11.2. Reports (Excel)
=====================================

Untuk membuat laporan Excel di Odoo, kita dapat memanfaatkan modul `report_xlsx` dari Odoo Community Association (OCA) yang mendukung pembuatan laporan XLSX secara terintegrasi dengan sistem action report Odoo. Modul ini memerlukan pustaka Python `xlsxwriter`. Kita akan membuat laporan Excel untuk daftar transaksi peminjaman.

11.2.1. Menginstal Modul dan Dependensi
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pastikan modul `report_xlsx` sudah diinstal dari Odoo Apps Store[](https://apps.odoo.com/apps/modules/18.0/report_xlsx). 
Instal dependensi Python dengan perintah:

.. code-block:: bash

   pip3 install xlsxwriter

Tambahkan `report_xlsx` sebagai dependensi di file ``__manifest__.py``:

.. code-block:: python

   'depends': [
       'base',
       'report_xlsx',  # Tambahkan ini
   ],

11.2.2. Membuat Kelas Laporan Excel
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Buat file baru ``reports/library_loan_xlsx.py`` di folder `reports` untuk mendefinisikan laporan XLSX:

.. code-block:: python

   from odoo import models

   class LibraryLoanXlsx(models.AbstractModel):
       _name = 'report.fahriza_latihan.report_library_loan_xlsx'
       _inherit = 'report.report_xlsx.abstract'

       def generate_xlsx_report(self, workbook, data, loans):
           # Format teks tebal
           bold = workbook.add_format({'bold': True})
           sheet = workbook.add_worksheet('Transaksi Peminjaman')

           # Header kolom
           sheet.write(0, 0, 'Peminjam', bold)
           sheet.write(0, 1, 'Buku', bold)
           sheet.write(0, 2, 'Tanggal Pinjam', bold)
           sheet.write(0, 3, 'Tanggal Kembali', bold)
           sheet.write(0, 4, 'Status', bold)

           # Data
           row = 1
           for loan in loans:
               sheet.write(row, 0, loan.borrower_id.name)
               sheet.write(row, 1, loan.book_id.name)
               sheet.write(row, 2, str(loan.borrow_date))
               sheet.write(row, 3, str(loan.return_date) if loan.return_date else '')
               sheet.write(row, 4, loan.state)
               row += 1

**Penjelasan Komponen Utama:**

- **`AbstractModel`**:
  - **Definisi**: `AbstractModel` adalah kelas dasar di Odoo yang digunakan untuk mendefinisikan model yang tidak disimpan sebagai tabel di database.
  - **Karakteristik**:
    - Bersifat abstrak dan digunakan untuk keperluan logika bisnis atau utilitas, seperti laporan, wizard, atau helper class.
    - Tidak menghasilkan tabel fisik di database, sehingga cocok untuk operasi sementara.
  - **Penggunaan dalam Konteks Ini**:
    - Kelas `LibraryLoanXlsx` menggunakan `AbstractModel` karena laporan XLSX adalah logika sementara yang dijalankan saat pengguna meminta cetak, bukan data yang disimpan permanen.
    - Model ini mewarisi `report.report_xlsx.abstract` dari modul `report_xlsx`, yang menyediakan kerangka kerja untuk menghasilkan file Excel.

- **`_name = 'report.fahriza_latihan.report_library_loan_xlsx'`**:
  - **Definisi**: Field `_name` adalah pengidentifikasi unik untuk model Odoo, yang dalam kasus laporan mengikuti konvensi `'report.<module_name>.<report_identifier>'`.
  - **Penjelasan Format**:
    - **`report`**: Menandakan bahwa ini adalah model laporan.
    - **`fahriza_latihan`**: Nama modul Anda, sesuai dengan nama modul `fahriza_latihan` di `day3.rst`.
    - **`report_library_loan_xlsx`**: Identifikasi unik untuk laporan ini, mencerminkan tujuannya sebagai laporan Excel untuk transaksi peminjaman buku.
  - **Integrasi**:
    - Nilai ini harus sesuai dengan field `report_name` di definisi action report XML (lihat 11.2.3) agar Odoo dapat menghubungkan model laporan dengan action yang dipanggil dari UI.
    - Menunjukkan bahwa laporan ini spesifik untuk modul `fahriza_latihan` dan digunakan untuk menghasilkan file XLSX berdasarkan data `library.loan`.

Tambahkan file ini ke `fahriza_latihan/__init__.py`:

.. code-block:: python

   from . import reports  # Tambahkan ini

Buat folder `reports/__init__.py` jika belum ada:

.. code-block:: python

   from . import library_loan_xlsx

11.2.3. Mendefinisikan Action Report
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Tambahkan definisi action report untuk XLSX di file `reports/library_report.xml`:

.. code-block:: xml

   <record id="action_report_library_loan_xlsx" model="ir.actions.report">
       <field name="name">Laporan Peminjaman Buku (XLSX)</field>
       <field name="model">library.loan</field>
       <field name="report_type">xlsx</field>
       <field name="report_name">fahriza_latihan.report_library_loan_xlsx</field>
       <field name="report_file">fahriza_latihan.report_library_loan_xlsx</field>
       <field name="binding_model_id" ref="model_library_loan"/>
       <field name="binding_type">report</field>
       <field name="attachment_use" eval="False"/>
   </record>

Pastikan file `reports/library_report.xml` sudah terdaftar di `data` pada `__manifest__.py`.

11.2.4. Verifikasi di UI
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Setelah restart Odoo dan upgrade modul `fahriza_latihan`, buka form view transaksi peminjaman (`library.loan`).
- Di kanan atas, klik ikon printer (dropdown "Print") dan pilih "Laporan Peminjaman Buku (XLSX)" untuk mengunduh file Excel.

💡 **Latihan:**

1. Instal modul `report_xlsx` dari Odoo Apps Store.
2. Instal pustaka `xlsxwriter` dengan perintah di atas.
3. Tambahkan dependensi di `__manifest__.py`.
4. Buat file `reports/library_loan_xlsx.py` dan impor di `models/__init__.py`.
5. Tambahkan definisi action report di `reports/library_report.xml`.
6. Restart Odoo dan upgrade modul.
7. Buka menu **Perpustakaan → Transaksi Peminjaman**, pilih transaksi, klik ikon printer, dan pilih "Laporan Peminjaman Buku (XLSX)". Perhatikan file Excel yang diunduh.

--------------------------------------
12. Exercise
--------------------------------------

Latihan ini dirancang untuk mengintegrasikan semua konsep yang telah dipelajari pada Hari 1 dan Hari 2, ditambah dengan pelaporan dari Hari 3.  
Tujuannya adalah membangun fitur lengkap untuk modul perpustakaan.

💡 **Latihan Terstruktur:**

1. **Menambahkan Field Baru ke library.book**  
   Tambahkan field ``total_loan_count`` (Integer, computed) di model ``library.book`` untuk menghitung total peminjaman buku (termasuk yang sudah dikembalikan).  
   - Gunakan ``@api.depends`` untuk menghitung berdasarkan ``loan_ids``.  
   - Tambahkan field ini ke form dan list view di ``views/library_book_views.xml``.  

2. **Membuat Constraint Baru**  
   Tambahkan Python constraint di model ``library.loan`` untuk memastikan ``return_date`` tidak boleh sebelum ``borrow_date``.  

3. **Menambahkan Filter di Search View**  
   Perbarui search view ``library.loan`` untuk menambahkan filter:  
   - “Peminjaman Aktif” (state = 'borrowed').  
   - “Peminjaman Selesai” (state = 'returned').  

4. **Membuat Laporan PDF untuk library.book**  
   Buat laporan PDF untuk model ``library.book`` yang menampilkan daftar buku beserta kategori dan penulis.  
   - Buat paperformat baru di ``reports/library_report.xml``.  
   - Tambahkan action report dan template QWeb.  
   - Tambahkan tombol cetak di form view ``library.book``.  

5. **Membuat Laporan Excel untuk library.book**  
   Tambahkan method di model ``library.book`` untuk export daftar buku ke Excel, termasuk kolom: Judul, ISBN, Kategori, dan Stok Tersedia.  
   - Tambahkan tombol di form view untuk memanggil method ini.  

6. **Menguji Keamanan**  
   - Modifikasi access right pada model ``library.book`` sehingga hanya group ``Librari Super Admin`` yang dapat menambah atau menghapus record. Selain itu, hanya dapat membaca dan mengubah.
   - Modifikasi access right pada model ``library.category`` sehingga hanya group ``Librari Super Admin`` yang dapat menambah, merubah atau menghapus record. Selain itu, hanya dapat melihat.
   - Modifikasi access right pada model ``library.author`` sehingga hanya group ``Librari Super Admin`` yang dapat menambah, merubah atau menghapus record. Selain itu, hanya dapat melihat.

7. **Menambahkan Button Aksi di Form View**  
   - Tambahkan tombol aksi di form view ``library.loan`` untuk mengubah status peminjaman atau kolom ``state`` menjadi ``returned``.

💡 **Langkah-langkah:**

1. Implementasikan kode untuk masing-masing tugas di atas.  
2. Update file ``__manifest__.py`` jika ada file baru.  
3. Restart Odoo dan upgrade modul.  
4. Uji setiap fitur di UI Odoo dan perhatikan hasilnya.  