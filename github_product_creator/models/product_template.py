# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: Odoo Community Association (OCA)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api, _
from openerp.tools import html_sanitize


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    odoo_module_id = fields.Many2one('odoo.module', 'Odoo Module', readonly=True)
    technical_name = fields.Char(string="Technical Name", related="odoo_module_id.technical_name", store=True)
