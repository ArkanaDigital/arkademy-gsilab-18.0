======================================
🧩 Arkademy GSI Lab 18.0 - Day 2
======================================

**Topik:** Development Basic Odoo 18 CE  

**Durasi:** 09.00 – 17.00 WIB  

**Versi:** Odoo 18.0 Community Edition

--------------------------------------
🎯 Tujuan Pembelajaran
--------------------------------------

Pada akhir sesi hari kedua, peserta akan mampu:

- Membuat model transaksi sederhana untuk perpustakaan.
- Menggunakan computed fields dan default values.
- Memahami dependencies antar field.
- Menerapkan constraints pada model.
- Menggunakan advanced view seperti list dan search view.
- Menyusun mekanisme keamanan berbasis grup, hak akses, dan record rule.
- Membuat wizard interaktif dan menjalankannya melalui UI.

--------------------------------------
🧱 Persiapan Sebelum Memulai
--------------------------------------

Sebelum mempelajari *computed field*, kita akan menambahkan model transaksi peminjaman buku  
dan menyesuaikan struktur model ``library.book`` agar bisa menghitung stok dan ketersediaan otomatis.

--------------------------------------
📘 Model Baru: library.loan
--------------------------------------

Buat file baru ``models/library_loan.py``:

.. code-block:: python

   from odoo import models, fields, api

   class LibraryLoan(models.Model):
       _name = 'library.loan'
       _description = 'Transaksi Peminjaman Buku'

       borrower_id = fields.Many2one(
           'res.partner',
           string="Peminjam",
           required=True,
           domain=[('is_library_member', '=', True)]
       )
       book_id = fields.Many2one('library.book', string="Buku", required=True)
       borrow_date = fields.Date("Tanggal Pinjam", required=True)
       return_date = fields.Date("Tanggal Kembali")
       state = fields.Selection([
           ('borrowed', 'Dipinjam'),
           ('returned', 'Dikembalikan')
       ], string="Status", default='borrowed')

💡 **Penjelasan:**

- Model ini merekam transaksi peminjaman buku.

- Field ``borrower_id`` hanya menampilkan partner yang merupakan anggota perpustakaan (`is_library_member = True`).

- Status digunakan untuk membedakan buku yang sedang dipinjam dan sudah dikembalikan.

Pastikan file ini di-*import* di ``models/__init__.py``:

.. code-block:: python

   from . import models
   from . import res_partner
   from . import library_loan

--------------------------------------
📗 Penyesuaian Model: library.book
--------------------------------------

Tambahkan kolom stok dan relasi transaksi pada model ``library.book`` di file ``models/models.py``:

.. code-block:: python

       # Kolom stok
       initial_stock = fields.Integer("Stok Awal", default=1)
       borrowed_qty = fields.Integer("Jumlah Dipinjam", compute="_compute_stock", store=True)
       available_qty = fields.Integer("Stok Tersedia", compute="_compute_stock", store=True)
       available = fields.Boolean("Tersedia", compute="_compute_stock", store=True)

       # Relasi ke transaksi
       loan_ids = fields.One2many('library.loan', 'book_id', string="Transaksi Peminjaman")

       @api.depends('initial_stock', 'loan_ids.state')
       def _compute_stock(self):
           for rec in self:
               active_loans = rec.loan_ids.filtered(lambda l: l.state == 'borrowed')
               rec.borrowed_qty = len(active_loans)
               rec.available_qty = rec.initial_stock - rec.borrowed_qty
               rec.available = rec.available_qty > 0

Tambahkan juga kolom baru di view form ``library.book`` pada file ``views/library_book_views.xml``:

.. code-block:: xml

   <field name="initial_stock"/>
   <field name="borrowed_qty" readonly="1"/>
   <field name="available_qty" readonly="1"/>
   <field name="available" readonly="1"/>
   <field name="loan_ids" widget="one2many_list" readonly="1"/>


💡 **Penjelasan:**
- ``loan_ids`` menghubungkan buku ke semua transaksi peminjamannya.
- ``@api.depends('loan_ids.state')`` memastikan stok diperbarui saat status pinjaman berubah.
- ``available`` otomatis berubah ke False bila stok habis.

--------------------------------------
📄 View dan Menu untuk library.loan
--------------------------------------

Buat file baru ``views/library_loan_views.xml`` agar model baru dapat diakses dari UI.

