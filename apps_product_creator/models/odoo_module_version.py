# Copyright (C) 2017-Today: Odoo Community Association (OCA), BizzAppDev
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, api


class OdooModuleVersion(models.Model):
    _inherit = 'odoo.module.version'

    @api.multi
    def _process_clean_module_version(self):
        product_obj = self.env['product.product']
        for module_version in self:
            product = product_obj.search(
                [('odoo_module_version_id', '=', module_version.id)])
            product.write({'active': False})
            active_variants = product_obj.search_count(
                [
                    ('product_tmpl_id', '=', product.product_tmpl_id.id),
                    ('active', '=', True)
                ]
            )
            if not active_variants:
                product.product_tmpl_id.write(
                    {'active': False, 'website_published': False})
        return super(OdooModuleVersion, self)._process_clean_module_version()
