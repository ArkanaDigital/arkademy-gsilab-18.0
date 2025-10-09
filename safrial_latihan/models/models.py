from odoo import models, fields, api


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
    _sql_constraints = [
        ('unique_isbn', 'unique(isbn)', 'Nomor ISBN harus unik!'),
        ('check_price_positive', 'CHECK(price >= 0)', 'Harga tidak boleh negatif!')
    ]

    name = fields.Char("Judul Buku", required=True)
    isbn = fields.Char("ISBN")
    published_date = fields.Date("Tanggal Terbit")
    price = fields.Float("Harga")
    available = fields.Boolean("Tersedia", default=True)

    category_id = fields.Many2one('library.category', string="Kategori")
    author_ids = fields.Many2many('library.author', string="Penulis")

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

    total_loan_count = fields.Integer("Total Loan", compute="_compute_loan", store=True)

    @api.depends('loan_ids')
    def _compute_loan(self):
        for rec in self:
            rec.total_loan_count = len(rec.loan_ids)
    