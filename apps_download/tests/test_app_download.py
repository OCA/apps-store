# Copyright (C) 2017-Today: Odoo Community Association (OCA)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import os

from odoo.exceptions import ValidationError

from odoo.addons.apps_product_creator.tests.common import Common


class TestAppDownload(Common):
    """Test for the Add download"""

    def setUp(self):
        super().setUp()
        test_path = os.path.dirname(os.path.realpath(__file__))
        module_path = os.path.join(test_path, "test_modules", "broken_lint")
        self.sub_child_product = self.env["product.product"].create(
            {"name": "business_requirement", "module_path": module_path}
        )
        module_path = os.path.join(test_path, "test_modules", "second_module")
        self.child_product = self.env["product.product"].create(
            {
                "name": "business_requirement_deliverable",
                "dependent_product_ids": [(6, 0, self.sub_child_product.ids)],
                "module_path": module_path,
            }
        )
        module_name = "test_module"
        self.odoo_module1_version2.technical_name = module_name
        self.main_app_product = self.env["product.product"].create(
            {
                "name": "business_requirement_deliverable_project",
                "odoo_module_version_id": self.odoo_module1_version2.id,
            }
        )
        self.main_app_product.module_path = os.path.join(test_path, "test_modules")

    def test_dependency(self):
        self.main_app_product.write(
            {"dependent_product_ids": [(6, 0, self.child_product.ids)]}
        )
        self.assertEqual(
            len(self.main_app_product.dependent_product_ids.ids),
            1,
            "Dependency: App Dependency does not set properlly",
        )
        self.main_app_product.generate_zip_file()
        with self.assertRaises(ValidationError):
            self.main_app_product.write(
                {"dependent_product_ids": [(6, 0, self.main_app_product.ids)]}
            )

    def _get_attachments(self, products):
        return self.env["ir.attachment"].search(
            [("res_id", "=", products.ids), ("res_model", "=", products._name)],
        )

    def test_generate_zip(self):
        """The attachment of a product can be generated."""
        # Arrange
        product = self.main_app_product
        existing_attachments = self._get_attachments(product)
        # pre-condition
        self.assertTrue(self.main_app_product.module_path)

        # Act
        product.generate_zip_file()

        # Assert
        zip_file = self._get_attachments(product) - existing_attachments
        self.assertTrue(zip_file)
