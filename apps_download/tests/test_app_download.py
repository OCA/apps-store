# Copyright (C) 2017-Today: Odoo Community Association (OCA)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
import os


class TestAppDownload(TransactionCase):
    """Test for the Add download"""

    def setUp(self):
        super(TestAppDownload, self).setUp()
        test_path = os.path.dirname(os.path.realpath(__file__))
        module_path = os.path.join(
            test_path, 'test_modules', 'broken_lint')
        self.sub_child_product = self.env['product.product'].create(
            {
                'name': 'business_requirement',
                'module_path': module_path
            }
        )
        module_path = os.path.join(
            test_path, 'test_modules', 'second_module')
        self.child_product = self.env['product.product'].create(
            {
                'name': 'business_requirement_deliverable',
                'dependent_product_ids': [(6, 0, self.sub_child_product.ids)],
                'module_path': module_path
            }
        )
        module_path = os.path.join(
            test_path, 'test_modules', 'test_module')
        self.main_app_product = self.env['product.product'].create(
            {
                'name': 'business_requirement_deliverable_project',
                'module_path': module_path
            }
        )

    def test_dependency(self):
        self.main_app_product.write(
            {
                'dependent_product_ids': [(6, 0, self.child_product.ids)]
            }
        )
        self.assertEqual(
            len(self.main_app_product.dependent_product_ids.ids), 1,
            'Dependency: App Dependency does not set properlly')
        self.main_app_product.generate_zip_file()
        with self.assertRaises(ValidationError):
            self.main_app_product.write(
                {
                    'dependent_product_ids': [
                        (6, 0, self.main_app_product.ids)]
                }
            )
