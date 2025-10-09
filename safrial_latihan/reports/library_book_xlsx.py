from odoo import models

class LibraryBookXlsx(models.AbstractModel):
    _name = 'report.safrial_latihan.report_library_book_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, books):
        # Format teks tebal
        bold = workbook.add_format({'bold': True})
        sheet = workbook.add_worksheet('List Buku')

        # Header kolom
        sheet.write(0, 0, 'Judul', bold)
        sheet.write(0, 1, 'ISBN', bold)
        sheet.write(0, 2, 'Kategori', bold)
        sheet.write(0, 3, 'Stok Tersedia', bold)

        # Data
        row = 1
        for book in books:
            sheet.write(row, 0, book.name)
            sheet.write(row, 1, book.isbn)
            sheet.write(row, 2, book.category_id.name)
            sheet.write(row, 3, book.available)
            row += 1