# Copyright (C) 2017-Today: Odoo Community Association (OCA), BizzAppDev
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, api


class OdooModuleVersion(models.Model):
    _inherit = 'odoo.module.version'

    @api.multi
    def _process_clean_module_version(self):
        for module_version in self:
            product = self.env['product.product'].search(
                [('odoo_module_version_id', '=', module_version.id)])
            product.write({'active': False})
            all_variant_archived = all(
                [
                    not a for a in
                    product.product_tmpl_id.product_variant_ids.mapped(
                        'active')
                ]
            )
            if all_variant_archived:
                product.product_tmpl_id.write(
                    {'active': False, 'website_published': False})
        return super(OdooModuleVersion, self)._process_clean_module_version()
