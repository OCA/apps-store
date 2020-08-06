# Copyright (C) 2017-Today: Odoo Community Association (OCA)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.depends("product_variant_ids", "product_variant_ids.download_count")
    def _compute_total_download_count(self):
        for product in self:
            product.total_download_count = sum(
                product.mapped("product_variant_ids.download_count")
            )

    total_download_count = fields.Integer(
        compute="_compute_total_download_count", store=True
    )

    def get_author_details(self):
        return self.mapped("product_variant_ids.app_author_ids")

    def get_version_info(self):
        products = self.product_variant_ids.sorted(
            lambda a: a._get_combination_info_variant().get("attribute_seq", 0),
            reverse=True,
        )
        return products[0]

    def _get_combination_info(
        self,
        combination=False,
        product_id=False,
        add_qty=1,
        pricelist=False,
        parent_combination=False,
        only_template=False,
    ):
        vals = super()._get_combination_info(
            combination=combination,
            product_id=product_id,
            add_qty=add_qty,
            pricelist=pricelist,
            parent_combination=parent_combination,
            only_template=only_template,
        )
        if not vals["product_id"]:
            return vals
        product = self.env["product.product"].browse(vals["product_id"])
        if product.odoo_module_id:
            module_id = product.odoo_module_version_id.module_id
            vals.update(
                {
                    "is_odoo_module": True,
                    "name_product": product.name,
                    "technical_name": module_id.technical_name,
                    "license": product.app_license_id.name,
                    "license_url": product.app_license_id.website,
                    "author": ", ".join(
                        author.name for author in product.app_author_ids
                    ),
                    "website": product.app_website,
                    "repository": product.app_github_url,
                    "rst_html": product.app_description_rst_html,
                    "app_summary": product.app_summary,
                    "attribute_seq": combination.attribute_id.sequence,
                }
            )
        return vals

    def _get_first_possible_combination(
        self, parent_combination=None, necessary_values=None
    ):
        """Override method to load last version first in app store"""
        values = list(
            self._get_possible_combinations(parent_combination, necessary_values)
        )
        if not any(values):
            return self.env["product.template.attribute.value"]
        return values[-1]
