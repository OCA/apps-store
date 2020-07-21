# Copyright (C) 2017-Today: Odoo Community Association (OCA)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    odoo_module_id = fields.Many2one("odoo.module", "Odoo Module", readonly=True,)
    technical_name = fields.Char(
        "Technical Name", related="odoo_module_id.technical_name", store=True,
    )
