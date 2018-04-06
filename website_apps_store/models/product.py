# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def get_author_details(self):
        author_ids = []
        for variant in self.product_variant_ids:
            for author in variant.app_author_ids:
                if author not in author_ids:
                    author_ids.append(author)
        return author_ids

