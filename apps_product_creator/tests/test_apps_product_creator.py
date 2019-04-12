# Copyright (C) 2017-Today: Odoo Community Association (OCA)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.tests.common import TransactionCase


class TestAppsProductCreator(TransactionCase):

    def setUp(self):
        super(TestAppsProductCreator, self).setUp()

        self.organization1 = self.env['github.organization'].create({
            'name': 'Organization 1',
            'github_login': 'login',
        })

        self.organization_serie1 = self.env[
            'github.organization.serie'].create({
                'name': '12.0',
                'sequence': 1,
                'organization_id': self.organization1.id,
            })

        self.repository1 = self.env['github.repository'].create({
            'name': 'Repository1',
            'organization_id': self.organization1.id,
        })

        self.branch1 = self.env['github.repository.branch'].create({
            'name': '12.0',
            'repository_id': self.repository1.id,
            'organization_id': self.organization1.id,
        })

        self.odoo_module2 = self.env['odoo.module'].create({
            'technical_name': 'odoo_module2',
        })

        self.odoo_module1_version2 = self.env['odoo.module.version'].create({
            'name': 'Odoo Module 2',
            'technical_name': 'odoo_module2',
            'module_id': self.odoo_module2.id,
            'repository_branch_id': self.branch1.id,
            'license': 'AGPL-3',
            'summary': 'Summary Test',
            'website': 'Website Test',
            'description_rst': 'Description Test',
            'version': '10.0',
            'author': 'OCA',
            'depends': 'base',
            'external_dependencies': '{}',
        })

        self.odoo_module1 = self.env['odoo.module'].create({
            'technical_name': 'odoo_module1',
            'dependence_module_version_ids': [
                (6, 0, [self.odoo_module1_version2.id])],
        })

        self.odoo_module1_version1 = self.env['odoo.module.version'].create({
            'name': 'Odoo Module 1',
            'technical_name': 'odoo_module1',
            'module_id': self.odoo_module1.id,
            'repository_branch_id': self.branch1.id,
            'license': 'AGPL-3',
            'summary': 'Summary Test',
            'website': 'Website Test',
            'description_rst': 'Description Test',
            'version': '10.0',
            'author': 'OCA',
            'depends': 'base',
            'external_dependencies': '{}',
        })

    def test1_product_create(self):
        self.assertFalse(self.odoo_module1.product_template_id)
        self.odoo_module1.action_create_product()
        self.assertTrue(self.odoo_module1.product_template_id)
        action = self.odoo_module1.action_view_products()
        self.assertEqual(
            self.odoo_module1.product_template_id.product_variant_ids.ids[0],
            action['res_id']
        )
