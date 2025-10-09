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
        self.env['library.loan'].sudo().create({
            'borrower_id': self.borrower_id.id,
            'book_id': self.book_id.id,
            'borrow_date': self.borrow_date,
            'state': 'borrowed',
        })
        return {'type': 'ir.actions.act_window_close'}