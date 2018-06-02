# -*- coding: utf-8 -*-
# Copyright (C) 2018-Today: Odoo Community Association (OCA)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def get_author_details(self):
        author_ids = []
        for variant in self.product_variant_ids:
            for author in variant.app_author_ids:
                if author not in author_ids:
                    author_ids.append(author)
        return author_ids

    def get_version_info(self):
        versions = []
        for attr in self.attribute_line_ids:
            for value in attr.value_ids:
                versions.append(float(value.name))
        version = max([x for x in versions])
        product = self.env['product.product'].search([
            ('attribute_value_ids.name', 'ilike', str(version)),
            ('product_tmpl_id', '=', self.id),
            ])
        return product