.. code-block:: xml

    <odoo>
       <!-- List View -->
       <record id="view_library_loan_list" model="ir.ui.view">
           <field name="name">library.loan.list</field>
           <field name="model">library.loan</field>
           <field name="arch" type="xml">
               <list string="Daftar Peminjaman">
                   <field name="borrower_id"/>
                   <field name="book_id"/>
                   <field name="borrow_date"/>
                   <field name="return_date"/>
                   <field name="state"/>
               </list>
           </field>
       </record>

       <!-- Form View -->
       <record id="view_library_loan_form" model="ir.ui.view">
           <field name="name">library.loan.form</field>
           <field name="model">library.loan</field>
           <field name="arch" type="xml">
               <form string="Data Peminjaman">
                   <sheet>
                       <group>
                           <field name="borrower_id" domain="[('is_library_member','=',True)]"/>
                           <field name="book_id"/>
                           <field name="borrow_date"/>
                           <field name="return_date"/>
                           <field name="state"/>
                       </group>
                   </sheet>
               </form>
           </field>
       </record>

       <!-- Action Window -->
       <record id="action_library_loan" model="ir.actions.act_window">
           <field name="name">Transaksi Peminjaman</field>
           <field name="res_model">library.loan</field>
           <field name="view_mode">list,form</field>
       </record>

       <!-- Hubungkan views ke action -->
       <record id="action_library_loan_list_view" model="ir.actions.act_window.view">
           <field name="sequence" eval="1"/>
           <field name="view_mode">list</field>
           <field name="view_id" ref="view_library_loan_list"/>
           <field name="act_window_id" ref="action_library_loan"/>
       </record>

       <record id="action_library_loan_form_view" model="ir.actions.act_window.view">
           <field name="sequence" eval="2"/>
           <field name="view_mode">form</field>
           <field name="view_id" ref="view_library_loan_form"/>
           <field name="act_window_id" ref="action_library_loan"/>
       </record>

       <!-- Menu Item -->
       <menuitem id="menu_library_loan"
                 name="Transaksi Peminjaman"
                 parent="menu_library_root"
                 action="action_library_loan"
                 sequence="20"/>
    </odoo>

----------------------------------------------------------------------------------------
🧩 Berikan access right untuk model ``library.loan`` dan Registrasi view nya di Manifest
----------------------------------------------------------------------------------------

Tambahkan akses di file ``security/ir.model.access.csv``:

.. code-block:: text

   access_library_loan_user,access_library_loan_user,model_library_loan,base.group_user,1,1,1,1


Tambahkan file view baru ke dalam ``__manifest__.py``:

.. code-block:: python

   'data': [
        'data/fahriza_latihan_data.xml',
        'security/ir.model.access.csv',
        'views/library_book_views.xml',
        'views/library_category_views.xml',
        'views/library_author_views.xml',
        'views/res_partner_views.xml',
        'views/library_loan_views.xml',
    ],

💡 **Setelah restart Odoo dan upgrade modul:**
Menu baru “**Perpustakaan → Transaksi Peminjaman**” akan muncul dan menampilkan daftar transaksi peminjaman buku.

--------------------------------------
✅ Setelah Preparation
--------------------------------------

Kini kita sudah memiliki model transaksi peminjaman buku yang terhubung dengan model buku.
Selanjutnya, kita akan mempelajari bagaimana **field computed dan constraint**
mengontrol hubungan data antar model ini.

--------------------------------------
6. Computed Fields and Default Values
--------------------------------------

6.1. Computed Fields dan Dependencies
=====================================

Field ``borrowed_qty``, ``available_qty`` dan ``available`` pada model ``library.book``  
adalah contoh nyata dari **computed fields**.

Mereka menghitung jumlah pinjaman aktif dan stok yang tersisa secara otomatis berdasarkan transaksi.

**Penjelasan:**

- ``@api.depends('loan_ids.state')`` → Odoo tahu kapan field perlu dihitung ulang.

- ``store=True`` → hasil perhitungan disimpan di database untuk performa pencarian dan filter.

- ``available`` menjadi nilai logis yang mudah dipakai di view (True/False).

💡 **Latihan:**  
Tambahkan satu record buku dengan stok awal 3, lalu buat 2 transaksi pinjam.  
Perhatikan bahwa kolom “Jumlah Dipinjam” dan “Stok Tersedia” otomatis terhitung.


6.2. Default Values
===================

Field di Odoo dapat memiliki **nilai default** menggunakan parameter ``default``. Default bisa bersifat **statis** atau **dinamis** (menggunakan method Python).

Contoh penerapan pada modul ``fahriza_latihan``:

