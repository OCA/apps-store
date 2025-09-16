# Copyright (C) 2017-Today: Odoo Community Association (OCA)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from .common import Common


class TestAppsProductCreator(Common):
    def test1_product_create(self):
        self.assertFalse(self.odoo_module1.product_template_id)
        self.odoo_module1.action_create_product()
        self.assertTrue(self.odoo_module1.product_template_id)
        action = self.odoo_module1.action_view_products()
        self.assertEqual(
            self.odoo_module1.product_template_id.product_variant_ids.ids[0],
            action["res_id"],
        )

    def test_process_clean_module_version(self):
        self.assertTrue(self.odoo_module2.product_template_id)
        self.odoo_module1_version2._process_clean_module_version()
        self.assertFalse(self.odoo_module1.product_template_id.active)
        self.assertFalse(self.odoo_module1.product_template_id.website_published)

    def test_action_create_product_active_product(self):
        self.odoo_module1_version2._process_clean_module_version()
        self.odoo_module2.action_create_product()
        self.assertTrue(self.odoo_module2.product_template_id.active)
        self.assertTrue(self.odoo_module2.product_template_id.website_published)

    def test_odoo_module_update_product(self):
        self.odoo_module1_version2._process_clean_module_version()
        self.odoo_module2._update_product()
        self.assertTrue(self.odoo_module2.product_template_id.active)
        self.assertTrue(self.odoo_module2.product_template_id.website_published)
