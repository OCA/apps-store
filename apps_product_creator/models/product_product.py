# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def create(self, values):
        if values.get('product_tmpl_id') and values.get('attribute_value_ids'):
            template = self.env['product.template'].browse(
                values['product_tmpl_id'])
            attribute = self.env['product.attribute.value'].browse(
                values['attribute_value_ids'][0][2]).filtered(
                lambda x: x.attribute_id == self.env.ref(
                    'github_product_creator.attribute_odoo_version'))

            if attribute:
                version = template.odoo_module_id.module_version_ids.filtered(
                    lambda x:
                    x.organization_milestone_id.name == attribute.name)
                if version:
                    values.update({'odoo_module_version_id': version.id})
        return super(ProductProduct, self).create(values)

    odoo_module_version_id = fields.Many2one(
        'odoo.module.version', 'Odoo Module')

    license = fields.Char(
        string='License (Manifest)', readonly=True,
        related="odoo_module_version_id.license", store=True)
    summary = fields.Char(
        string='Summary (Manifest)', readonly=True,
        related="odoo_module_version_id.summary", store=True)
    website = fields.Char(
        string='Website (Manifest)', readonly=True,
        related="odoo_module_version_id.website", store=True)
    external_dependencies = fields.Char(
        string='External Dependencies (Manifest)',
        readonly=True, related="odoo_module_version_id.external_dependencies",
        store=True)
    description_rst = fields.Char(
        string='RST Description (Manifest)', readonly=True,
        related="odoo_module_version_id.description_rst", store=True)
    description_rst_html = fields.Html(
        string='HTML the RST Description', readonly=True,
        related="odoo_module_version_id.description_rst_html", store=True)
    version = fields.Char(
        string='Version (Manifest)', readonly=True,
        related="odoo_module_version_id.version", store=True)
    author = fields.Char(
        string='Author (Manifest)', readonly=True,
        related="odoo_module_version_id.author", store=True)
    image_module = fields.Binary(
        string='Icon Image', reaonly=True,
        related="odoo_module_version_id.image", store=True)
    github_url = fields.Char(
        string='Github URL', readonly=True,
        related="odoo_module_version_id.github_url", store=True)