**Contoh 1 — Default Statis (langsung)**

Default statis untuk stok awal buku pada model ``library.book``:

.. code-block:: python

    initial_stock = fields.Integer(
        string="Stok Awal",
        default=1
    )

**Contoh 2 — Default Dinamis (best practice)**

Default tanggal pinjam dan tanggal kembali pada model ``library.loan``.  
Method default ditulis **di atas field** agar Python mengenal nama method saat field didefinisikan.

.. code-block:: python

    from datetime import date, timedelta
    from odoo import models, fields, api

    class LibraryLoan(models.Model):
        _name = 'library.loan'
        _description = 'Transaksi Peminjaman Buku'

        # Method default di atas field
        @api.model
        def _default_borrow_date(self):
            """Tanggal pinjam otomatis diisi dengan tanggal hari ini."""
            return date.today()

        @api.model
        def _default_return_date(self):
            """Tanggal kembali otomatis tergantung hari pinjam."""
            today = date.today()
            # Jika pinjam hari Jumat, default kembali 3 hari kemudian (Senin)
            if today.weekday() == 4:  # 0=Senin, 4=Jumat
                return today + timedelta(days=3)
            # Hari lain, default kembali besok
            return today + timedelta(days=1)

        # Field dengan default method
        borrow_date = fields.Date(
            string="Tanggal Pinjam",
            default=_default_borrow_date,
            required=True
        )
        return_date = fields.Date(
            string="Tanggal Kembali",
            default=_default_return_date
        )

💡 **Catatan Penting**

- Default **statis**: angka, string literal, boolean → tulis langsung (`default=1`, `default="teks"`, `default=True`).  

- Default **dinamis (method)**: tulis **tanpa tanda kutip** dan **pastikan method didefinisikan sebelum field**.  

💡 **Latihan**

1. Update kolom ``borrow_date`` dan ``return_date`` di view form ``library.loan`` agar menampilkan tanggal default.  

2. Buat transaksi pinjam baru dan perhatikan tanggal otomatis terisi sesuai logika di atas.


--------------------------------------
7. Model Constraints
--------------------------------------

Constraints digunakan untuk **menjaga konsistensi data** di level model maupun database.  
Ada dua jenis utama constraint di Odoo:

1. **Python Constraints** → validasi logika menggunakan decorator ``@api.constrains``  
2. **SQL Constraints** → validasi langsung di level database PostgreSQL melalui atribut ``_sql_constraints``


7.1. Python Constraints
=====================================

Python constraint dijalankan setiap kali data disimpan (``create`` atau ``write``).  
Biasanya digunakan untuk memeriksa logika bisnis yang kompleks dan melibatkan relasi antar record.

**Contoh:** Batasi agar satu anggota hanya bisa meminjam maksimal 2 buku sekaligus. Tambahkan method berikut di model ``library.loan``:

.. code-block:: python

    @api.constrains('borrower_id', 'state')
    def _check_max_borrow_limit(self):
        """Pastikan anggota tidak meminjam lebih dari 2 buku aktif."""
        for rec in self:
            if rec.state == 'borrowed' and rec.borrower_id:
                active_loans = self.search([
                    ('borrower_id', '=', rec.borrower_id.id),
                    ('state', '=', 'borrowed'),
                    ('id', '!=', rec.id)
                ])
                if len(active_loans) >= 2:
                    raise ValidationError(
                        f"Anggota '{rec.borrower_id.name}' sudah memiliki 2 buku yang belum dikembalikan!"
                    )

💡 **Penjelasan:**

- Constraint ini berjalan setiap kali transaksi pinjaman disimpan.

- Mengecek apakah peminjam (`borrower_id`) sudah punya 2 transaksi aktif (`state='borrowed'`).

- Jika iya → proses ditolak dengan pesan error.

💡 **Latihan untuk peserta:**

- Buat satu anggota dan pinjam 2 buku (state = *Dipinjam*).  

- Coba pinjam buku ketiga → sistem akan menolak dengan pesan error.


7.2. SQL Constraints
=====================================

SQL constraint dijalankan di level database PostgreSQL.  
Biasanya digunakan untuk aturan sederhana seperti *unique*, *check*, atau *not null*.

**Contoh:** Tambahkan SQL constraint pada model ``library.book`` untuk memastikan ISBN unik dan harga tidak negatif:

.. code-block:: python

    _sql_constraints = [
        ('unique_isbn', 'unique(isbn)', 'Nomor ISBN harus unik!'),
        ('check_price_positive', 'CHECK(price >= 0)', 'Harga tidak boleh negatif!')
    ]


