# Copyright (C) 2017-Today: Odoo Community Association (OCA)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.multi
    @api.depends('product_variant_ids', 'product_variant_ids.download_count')
    def _compute_total_download_count(self):
        for product in self:
            product.total_download_count = sum(
                product.mapped('product_variant_ids.download_count'))

    total_download_count = fields.Integer(
        compute="_compute_total_download_count", store=True)

    def get_author_details(self):
        author_ids = []
        for variant in self.product_variant_ids:
            for author in variant.app_author_ids:
                if author not in author_ids:
                    author_ids.append(author)
        return author_ids

    def get_version_info(self):
        products = self.product_variant_ids.sorted(
            lambda a: a.attribute_value_ids.sequence,  reverse=True)
        return products[0]
