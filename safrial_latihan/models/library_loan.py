from odoo import models, fields, api
from datetime import date, timedelta
from odoo.exceptions import ValidationError

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
    # borrow_date = fields.Date("Tanggal Pinjam", required=True)
    # return_date = fields.Date("Tanggal Kembali")
    state = fields.Selection([
        ('borrowed', 'Dipinjam'),
        ('returned', 'Dikembalikan')
    ], string="Status", default='borrowed')

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


    @api.onchange('borrow_date')
    def _onchange_borrow_date(self):
        today = date.today()
        for rec in self:
            if rec.borrow_date.weekday() == 4:
                rec.return_date = rec.borrow_date + timedelta(days=3)
            else:
                rec.return_date = rec.borrow_date + timedelta(days=1)

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
                
    @api.constrains('return_date')
    def _check_return_date(self):
        for rec in self:
            if rec.return_date < rec.borrow_date:
                raise ValidationError(
                    f"Tanggal Pengembalian tidak boleh sebelum Tanggal Peminjaman"
                )
    
    def action_return_book(self):
        self.state = "returned"
        pass