💡 **Kapan digunakan:**

- Jika validasi bisa dilakukan langsung oleh PostgreSQL (lebih cepat dan efisien).

- Cocok untuk validasi sederhana dan statis seperti keunikan, batas angka, atau ekspresi logis tunggal.


7.3. Perbandingan Python vs SQL Constraints
===========================================

+----------------------+----------------------------------------------+--------------------------------------------+
| **Aspek**            | **Python Constraint**                        | **SQL Constraint**                         |
+======================+==============================================+============================================+
| Lokasi Eksekusi      | Di level Odoo (Python)                       | Di level PostgreSQL                        |
+----------------------+----------------------------------------------+--------------------------------------------+
| Fleksibilitas        | Sangat fleksibel, bisa gunakan logika        | Terbatas pada ekspresi SQL sederhana       |
|                      | kompleks dan relasi antar model              |                                            |
+----------------------+----------------------------------------------+--------------------------------------------+
| Performa             | Lebih lambat (tergantung kode)               | Sangat cepat                               |
+----------------------+----------------------------------------------+--------------------------------------------+
| Akses Relasi         | Bisa akses relasi seperti Many2one, One2many | Tidak bisa akses relasi                    |
+----------------------+----------------------------------------------+--------------------------------------------+
| Waktu Eksekusi       | Setelah data dibuat atau diubah              | Saat INSERT/UPDATE di database             |
+----------------------+----------------------------------------------+--------------------------------------------+

💡 **Best Practice:**  
Gunakan SQL constraint untuk validasi sederhana dan statis,  
dan Python constraint untuk validasi dinamis atau yang melibatkan relasi antar record.


--------------------------------------
8. Advanced Views
--------------------------------------

Di bagian ini kita akan membuat tampilan **list view** dan **search view** yang lebih cerdas untuk modul library.  
“Advanced” di sini berarti kita menggunakan **domain, context, filter, group by, dan prioritas view** untuk meningkatkan UX.

8.1. List Views
=====================================

Selain membuat tampilan untuk model buku, kita juga bisa menampilkan **anggota perpustakaan**
dengan tampilan khusus yang berbeda dari kontak umum.


8.1.1. Daftar Anggota Perpustakaan
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Berikut contoh tampilan daftar anggota (`res.partner`) yang hanya menampilkan
kontak dengan ``is_library_member=True``.

.. code-block:: xml

    <odoo>
    <!-- View List untuk Anggota Perpustakaan -->
    <record id="view_library_member_list" model="ir.ui.view">
        <field name="name">library.member.list</field>
        <field name="model">res.partner</field>
        <field name="arch" type="xml">
            <list string="Daftar Anggota Perpustakaan">
                <field name="name"/>
                <field name="mobile"/>
                <field name="email"/>
            </list>
        </field>
    </record>

    <!-- View Form sederhana -->
    <record id="view_library_member_form" model="ir.ui.view">
        <field name="name">library.member.form</field>
        <field name="model">res.partner</field>
        <field name="arch" type="xml">
            <form string="Anggota Perpustakaan">
                <sheet>
                    <group>
                        <field name="name"/>
                        <field name="mobile"/>
                        <field name="email"/>
                        <field name="is_library_member" invisible="1"/>
                    </group>
                </sheet>
            </form>
        </field>
    </record>

    <!-- Action Window -->
    <record id="action_library_member" model="ir.actions.act_window">
        <field name="name">Anggota Perpustakaan</field>
        <field name="res_model">res.partner</field>
        <field name="domain">[('is_library_member', '=', True)]</field>
        <field name="view_mode">list,form</field>
        <field name="context">{'default_is_library_member': True}</field>
    </record>

    <!-- Hubungkan view list & form ke action -->
    <record id="action_library_member_view_list" model="ir.actions.act_window.view">
        <field name="sequence" eval="101"/>
        <field name="view_mode">list</field>
        <field name="view_id" ref="view_library_member_list"/>
        <field name="act_window_id" ref="action_library_member"/>
    </record>

    <record id="action_library_member_view_form" model="ir.actions.act_window.view">
        <field name="sequence" eval="102"/>
        <field name="view_mode">form</field>
        <field name="view_id" ref="view_library_member_form"/>
        <field name="act_window_id" ref="action_library_member"/>
    </record>

    <!-- Menu -->
    <menuitem id="menu_library_member"
                name="Anggota Perpustakaan"
                parent="menu_library_root"
                action="action_library_member"
                sequence="30"/>
    </odoo>

