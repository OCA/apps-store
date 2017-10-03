# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: Odoo Community Association (OCA)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api, _
from openerp.tools import html_sanitize


class OdooModule(models.Model):
    _inherit = 'odoo.module'

    product_template_id = fields.Many2one('product.template', string="Product Template")

    @api.multi
    def action_create_product(self):
        self._create_product()

    @api.multi
    def _create_product(self):
        for module in self:
            if module.product_template_id:
                continue
            matching_template = self.env['product.template'].search([('odoo_module_id','=',module.id)], limit=1)
            if matching_template:
                module.product_template_id = matching_template
                continue
            template_dict = module._get_template_values()
            new_template = self.env['product.template'].create(template_dict)
            module.product_template_id = new_template

    @api.multi
    def _get_template_values(self):
        self.ensure_one()

        milestones = self.module_version_ids.mapped('repository_branch_id').mapped('organization_milestone_id').mapped('name')
        value_ids = self.env['product.attribute.value'].search([('name','in',milestones)]).ids

        ret = {
            'odoo_module_id': self.id,
            'type': 'service',
            'name': self.name,
            'attribute_line_ids': [(0, 0, {
                'attribute_id': self.env.ref('github_product_creator.attribute_odoo_version').id,
                'value_ids': [(6, 0, value_ids)],
            })]
        }
        return ret