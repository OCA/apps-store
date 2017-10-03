# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    odoo_module_id = fields.Many2one(
        'odoo.module', 'Odoo Module', readonly=True)
    technical_name = fields.Char(
        string="Technical Name", related="odoo_module_id.technical_name",
        store=True)