💡 **Penjelasan:**

- Record `ir.actions.act_window.view` digunakan agar action tahu view mana yang diprioritaskan (list → form).

- Domain memastikan hanya anggota perpustakaan yang muncul.

- Context membuat anggota baru otomatis diset `is_library_member=True`.


💡 **Latihan:**

1. Buat file view baru di ``views/library_member_views.xml`` dengan kode di atas.

2. Tambahkan file view ke ``__manifest__.py``.

3. Restart Odoo dan upgrade modul.

4. Coba akses menu baru “**Perpustakaan → Anggota Perpustakaan**” dan buat anggota baru.

8.2. Search Views
=====================================

di Day 1 kita sudah membuat search view sederhana untuk model buku.
Sekarang kita akan menambahkan fitur **filter** dan **group by** pada search view tersebut.
Sebelum itu, pastikan kita sudah memiliki field computed `available` di model `library.book` dan 
menampulkan field tersebut di list view.

**Contoh:** menambahkan filter dan pengelompokan untuk model ``library.book`` di search view ``view_library_book_search``

.. code-block:: xml


        <filter string="Tersedia" domain="[('available', '=', True)]"/>
        <filter string="Stok Habis" domain="[('available', '=', False)]"/>
        <group expand="0" string="Group By">
            <filter string="Kategori" context="{'group_by': 'category_id'}"/>
        </group>


💡 **Penjelasan:**

- `<filter>` menambah tombol cepat untuk menyaring data.

- `<group>` memungkinkan pengguna mengelompokkan daftar berdasarkan field tertentu.

- Fitur ini umum digunakan untuk meningkatkan UX di list view besar.

💡 **Latihan:**

1. Tambahkan kode di atas ke search view ``view_library_book_search`` di file ``views/library_book_views.xml``.

2. Restart Odoo dan upgrade modul.

3. Coba akses menu “**Perpustakaan → Buku**” dan gunakan filter serta group by di search view.


--------------------------------------
9. Security
--------------------------------------

Untuk menjaga keamanan dan isolasi data dalam Odoo, sistem menyediakan beberapa mekanisme kontrol akses.  
Dokumentasi ini membahas tiga lapisan utama: *Groups*, *Access Rights*, dan *Record Rules*.  
Masing-masing lapisan bekerja bersama untuk membatasi apa yang dapat dilakukan pengguna terhadap data.

9.1 Groups (Grup)
=================
- Grup (group) adalah cara untuk mengelompokkan pengguna (users) ke dalam peran tertentu (role).  
- Pengguna dapat menjadi anggota dari satu atau beberapa grup.  
- Grup menentukan hak macros (misalnya: “Administrator”, “Sales / User”, “Portal”, dll).  
- Dalam modul keamanan, grup biasanya ditentukan di file XML dengan tag `<group ...>`.

Contoh Groups untuk Model ``library.loan``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Kita akan membuat tiga grup utama yang akan digunakan untuk mengatur hak akses pada model ``library.loan``:

1. **Library Super Admin** – memiliki semua hak penuh terhadap data pinjaman.
2. **Library Admin** – dapat membuat, membaca, dan mengubah transaksi peminjaman.
3. **Library Member** – hanya dapat melihat data peminjamannya sendiri (akan dibatasi melalui record rule nanti).

Pertama, kita buat **kategori grup khusus** untuk modul ini, kemudian definisikan grup-grupnya:

.. code-block:: xml

   <odoo>
       <!-- Kategori Grup Perpustakaan -->
       <record id="module_category_library_management" model="ir.module.category">
           <field name="name">Library Management</field>
           <field name="sequence">10</field>
           <field name="description">Kategori untuk grup dan keamanan modul perpustakaan</field>
       </record>

       <!-- Member -->
       <record id="group_library_member" model="res.groups">
           <field name="name">Library Member</field>
           <field name="category_id" ref="module_category_library_management"/>
       </record>

       <!-- Admin -->
       <record id="group_library_admin" model="res.groups">
           <field name="name">Library Admin</field>
           <field name="implied_ids" eval="[(4, ref('group_library_member'))]"/>
           <field name="category_id" ref="module_category_library_management"/>
       </record>

       <!-- Super Admin -->
       <record id="group_library_super_admin" model="res.groups">
           <field name="name">Library Super Admin</field>
           <field name="category_id" ref="module_category_library_management"/>
       </record>
   </odoo>

