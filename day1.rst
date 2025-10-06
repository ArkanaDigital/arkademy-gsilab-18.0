======================================
🧩 Arkademy GSI Lab 18.0 - Day 1
======================================

**Topik:** Development Basic Odoo 18 CE  
**Durasi:** 09.00 – 17.00 WIB  
**Versi:** Odoo 18.0 Community Edition

--------------------------------------
🎯 Tujuan Pembelajaran
--------------------------------------

Pada akhir sesi hari pertama, peserta akan mampu:

- Membuat modul Odoo menggunakan perintah ``scaffold``.
- Memahami struktur dan komposisi modul Odoo.
- Membuat model dan field dasar menggunakan ORM.
- Menampilkan data melalui view (list, form, search).
- Menambahkan menu dan action di UI.
- Mengenal dasar inheritance model dan view.

--------------------------------------
2. Build an Odoo Module
--------------------------------------

2.1. Membuat Modul dengan Scaffold
==================================

Odoo menyediakan perintah ``scaffold`` untuk membuat struktur modul secara otomatis.  
Perintah ini sangat berguna untuk memulai latihan dasar development.

**Langkah-langkah:**

1. Pastikan Odoo Anda dapat dijalankan dari terminal:

   .. code-block:: bash

      ./odoo-bin --version

2. Arahkan ke folder repository custom Anda. Contoh:

   .. code-block:: bash

      cd ~/Workspace/training/latihan

3. Jalankan perintah scaffold:

   .. code-block:: bash

      ./odoo-bin scaffold namadepan_library .

   Contoh (jika nama depan Anda adalah Fahriza):

   .. code-block:: bash

      ./odoo-bin scaffold fahriza_library .

4. Setelah berhasil, akan muncul folder baru:

   .. code-block::

      fahriza_library/


2.2. Komposisi dan Struktur Modul
==================================

Setelah menjalankan perintah scaffold, Odoo otomatis membuat struktur dasar seperti berikut:

.. code-block::

   fahriza_library/
   ├── __manifest__.py          → Metadata modul (nama, versi, dependensi, dsb)
   ├── __init__.py              → Inisialisasi package Python
   │
   ├── controllers/             → Berisi controller HTTP (opsional)
   │   ├── __init__.py
   │   └── controllers.py
   │
   ├── demo/                    → Berisi data contoh (demo data)
   │   └── demo.xml
   │
   ├── models/                  → Definisi model dan field (ORM)
   │   ├── __init__.py
   │   └── models.py
   │
   ├── security/                → Hak akses pengguna
   │   └── ir.model.access.csv
   │
   └── views/                   → Tampilan (form, list, search)
       ├── templates.xml
       ├── views.xml
       └── __init__.py

💡 **Latihan:**  
Buka file ``__manifest__.py`` dan ubah bagian:
- ``'name'`` menjadi **"Fahriza Library"**
- ``'summary'`` menjadi **"Modul Latihan Perpustakaan Dasar"**
Kemudian restart Odoo dan update Apps List untuk melihat modul di daftar aplikasi.


2.3. Object-Relational Mapping (ORM)
==================================

ORM (*Object-Relational Mapping*) adalah **jembatan antara class Python dan tabel database**.  
Setiap *model* yang kita buat di Python akan otomatis diterjemahkan oleh Odoo menjadi tabel di PostgreSQL.

Dengan ORM, kita tidak perlu menulis perintah SQL secara manual seperti
``CREATE TABLE``, ``INSERT``, ``UPDATE``, atau ``DELETE``.
Cukup dengan mendeklarasikan class dan field, Odoo akan:

- Membuat tabel baru di database.
- Membuat kolom sesuai field yang kita definisikan.
- Mengatur relasi antar tabel secara otomatis.
- Menyediakan fungsi CRUD (Create, Read, Update, Delete) yang bisa langsung dipakai di Python.


🔍 Perbandingan ORM vs SQL Langsung
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

