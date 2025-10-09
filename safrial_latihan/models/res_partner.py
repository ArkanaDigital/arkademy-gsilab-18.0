# File: models/res_partner.py
from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_library_member = fields.Boolean("Anggota Perpustakaan", default=False)