Simpan kode di atas dalam file XML baru, misalnya ``security/library_groups.xml``,
dan daftarkan file ini di ``__manifest__.py``.



💡 **Penjelasan:**

- Kategori `Library Management` membuat grup-grup ini tampil di bagian khusus pada *Settings → Users & Companies → Groups*.
- Grup **Library Admin** mewarisi hak dari **Library Member** melalui atribut `implied_ids`.
- Nantinya, grup-grup ini akan digunakan di file `security/ir.model.access.csv` dan `ir.rule` untuk menentukan siapa yang bisa mengakses model `library.loan`.


9.2 Access Rights (Hak Akses)
=========================
- Access Rights diterapkan pada level *model* (model-level).  
- Mereka menentukan apakah anggota grup boleh melakukan operasi CRUD dasar terhadap model tersebut:  
  - **create** (membuat),  
  - **read** (membaca),  
  - **write** (menulis / mengubah),  
  - **unlink** (menghapus).  
- Akses ini bersifat global terhadap semua record di model kecuali dicegah lebih lanjut oleh *Record Rules*.  

Contoh Access Rights untuk Model ``library.loan``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Setelah membuat tiga grup (Super Admin, Admin, dan Member), kita perlu menentukan hak akses (CRUD) untuk masing-masing grup terhadap model ``library.loan``.

Buka atau buat file baru ``security/ir.model.access.csv`` dan tambahkan baris berikut:

.. code-block:: text

   access_library_loan_super_admin,access.library.loan.super.admin,model_library_loan,fahriza_latihan.group_library_super_admin,1,1,1,1
   access_library_loan_admin,access.library.loan.admin,model_library_loan,fahriza_latihan.group_library_admin,1,1,1,0
   access_library_loan_member,access.library.loan.member,model_library_loan,fahriza_latihan.group_library_member,1,0,0,0

💡 **Penjelasan:**

- **Super Admin**: punya akses penuh (baca, tulis, buat, hapus).
- **Admin**: boleh membaca, menulis, dan membuat transaksi, tetapi **tidak bisa menghapus**.
- **Member**: hanya boleh **melihat** (read-only) data pinjaman.
- Pastikan nama grup (`fahriza_latihan.group_library_admin`, dll.) sesuai dengan XML ID grup yang kamu definisikan di file ``library_groups.xml``.
- Pastikan file ``security/ir.model.access.csv`` sudah direferensikan di `__manifest__.py`:


💡 **Tips:**

- Kamu bisa menambahkan akses tambahan untuk model lain seperti `library.book` atau `library.category` dengan pola yang sama.
- Setelah file disimpan, **restart Odoo dan upgrade modul** agar perubahan diterapkan.


9.3 Record Rules (Aturan Rekaman)
==========================
- Record Rules bekerja pada level record (baris data) dan bersifat lebih spesifik daripada Access Rights.  
- Mereka mengevaluasi domain (kondisi) untuk menentukan record mana saja yang boleh diakses (read/write/unlink/create) oleh pengguna.  
- Sebuah Record Rule didefinisikan dengan:  
  - model terkait,  
  - domain (ekspresi pencarian, e.g. `[('company_id','=',user.company_id)]`),  
  - grup (opsional) agar aturan hanya berlaku untuk grup tertentu,  
  - jenis akses (mode: read, write, unlink, create).  
- Beberapa aturan bisa digabung (OR / AND) sesuai kebutuhan.  
- Jika seorang pengguna tidak memenuhi domain dari Record Rule-nya, maka akses terhadap record tersebut ditolak.

Contoh Record Rules untuk Model ``library.loan``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Setelah menetapkan hak akses di ``ir.model.access.csv``, kita tambahkan **aturan rekaman (record rules)** untuk membatasi data yang dapat dilihat oleh masing-masing grup.

Buat file baru bernama ``security/library_record_rules.xml`` dan tambahkan kode berikut:

