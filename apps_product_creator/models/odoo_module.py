# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: Odoo Community Association (OCA)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class OdooModule(models.Model):
    _inherit = 'odoo.module'

    product_template_id = fields.Many2one(
        'product.template',
        "Product Template",
    )

    @api.multi
    def action_create_product(self):
        self._create_product()

    @api.multi
    def _create_product(self):
        """
        Create the product template related to the module in current recordset.
        :return: product.template recordset
        """
        product_obj = self.env['product.template']
        products = self.env['product.template']
        modules = self.filtered(lambda m: not m.product_template_id)
        domain = [
            ('odoo_module_id', '=', modules.ids),
        ]
        matching_products = product_obj.search(domain)
        for odoo_module in modules:
            product = matching_products.filtered(
                lambda p: p.odoo_module_id == odoo_module)
            if not product:
                product_values = odoo_module._get_template_values()
                new_product = product_obj.create(product_values)
                odoo_module.write({
                    'product_template_id': new_product.id,
                })
                products |= new_product
        return products

    @api.multi
    def _get_template_values(self):
        """
        Create the dict to create a product.template recordset based on the
        current recordset.
        The values dict contains info to link the future product with the
        current module. It also fill the name of the future product with the
        name of the current module.
        :return: dict
        """
        self.ensure_one()
        attribute_obj = self.env['product.attribute.value']
        milestones = self.module_version_ids.mapped(
            'repository_branch_id.organization_milestone_id.name')
        attributes = attribute_obj.search([('name', 'in', milestones)])
        attribute = self.env.ref(
            'github_product_creator.attribute_odoo_version')
        attribute_line_values = {
            'attribute_id': attribute.id,
            'value_ids': [(6, 0, attributes.ids)],
        }
        values = {
            'odoo_module_id': self.id,
            'type': 'service',
            'name': self.name,
            'attribute_line_ids': [
                (0, 0, attribute_line_values),
            ]
        }
        return values