+------------------+---------------------------------------------+----------------------------------------------------------+
| **Aksi**         | **SQL Manual (PostgreSQL)**                 | **ORM (Odoo)**                                           |
+==================+=============================================+==========================================================+
| Membuat tabel    | ``CREATE TABLE library_book (id SERIAL      | ``_name = 'library.book'`` dan                           |
|                  | PRIMARY KEY, name VARCHAR, author VARCHAR);``| ``name = fields.Char()``                                 |
+------------------+---------------------------------------------+----------------------------------------------------------+
| Menambah data    | ``INSERT INTO library_book (name, author)   | ``self.env['library.book'].create({'name': 'Belajar      |
|                  | VALUES ('Belajar Odoo', 'Fahriza');``       | Odoo', 'author': 'Fahriza'})``                          |
+------------------+---------------------------------------------+----------------------------------------------------------+
| Membaca data     | ``SELECT * FROM library_book WHERE          | ``self.env['library.book'].search([('author','=','Fahriza')])`` |
|                  | author='Fahriza';``                         |                                                          |
+------------------+---------------------------------------------+----------------------------------------------------------+
| Mengubah data    | ``UPDATE library_book SET price=120000      | ``book.write({'price':120000})``                         |
|                  | WHERE id=1;``                               |                                                          |
+------------------+---------------------------------------------+----------------------------------------------------------+
| Menghapus data   | ``DELETE FROM library_book WHERE id=1;``    | ``book.unlink()``                                        |
+------------------+---------------------------------------------+----------------------------------------------------------+

Dengan ORM, kode menjadi:

- **Lebih ringkas** dan mudah dibaca.

- **Lebih aman**, karena terhindar dari SQL Injection.

- **Terintegrasi penuh** dengan hak akses, log aktivitas, dan constraint Odoo.

- **Lebih mudah di-*upgrade*** karena perubahan field langsung ditangani oleh sistem Odoo.


📘 Contoh Model Utama: ``library.book``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from odoo import models, fields, api

   class LibraryBook(models.Model):
       _name = 'library.book'
       _description = 'Data Buku Perpustakaan'

       name = fields.Char("Judul Buku", required=True)
       isbn = fields.Char("ISBN")
       published_date = fields.Date("Tanggal Terbit")
       price = fields.Float("Harga")
       available = fields.Boolean("Tersedia", default=True)


⚙️ Cara ORM Membuat Tabel di Database
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Ketika modul dipasang (install), Odoo akan:

1. Membaca deklarasi ``_name = 'library.book'``.
2. Membuat tabel baru dengan nama ``library_book`` di PostgreSQL.
3. Menambahkan kolom sesuai field yang didefinisikan.
4. Menambahkan kolom bawaan berikut:

   - ``id`` → Primary Key  
   - ``create_uid`` → User yang membuat record  
   - ``create_date`` → Tanggal record dibuat  
   - ``write_uid`` → User yang terakhir mengubah  
   - ``write_date`` → Tanggal terakhir diubah  

Contoh struktur tabel di PostgreSQL:

+------------------+------------------+----------------------------+
| **Kolom**        | **Tipe Data**    | **Keterangan**             |
+==================+==================+============================+
| id               | integer          | Primary key                |
+------------------+------------------+----------------------------+
| name             | varchar          | Judul buku                 |
+------------------+------------------+----------------------------+
| isbn             | varchar          | Nomor ISBN                 |
+------------------+------------------+----------------------------+
| published_date   | date             | Tanggal terbit             |
+------------------+------------------+----------------------------+
| price            | double precision | Harga buku                 |
+------------------+------------------+----------------------------+
| available        | boolean          | Status ketersediaan buku   |
+------------------+------------------+----------------------------+
| create_uid       | integer          | User pembuat record        |
+------------------+------------------+----------------------------+
| create_date      | timestamp        | Tanggal dibuat             |
+------------------+------------------+----------------------------+
| write_uid        | integer          | User terakhir ubah         |
+------------------+------------------+----------------------------+
| write_date       | timestamp        | Waktu terakhir diubah      |
+------------------+------------------+----------------------------+


🧩 Operasi CRUD dengan ORM
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**1. Create (Tambah Data)**

.. code-block:: python

   self.env['library.book'].create({
       'name': 'Odoo 18 Developer Guide',
       'author': 'Arkana Dev',
       'price': 150000,
       'available': True
   })

**2. Read (Baca Data)**

.. code-block:: python

   books = self.env['library.book'].search([('available', '=', True)])
   for book in books:
       print(book.name, book.author)

**3. Update (Ubah Data)**

.. code-block:: python

   book = self.env['library.book'].browse(1)
   book.write({'price': 175000})

**4. Delete (Hapus Data)**

.. code-block:: python

   book = self.env['library.book'].browse(1)
   book.unlink()


💡 Catatan Tambahan
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ORM Odoo sepenuhnya menggunakan **PostgreSQL** (tidak mendukung MySQL).
- Semua operasi CRUD dijalankan dalam konteks environment ``self.env``.
- Odoo otomatis mengatur **transaksi (transaction)** dan **rollback** jika terjadi error.
- Model ORM juga terhubung dengan fitur keamanan seperti **Access Control List (ACL)** dan **Record Rules**.
- Penambahan field baru akan otomatis membuat kolom baru di tabel tanpa perlu perintah SQL tambahan.


2.4. Model Fields
=======================================

2.4.1. Atribut Umum (Common Attributes)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``string`` → Label tampilan
- ``required`` → Field wajib diisi
- ``default`` → Nilai awal
- ``readonly`` → Tidak dapat diubah
- ``help`` → Keterangan tambahan pada tooltip

2.4.2. Simple Fields
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   name = fields.Char("Judul Buku")
   price = fields.Float("Harga")
   available = fields.Boolean("Tersedia", default=True)
   published_date = fields.Date("Tanggal Terbit")

2.4.3. Reserved Fields
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Field bawaan Odoo yang tersedia di semua model:

- ``id``, ``create_date``, ``write_date``
- ``create_uid``, ``write_uid``
- ``display_name``

2.4.4. Special Fields (Relasional)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Special fields digunakan untuk membuat relasi antar model. 

.. code-block:: python

   category_id = fields.Many2one('library.category', string="Kategori")


2.5. Data Files
=======================================

File XML digunakan untuk menambahkan data awal (initial data) atau konfigurasi.

Data file biasanya disimpan di dalam folder ``data/``.
**Contoh:** ``data/fahriza_library_data.xml``

.. code-block:: xml

   <odoo>
       <data>
           <record id="book_python" model="library.book">
               <field name="name">Python untuk Pemula</field>
               <field name="isbn">ISBN1234567</field>
               <field name="published_date">2023-06-01</field>
               <field name="price">120000</field>
               <field name="available">True</field>
           </record>
       </data>
   </odoo>

Tambahkan file ini ke ``__manifest__.py``:

.. code-block:: python

   'data': [
       'data/fahriza_library_data.xml',
   ],


💡 **Latihan:**  
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1. Buat model ``library.book`` di file ``models/models.py``.

2. Tambahkan field:

   - ``name`` (Char, required)

   - ``isbn`` (Char)

   - ``published_date`` (Date)

   - ``price`` (Float)

   - ``available`` (Boolean, default True)

3. Buat file data XML di ``data/fahriza_library_data.xml`` dan tambahkan 3 record buku.

4. Daftarkan file data di ``__manifest__.py``.

5. Restart Odoo, kemudian install atau upgrade modul ``fahriza_library``.

6. Cek di database PostgreSQL apakah tabel ``library_book`` sudah dibuat dan data sudah masuk.


--------------------------------------
3. Basic Views
--------------------------------------

Setelah model ``library.book`` dibuat, langkah berikutnya adalah menampilkan datanya di antarmuka Odoo.  
Tampilan atau *view* dalam Odoo ditulis menggunakan XML, dan setiap view terhubung ke sebuah model.

Ada beberapa jenis view utama:

- **List View** → menampilkan banyak record dalam bentuk tabel.

- **Form View** → menampilkan detail satu record.

- **Search View** → menyediakan kolom pencarian dan filter.

- **Kanban / Calendar / Pivot** → jenis lanjutan (dibahas di tingkat lanjut).


3.1. Generic View Declaration
=======================================

Setiap view di Odoo dideklarasikan dalam model ``ir.ui.view`` melalui XML.  
Struktur umum deklarasinya seperti berikut:

.. code-block:: xml

   <record id="view_id_unik" model="ir.ui.view">
       <field name="name">nama_view</field>
       <field name="model">nama_model</field>
       <field name="arch" type="xml">
           <!-- struktur tampilan disini -->
       </field>
   </record>

**Penjelasan:**

- ``id`` → identitas unik view.

- ``name`` → nama view (tidak wajib unik, tapi disarankan deskriptif).

- ``model`` → model yang digunakan (contoh: ``library.book``).

- ``arch`` → isi struktur XML dari tampilan (form, list, dsb.).


3.2. List Views
=======================================

List view digunakan untuk menampilkan **daftar data** seperti tabel.  
Biasanya berisi beberapa kolom utama dari model.

.. code-block:: xml

   <record id="view_library_book_list" model="ir.ui.view">
       <field name="name">library.book.list</field>
       <field name="model">library.book</field>
       <field name="arch" type="xml">
           <list string="Daftar Buku">
               <field name="name"/>
               <field name="isbn"/>
               <field name="published_date"/>
               <field name="price"/>
               <field name="available"/>
           </list>
       </field>
   </record>

**Penjelasan:**

- ``list`` → jenis view yang digunakan.

- ``string`` → judul tampilan (akan muncul di UI).

- ``field`` → nama-nama kolom dari model ``library.book`` yang akan ditampilkan.


3.3. Form Views
=======================================

Form view digunakan untuk menampilkan **detail satu record** — digunakan saat membuat atau mengedit data.

.. code-block:: xml

   <record id="view_library_book_form" model="ir.ui.view">
       <field name="name">library.book.form</field>
       <field name="model">library.book</field>
       <field name="arch" type="xml">
           <form string="Data Buku">
               <sheet>
                   <group>
                       <field name="name"/>
                       <field name="published_date"/>
                       <field name="isbn"/>
                       <field name="price"/>
                       <field name="available"/>
                   </group>
               </sheet>
           </form>
       </field>
   </record>

**Penjelasan:**

- ``form`` → jenis view untuk detail satu record.

- ``sheet`` → area utama isi form (secara default punya margin & padding yang rapi).

- ``group`` → mengelompokkan field agar tersusun rapi di dua kolom.


3.4. Search Views
=======================================

Search view digunakan untuk mendefinisikan **kolom pencarian dan filter cepat** di bagian atas List View.

.. code-block:: xml

   <record id="view_library_book_search" model="ir.ui.view">
       <field name="name">library.book.search</field>
       <field name="model">library.book</field>
       <field name="arch" type="xml">
           <search string="Cari Buku">
               <field name="name" string="Judul Buku"/>
               <field name="isbn"/>
           </search>
       </field>
   </record>

**Penjelasan:**

- ``search`` → jenis view untuk pencarian.

- ``field`` → menentukan field mana yang bisa dicari.

- ``filter`` → menambahkan tombol filter cepat dengan domain tertentu.


3.5. Actions dan Menus
=======================================

Agar view dapat diakses dari UI, kita perlu mendefinisikan **Action Window** dan **Menu**.

.. code-block:: xml

    <!-- Menu Root -->
    <menuitem id="menu_library_root" name="Perpustakaan"/>

    <!-- Submenu Buku -->
    <menuitem id="menu_library_book" name="Data Buku" parent="menu_library_root"/>

    <!-- Action Window -->
    <record id="action_library_book" model="ir.actions.act_window">
        <field name="name">Daftar Buku</field>
        <field name="res_model">library.book</field>
        <field name="view_mode">list,form</field>
    </record>

    <!-- Hubungan Action Window dengan View -->
    <record id="action_library_book_list" model="ir.actions.act_window.view">
        <field name="sequence" eval="1"/>
        <field name="view_mode">list</field>
        <field name="view_id" ref="fahriza_library.view_library_book_list"/>
        <field name="act_window_id" ref="action_library_book"/>
    </record>

    <record id="action_library_book_form" model="ir.actions.act_window.view">
        <field name="sequence" eval="2"/>
        <field name="view_mode">form</field>
        <field name="view_id" ref="fahriza_library.view_library_book_form"/>
        <field name="act_window_id" ref="action_library_book"/>
    </record>

    <!-- Menu Item -->
    <menuitem id="menu_library_book_list"
                name="Buku"
                parent="menu_library_book"
                action="action_library_book"/>

**Penjelasan:**

- ``ir.actions.act_window`` → menentukan model dan mode tampilan default.

- ``ir.actions.act_window.view`` → mendefinisikan urutan dan view spesifik (misalnya list dan form).

- ``menuitem`` → membuat menu di UI Odoo.

- ``parent`` → menentukan hierarki menu.

- ``action`` → menghubungkan menu dengan action window.



Menggabungkan Semua View
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Semua deklarasi view, menu dan action dapat dimasukkan ke dalam satu file XML, misalnya di:  
``views/library_book_views.xml``

.. code-block:: xml

   <odoo>
       <record id="view_library_book_list" model="ir.ui.view">
           <field name="name">library.book.list</field>
           <field name="model">library.book</field>
           <field name="arch" type="xml">
               <list string="Daftar Buku">
                   <field name="name"/>
                   <field name="isbn"/>
                   <field name="published_date"/>
                   <field name="price"/>
                   <field name="available"/>
               </list>
           </field>
       </record>

       <record id="view_library_book_form" model="ir.ui.view">
           <field name="name">library.book.form</field>
           <field name="model">library.book</field>
           <field name="arch" type="xml">
               <form string="Data Buku">
                   <sheet>
                       <group>
                           <field name="name"/>
                           <field name="published_date"/>
                           <field name="isbn"/>
                           <field name="price"/>
                           <field name="available"/>
                       </group>
                   </sheet>
               </form>
           </field>
       </record>

       <record id="view_library_book_search" model="ir.ui.view">
           <field name="name">library.book.search</field>
           <field name="model">library.book</field>
           <field name="arch" type="xml">
               <search>
                   <field name="name" string="Judul Buku"/>
                   <field name="isbn"/>
               </search>
           </field>
       </record>

       <!-- Menu Root -->
       <menuitem id="menu_library_root" name="Perpustakaan"/>

       <!-- Submenu Buku -->
       <menuitem id="menu_library_book" name="Data Buku" parent="menu_library_root"/>

       <!-- Action Window -->
       <record id="action_library_book" model="ir.actions.act_window">
           <field name="name">Daftar Buku</field>
           <field name="res_model">library.book</field>
           <field name="view_mode">list,form</field>
       </record>

       <!-- Hubungan Action Window dengan View -->
       <record id="action_library_book_list" model="ir.actions.act_window.view">
           <field name="sequence" eval="1"/>
           <field name="view_mode">list</field>
           <field name="view_id" ref="fahriza_library.view_library_book_list"/>
           <field name="act_window_id" ref="action_library_book"/>
       </record>

       <record id="action_library_book_form" model="ir.actions.act_window.view">
           <field name="sequence" eval="2"/>
           <field name="view_mode">form</field>
           <field name="view_id" ref="fahriza_library.view_library_book_form"/>
           <field name="act_window_id" ref="action_library_book"/>
       </record>

       <!-- Menu Item -->
       <menuitem id="menu_library_book_list"
           name="Buku"
           parent="menu_library_book"
           action="action_library_book"/>
   </odoo>


Setelah file ini dimuat, menu **Perpustakaan → Data Buku → Buku** akan muncul di modul, dan membuka tampilan *list* terlebih dahulu sebelum *form view*.


3.6. Security (Access Rights)
=======================================

Sebelum model ``library.book`` dapat digunakan dari antarmuka Odoo,  
kita perlu memberikan hak akses (permissions) agar pengguna bisa melihat, membuat, mengedit, dan menghapus data.


3.6.1. File ir.model.access.csv
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

File hak akses disimpan di dalam direktori:

.. code-block::

   fahriza_library/
   └── security/
       └── ir.model.access.csv

Isinya dalam format CSV seperti berikut:

.. code-block:: csv

   id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
   access_library_book_user,access.library.book,model_library_book,base.group_user,1,1,1,1


3.6.2. Penjelasan Kolom
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **id** → identitas unik record hak akses (tidak boleh sama antar modul)
- **name** → nama deskriptif untuk rule ini
- **model_id:id** → nama model yang diizinkan (otomatis berdasarkan ``_name`` di model Python)
- **group_id:id** → grup pengguna yang diberi izin (misalnya ``base.group_user`` untuk user internal)
- **perm_read** → izin membaca data (1 = ya, 0 = tidak)
- **perm_write** → izin mengubah data
- **perm_create** → izin membuat data
- **perm_unlink** → izin menghapus data


3.6.3. Registrasi File di Manifest
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pastikan file CSV ini didaftarkan dalam ``__manifest__.py``  
agar diproses oleh Odoo ketika modul diinstal.

.. code-block:: python

    'data': [
        'data/fahriza_library_data.xml',
        'security/ir.model.access.csv',
        'views/library_book_views.xml',
    ],



💡 Tips Tambahan
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Setelah file hak akses ditambahkan dan modul di-*upgrade*, user internal Odoo (grup ``base.group_user``)  
akan memiliki akses penuh (read, write, create, delete) terhadap model ``library.book``.

Tanpa file ini, data akan tetap tersimpan di database,  
namun **tidak dapat diakses melalui menu atau tampilan apa pun** di Odoo.


- Untuk akses **khusus admin**, gunakan ``base.group_system``.  

- Jika model tidak memiliki akses sama sekali, Odoo akan menampilkan error:
  ``Access Error: You are not allowed to access 'library.book' records.``  

- Hak akses lanjutan seperti *record rules* dibahas pada bab selanjutnya.


--------------------------------------
4. Relations Between Models
--------------------------------------

Relasi digunakan untuk menghubungkan satu model dengan model lainnya.  
Di Odoo, relasi dikelola sepenuhnya oleh ORM — sehingga developer tidak perlu menulis query SQL ``JOIN`` secara manual seperti di PostgreSQL.


4.1. Jenis Relasi di Odoo
=======================================

Odoo menyediakan tiga jenis relasi utama:

+------------------+-----------------------------+--------------------------------------------+
| Jenis Relasi     | Arah Relasi                 | Contoh Logika                              |
+==================+=============================+============================================+
| ``Many2one``     | Banyak → Satu               | Banyak buku memiliki satu kategori         |
+------------------+-----------------------------+--------------------------------------------+
| ``One2many``     | Satu → Banyak               | Satu kategori memiliki banyak buku         |
+------------------+-----------------------------+--------------------------------------------+
| ``Many2many``    | Banyak ↔ Banyak             | Satu buku dapat memiliki banyak penulis,   |
|                  |                             | dan satu penulis dapat menulis banyak buku |
+------------------+-----------------------------+--------------------------------------------+


4.2. Contoh Many2one (Buku → Kategori)
=======================================

Setiap buku hanya memiliki satu kategori.  
Relasi ini seperti *foreign key* di PostgreSQL.

.. code-block:: python

   from odoo import models, fields

   class LibraryCategory(models.Model):
       _name = 'library.category'
       _description = 'Kategori Buku'

       name = fields.Char("Nama Kategori", required=True)
       description = fields.Text("Deskripsi")

   class LibraryBook(models.Model):
       _name = 'library.book'

       category_id = fields.Many2one(
           'library.category',
           string="Kategori",
           ondelete='set null'
       )

**Penjelasan:**

- ``category_id`` menjadi *foreign key* ke tabel ``library_category``.

- ``ondelete='set null'`` artinya jika kategori dihapus, kolom kategori buku akan dikosongkan.

- Secara otomatis, Odoo membuat kolom ``category_id`` di tabel ``library_book``.


4.3. Contoh One2many (Kategori → Buku)
=======================================

Kebalikan dari Many2one, kita bisa menampilkan semua buku dalam satu kategori.

.. code-block:: python

   class LibraryCategory(models.Model):
       _name = 'library.category'
       _description = 'Kategori Buku'

       name = fields.Char("Nama Kategori", required=True)
       description = fields.Text("Deskripsi")

       book_ids = fields.One2many(
           'library.book',       # model tujuan
           'category_id',        # field di model tujuan
           string="Daftar Buku"
       )

**Penjelasan:**

- ``book_ids`` tidak membuat kolom baru di database.

- Field ini bersifat virtual, digunakan untuk navigasi antar model.

- Hubungannya didasarkan pada field ``category_id`` di model ``library.book``.


4.4. Contoh Many2many (Buku ↔ Penulis)
=======================================

Dalam kasus lain, satu buku bisa memiliki banyak penulis,  
dan satu penulis bisa menulis banyak buku.

.. code-block:: python

   class LibraryAuthor(models.Model):
       _name = 'library.author'
       _description = 'Penulis Buku'

       name = fields.Char("Nama Penulis", required=True)
       biography = fields.Text("Biografi")

   class LibraryBook(models.Model):
       _name = 'library.book'

       author_ids = fields.Many2many(
           'library.author',
           'library_book_author_rel',   # nama tabel relasi (opsional)
           'book_id',                   # kolom yang mereferensi buku
           'author_id',                 # kolom yang mereferensi penulis
           string="Penulis"
       )

**Penjelasan:**

- ORM akan otomatis membuat tabel *relasi many-to-many* bernama ``library_book_author_rel``.

- Kita bisa memberi nama sendiri untuk tabel relasi (parameter kedua).

- Tidak perlu membuat tabel relasi secara manual seperti di SQL.


4.5. Contoh Kombinasi Relasi dalam Modul Library
=======================================

Berikut contoh penerapan semua relasi di modul ``fahriza_library``.

4.5.1. Definisi Model dan Field
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python


   from odoo import models, fields


   class LibraryCategory(models.Model):
       _name = 'library.category'
       _description = 'Kategori Buku'

       name = fields.Char("Nama Kategori", required=True)
       book_ids = fields.One2many('library.book', 'category_id', string="Daftar Buku")


   class LibraryAuthor(models.Model):
       _name = 'library.author'
       _description = 'Penulis Buku'

       name = fields.Char("Nama Penulis", required=True)
       biography = fields.Text("Biografi")
       book_ids = fields.Many2many('library.book', string="Buku Ditulis")


   class LibraryBook(models.Model):
       _name = 'library.book'
       _description = 'Data Buku Perpustakaan'

       name = fields.Char("Judul Buku", required=True)
       isbn = fields.Char("ISBN")
       published_date = fields.Date("Tanggal Terbit")
       price = fields.Float("Harga")
       available = fields.Boolean("Tersedia", default=True)

       category_id = fields.Many2one('library.category', string="Kategori")
       author_ids = fields.Many2many('library.author', string="Penulis")

4.5.2. Definisi View dengan Relasi pada file ``views/library_book_views.xml``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: xml

    <odoo>
        <record id="view_library_book_list" model="ir.ui.view">
            <field name="name">library.book.list</field>
            <field name="model">library.book</field>
            <field name="arch" type="xml">
                <list string="Daftar Buku">
                    <field name="name" />
                    <field name="isbn" />
                    <field name="category_id" />  <!-- Many2one -->
                    <field name="published_date" />
                    <field name="price" />
                    <field name="available" />
                </list>
            </field>
        </record>

        <record id="view_library_book_form" model="ir.ui.view">
            <field name="name">library.book.form</field>
            <field name="model">library.book</field>
            <field name="arch" type="xml">
                <form string="Data Buku">
                    <sheet>
                        <group>
                            <field name="name" />
                            <field name="category_id" />  <!-- Many2one -->
                            <field name="author_ids" widget="many2many_tags" /> <!-- Many2many -->
                            <field name="published_date" />
                            <field name="isbn" />
                            <field name="price" />
                            <field name="available" />
                        </group>
                    </sheet>
                </form>
            </field>
        </record>

        <record id="view_library_book_search" model="ir.ui.view">
            <field name="name">library.book.search</field>
            <field name="model">library.book</field>
            <field name="arch" type="xml">
                <search>
                    <field name="name" string="Judul Buku" />
                    <field name="isbn" />
                    <field name="category_id" />  <!-- Many2one -->
                </search>
            </field>
        </record>

        <!-- Menu Root -->
        <menuitem id="menu_library_root" name="Perpustakaan" />

        <!-- Submenu Buku -->
        <menuitem id="menu_library_book" name="Data Buku" parent="menu_library_root" />

        <!-- Action Window -->
        <record id="action_library_book" model="ir.actions.act_window">
            <field name="name">Daftar Buku</field>
            <field name="res_model">library.book</field>
            <field name="view_mode">list,form</field>
        </record>

        <!-- Hubungan Action Window dengan View -->
        <record id="action_library_book_list" model="ir.actions.act_window.view">
            <field name="sequence" eval="1" />
            <field name="view_mode">list</field>
            <field name="view_id" ref="fahriza_library.view_library_book_list" />
            <field name="act_window_id" ref="action_library_book" />
        </record>

        <record id="action_library_book_form" model="ir.actions.act_window.view">
            <field name="sequence" eval="2" />
            <field name="view_mode">form</field>
            <field name="view_id" ref="fahriza_library.view_library_book_form" />
            <field name="act_window_id" ref="action_library_book" />
        </record>

        <!-- Menu Item -->
        <menuitem id="menu_library_book_list"
            name="Buku"
            parent="menu_library_book"
            action="action_library_book" />
    </odoo>

4.5.3. Definisi View, Action dan Menu untuk model ``library.category`` pada file ``views/library_category_views.xml``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: xml

   <odoo>
       <!-- List View Kategori -->
       <record id="view_library_category_list" model="ir.ui.view">
           <field name="name">library.category.list</field>
           <field name="model">library.category</field>
           <field name="arch" type="xml">
               <list string="Daftar Kategori">
                   <field name="name"/>
               </list>
           </field>
       </record>

       <!-- Form View Kategori -->
       <record id="view_library_category_form" model="ir.ui.view">
           <field name="name">library.category.form</field>
           <field name="model">library.category</field>
           <field name="arch" type="xml">
               <form string="Data Kategori">
                   <sheet>
                       <group>
                           <field name="name"/>
                       </group>
                       <notebook>
                           <page string="Buku dalam Kategori">
                               <field name="book_ids">
                                   <tree>
                                       <field name="name"/>
                                       <field name="isbn"/>
                                       <field name="published_date"/>
                                   </tree>
                               </field>
                           </page>
                        </notebook>
                   </sheet>
               </form>
           </field>
       </record>

       <!-- Search View Kategori -->
       <record id="view_library_category_search" model="ir.ui.view">
           <field name="name">library.category.search</field>
           <field name="model">library.category</field>
           <field name="arch" type="xml">
               <search string="Cari Kategori">
                   <field name="name" string="Nama Kategori"/>
               </search>
           </field>
       </record>

       <!-- Action Window Kategori -->
       <record id="action_library_category" model="ir.actions.act_window">
           <field name="name">Daftar Kategori</field>
           <field name="res_model">library.category</field>
           <field name="view_mode">list,form</field>
       </record>

       <!-- Menu Item Kategori -->
       <menuitem id="menu_library_category"
                 name="Kategori"
                 parent="menu_library_root"
                 action="action_library_category"/>
   </odoo>

4.5.4. Definisi View, Action dan Menu untuk model ``library.author`` pada file ``views/library_author_views.xml``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: xml

    <odoo>
         <!-- List View Penulis -->
         <record id="view_library_author_list" model="ir.ui.view">
              <field name="name">library.author.list</field>
              <field name="model">library.author</field>
              <field name="arch" type="xml">
                <list string="Daftar Penulis">
                     <field name="name"/>
                     <field name="book_ids" widget="many2many_tags"/> <!-- Many2many -->
                </list>
              </field>
         </record>
    
         <!-- Form View Penulis -->
         <record id="view_library_author_form" model="ir.ui.view">
              <field name="name">library.author.form</field>
              <field name="model">library.author</field>
              <field name="arch" type="xml">
                <form string="Data Penulis">
                     <sheet>
                          <group>
                            <field name="name"/>
                            <field name="biography"/>
                            <field name="book_ids" widget="many2many_tags"/> <!-- Many2many -->
                          </group>
                     </sheet>
                </form>
              </field>
         </record>
    
         <!-- Search View Penulis -->
         <record id="view_library_author_search" model="ir.ui.view">
              <field name="name">library.author.search</field>
              <field name="model">library.author</field>
              <field name="arch" type="xml">
                <search string="Cari Penulis">
                     <field name="name" string="Nama Penulis"/>
                </search>
              </field>
         </record>
    
         <!-- Action Window Penulis -->
         <record id="action_library_author" model="ir.actions.act_window">
              <field name="name">Daftar Penulis</field>
              <field name="res_model">library.author</field>
              <field name="view_mode">list,form</field>
         </record>
    
         <!-- Menu Item Penulis -->
         <menuitem id="menu_library_author"
                  name="Penulis"
                  parent="menu_library_root"
                  action="action_library_author"/>
    </odoo>


4.5.5. Tambah access rights untuk model baru di file ``security/ir.model.access.csv``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: csv

   id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
   access_library_book_user,access.library.book,model_library_book,base.group_user,1,1,1,1
   access_library_category_user,access.library.category,model_library_category,base.group_user,1,1,1,1
   access_library_author_user,access.library.author,model_library_author,base.group_user,1,1,1,1

4.5.6. Registrasi Semua File di Manifest
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Pastikan semua file XML dan CSV didaftarkan di ``__manifest__.py``:

.. code-block:: python

        'data': [
            'data/fahriza_library_data.xml',
            'security/ir.model.access.csv',
            'views/library_book_views.xml',
            'views/library_category_views.xml',
            'views/library_author_views.xml',
        ],


💡 Latihan
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Buat model ``library.category`` dan ``library.author``.
2. Tambahkan relasi:
   - ``Many2one`` dari ``library.book`` ke ``library.category``
   - ``Many2many`` antara ``library.book`` dan ``library.author``
3. Buat menu, action dan view untuk model ``library.category`` dan ``library.author``.
4. Tambahkan field relasi ke form view masing-masing.
5. Coba input data kategori dan penulis dari UI, lalu hubungkan dengan buku.
6. Perhatikan bagaimana field relasi otomatis membuat dropdown dan tabel relasi di antarmuka Odoo.

--------------------------------------
5. Inheritance
--------------------------------------

Inheritance (pewarisan) dalam Odoo digunakan untuk **memperluas atau memodifikasi perilaku** dari model atau view yang sudah ada, tanpa harus menyalin seluruh kodenya.  
Dengan inheritance, kita bisa menambahkan field, mengubah tampilan, atau menyesuaikan logika bisnis dari model lain.

Ada dua jenis inheritance utama di Odoo:

1. **Model Inheritance** — memperluas model Python.
2. **View Inheritance** — memperluas tampilan XML.


5.1. Model Inheritance
=======================================

Model inheritance digunakan untuk **menambahkan atau mengubah field serta method** dari model yang sudah ada.  
Misalnya, kita ingin menambahkan informasi apakah *partner* merupakan anggota perpustakaan.

**Contoh:** menambahkan field ke model ``res.partner``

.. code-block:: python

   # File: models/res_partner.py
   from odoo import models, fields

   class ResPartner(models.Model):
       _inherit = 'res.partner'

       is_library_member = fields.Boolean("Anggota Perpustakaan", default=False)

**Penjelasan:**

- ``_inherit`` digunakan untuk mewarisi model yang sudah ada (dalam hal ini ``res.partner`` dari modul `base`).

- Field baru ``is_library_member`` ditambahkan tanpa memodifikasi kode asli model `res.partner`.

- Model ini otomatis digabung dengan model induknya saat Odoo memproses registry model.

**Struktur folder Python:**

.. code-block:: text

   fahriza_library/
   ├── models/
   │   ├── __init__.py
   │   ├── models.py
   │   └── res_partner.py
   └── __manifest__.py

Isi file `models/__init__.py` harus memanggil file Python baru:

.. code-block:: python

   from . import models
   from . import res_partner



5.2. View Inheritance
=======================================

View inheritance digunakan untuk **menambahkan atau memodifikasi elemen tampilan** dari view yang sudah ada.  
Dengan cara ini, kita tidak perlu menduplikasi seluruh struktur XML dari view aslinya.

**Contoh:** menambahkan field ``is_library_member`` ke form ``res.partner``.

.. code-block:: xml

   <!-- File: views/res_partner_views.xml -->
   <odoo>
       <record id="view_partner_form_inherit_library" model="ir.ui.view">
           <field name="name">res.partner.form.inherit.library</field>
           <field name="model">res.partner</field>
           <field name="inherit_id" ref="base.view_partner_form"/>
           <field name="arch" type="xml">
                <xpath expr="//field[@name='function']" position="before">
                    <field name="is_library_member" />
                </xpath>
           </field>
       </record>
   </odoo>

**Penjelasan:**

- ``inherit_id`` menunjuk ke view asli yang ingin kita perluas (``base.view_partner_form``).

- ``xpath`` digunakan untuk menentukan lokasi di mana elemen baru akan disisipkan.

- ``position="before"`` berarti field baru akan diletakkan sebelum elemen target.

**Struktur folder XML:**

.. code-block:: text

   fahriza_library/
   ├── views/
   │   ├── library_book_views.xml
   │   └── res_partner_views.xml
   └── __manifest__.py

Pastikan file XML baru juga direferensikan di `__manifest__.py` agar dimuat saat modul diinstall:

.. code-block:: python

    'data': [
        'data/fahriza_library_data.xml',
        'security/ir.model.access.csv',
        'views/library_book_views.xml',
        'views/res_partner_views.xml',
    ],


💡 Tips Tambahan
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Dengan inheritance:

- Kita bisa **memperluas model dan view yang ada tanpa menyalin atau mengubah file aslinya.**

- Teknik ini menjaga **kompatibilitas** dan **kemudahan upgrade**, karena perubahan hanya dilakukan di modul turunan.

- Inheritance adalah konsep fundamental dalam pengembangan modul Odoo yang modular dan berkelanjutan.

- Karena view ``view_partner_form`` baru bisa kita lihat setelah install modul ``Contacts``, pastikan modul tersebut sudah terinstal sebelum menguji inheritance view.