.. code-block:: xml

   <odoo>
       <!-- 1. Super Admin: akses penuh ke semua record -->
       <record id="rule_library_loan_super_admin" model="ir.rule">
           <field name="name">Library Loan: Super Admin full access</field>
           <field name="model_id" ref="model_library_loan"/>
           <field name="domain_force">[(1, '=', 1)]</field>
           <field name="groups" eval="[(4, ref('fahriza_latihan.group_library_super_admin'))]"/>
           <field name="perm_read" eval="1"/>
           <field name="perm_write" eval="1"/>
           <field name="perm_create" eval="1"/>
           <field name="perm_unlink" eval="1"/>
       </record>

       <!-- 2. Admin: akses ke semua transaksi -->
       <record id="rule_library_loan_admin" model="ir.rule">
           <field name="name">Library Loan: Admin access all</field>
           <field name="model_id" ref="model_library_loan"/>
           <field name="domain_force">[(1, '=', 1)]</field>
           <field name="groups" eval="[(4, ref('fahriza_latihan.group_library_admin'))]"/>
           <field name="perm_read" eval="1"/>
           <field name="perm_write" eval="1"/>
           <field name="perm_create" eval="1"/>
           <field name="perm_unlink" eval="0"/>
       </record>

       <!-- 3. Member: hanya bisa melihat record miliknya sendiri -->
       <record id="rule_library_loan_member" model="ir.rule">
           <field name="name">Library Loan: Member own records only</field>
           <field name="model_id" ref="model_library_loan"/>
           <field name="domain_force">[('borrower_id.user_id', '=', user.id)]</field>
           <field name="groups" eval="[(4, ref('fahriza_latihan.group_library_member'))]"/>
           <field name="perm_read" eval="1"/>
           <field name="perm_write" eval="0"/>
           <field name="perm_create" eval="0"/>
           <field name="perm_unlink" eval="0"/>
       </record>
   </odoo>

💡 **Penjelasan:**

- **Super Admin**: bisa melihat dan mengelola semua transaksi tanpa batas.
- **Admin**: bisa melihat dan mengedit semua transaksi, tapi tidak bisa menghapus.
- **Member**: hanya bisa melihat transaksi peminjaman **yang dibuat atas nama dirinya sendiri**, berdasarkan relasi antara `borrower_id.user_id` dan `user.id`.

💡 **Tips Tambahan**

- Pastikan setiap anggota (`res.partner`) yang merupakan anggota perpustakaan (`is_library_member=True`) memiliki user terkait (`user_id`), agar rule `borrower_id.user_id = user.id` berfungsi dengan benar.

Tambahkan file baru ini di bagian `data` manifest:
Setelah itu, **restart Odoo dan upgrade modul** untuk menerapkan aturan keamanan baru ini.


9.4 Security Override (Override Keamanan)
=======================================
- Ada skenario di mana batasan default harus dilanggar (override) — contohnya dalam operasi internal, migrasi data, atau kebutuhan teknis khusus.  
- Di dalam kode Python, dapat menggunakan **`sudo()`** untuk menjalankan operasi tanpa batasan hak akses pengguna.  
- Namun, penggunaan `sudo()` harus sangat hati-hati karena bisa melewati semua aturan keamanan.  
- Odoo juga menyediakan metode seperti `check_access(write)` untuk memeriksa hak akses secara programatis.

💡 Visibility != Security (Visibilitas ≠ Keamanan)
=================================================
- Penting dipahami: hanya karena suatu record **tidak muncul** di antarmuka (UI), bukan berarti pengguna tidak bisa mengaksesnya lewat API / RPC / kode.  
- Mekanisme keamanan (Access Rights + Record Rules) tetap menjadi filter terakhir terhadap akses data.  
- UI bisa menyembunyikan opsi (button, menu) tetapi tidak menggantikan aturan keamanan.


Referensi
~~~~~~~~~~~~~~~~~~~~~~~~~
- Dokumentasi Odoo: https://www.odoo.com/documentation/18.0/id/developer/tutorials/restrict_data_access.html#access-rights  



--------------------------------------
10. Wizards
--------------------------------------

Wizard digunakan untuk memandu pengguna melalui proses interaktif beberapa langkah.  
Dalam modul perpustakaan, kita akan membuat **wizard peminjaman buku** yang dipanggil dari tombol di model ``library.book``.

Tujuannya:  

- Saat admin atau member klik tombol **"Pinjam Buku"**, akan muncul wizard.
- Wizard akan meminta nama peminjam dan tanggal pinjam.
- Setelah dikonfirmasi, sistem otomatis membuat record baru di model ``library.loan``.


10.1 Method Pemanggil Wizard di ``library.book``
================================================

Tambahkan method berikut di model ``library.book``:

.. code-block:: python

   from odoo import models, fields, api

   class LibraryBook(models.Model):
       _inherit = 'library.book'

       def action_borrow_book(self):
           """Buka wizard peminjaman buku."""
           return {
               'type': 'ir.actions.act_window',
               'name': 'Pinjam Buku',
               'res_model': 'library.borrow.wizard',
               'view_mode': 'form',
               'target': 'new',
               'context': {
                   'default_book_id': self.id,
               }
           }

