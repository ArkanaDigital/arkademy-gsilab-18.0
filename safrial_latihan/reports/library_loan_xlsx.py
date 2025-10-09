from odoo import models

class LibraryLoanXlsx(models.AbstractModel):
    _name = 'report.safrial_latihan.report_library_loan_xlsx'
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