💡 **Penjelasan:**

- Method ini mengembalikan action tipe `ir.actions.act_window` yang membuka tampilan *popup form (target='new')*.
- Field `context` digunakan untuk mengisi nilai default buku yang akan dipinjam.

Tambahkan juga tombol untuk menjalankan wizard di form view buku:

.. code-block:: xml

   <button name="action_borrow_book"
           string="Pinjam Buku"
           type="object"
           class="btn-primary"
           attrs="{'invisible': [('available', '=', False)]}"/>

💡 Tombol ini hanya muncul jika buku masih tersedia (`available=True`).


10.2 Membuat Model Wizard: ``library.borrow.wizard``
===============================================================

Buat file baru ``wizard/library_borrow_wizard.py``:

.. code-block:: python

   from odoo import models, fields, api
   from datetime import date

   class LibraryBorrowWizard(models.TransientModel):
       _name = 'library.borrow.wizard'
       _description = 'Wizard Peminjaman Buku'

       borrower_id = fields.Many2one(
           'res.partner',
           string="Peminjam",
           domain=[('is_library_member', '=', True)],
           required=True
       )
       book_id = fields.Many2one('library.book', string="Buku", required=True, readonly=True)
       borrow_date = fields.Date(string="Tanggal Pinjam", default=lambda self: date.today())

       def action_confirm(self):
           """Buat record peminjaman baru di library.loan"""
           self.env['library.loan'].create({
               'borrower_id': self.borrower_id.id,
               'book_id': self.book_id.id,
               'borrow_date': self.borrow_date,
               'state': 'borrowed',
           })
           return {'type': 'ir.actions.act_window_close'}

💡 **Penjelasan:**

- Model wizard menggunakan `TransientModel` karena datanya bersifat sementara.
- Saat tombol konfirmasi ditekan, wizard otomatis membuat transaksi baru di `library.loan`.
- Setelah selesai, wizard akan menutup dirinya (`act_window_close`).


10.3 View Wizard
===============================================

Buat file baru ``views/library_borrow_wizard_views.xml``:

.. code-block:: xml

   <odoo>
       <record id="view_library_borrow_wizard_form" model="ir.ui.view">
           <field name="name">library.borrow.wizard.form</field>
           <field name="model">library.borrow.wizard</field>
           <field name="arch" type="xml">
               <form string="Peminjaman Buku">
                   <group>
                       <field name="book_id"/>
                       <field name="borrower_id"/>
                       <field name="borrow_date"/>
                   </group>
                   <footer>
                       <button string="Konfirmasi" name="action_confirm" type="object" class="btn-primary"/>
                       <button string="Batal" class="btn-secondary" special="cancel"/>
                   </footer>
               </form>
           </field>
       </record>
   </odoo>

💡 **Penjelasan:**
- Wizard hanya menampilkan field penting: buku, peminjam, dan tanggal pinjam.
- Tombol “Konfirmasi” menjalankan method `action_confirm`.
- Tombol “Batal” menutup wizard tanpa menyimpan data.


10.3.1. Daftarkan Wizard di Manifest
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pastikan file wizard dan view-nya sudah terdaftar di ``__manifest__.py``:

.. code-block:: python

   'data': [
       'security/library_groups.xml',
       'security/ir.model.access.csv',
       'security/library_record_rules.xml',
       'views/library_book_views.xml',
       'views/library_loan_views.xml',
       'wizard/library_borrow_wizard_views.xml',
   ],
   'demo': [],
   'installable': True,
   'application': True,

Dan di dalam folder ``wizard/__init__.py`` tambahkan:

.. code-block:: python

   from . import library_borrow_wizard

10.3.2 Tambahkan access right untuk wizard
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Tambahkan akses di file ``security/ir.model.access.csv``:

.. code-block:: text

   access_library_borrow_wizard_user,access.library.borrow.wizard.user,model_library_borrow_wizard,base.group_user,1,1,1,1


💡 Hasil Akhir
===============

1. Buka menu **Perpustakaan → Buku**.  
2. Pilih salah satu buku yang masih tersedia.  
3. Klik tombol **"Pinjam Buku"**, wizard akan muncul.  
4. Isi nama anggota dan tanggal pinjam, lalu tekan **Konfirmasi**.  
5. Record baru otomatis muncul di menu **Transaksi Peminjaman** (`library.loan`).

Dengan wizard ini, proses peminjaman buku menjadi lebih cepat, terkontrol, dan user-friendly.
