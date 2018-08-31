# Copyright (C) 2018-Today: Odoo Community Association (OCA)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.tests.common import TransactionCase


class TestWebsiteAppsStore(TransactionCase):

    def setUp(self):
        super(TestWebsiteAppsStore, self).setUp()

        self.organization2 = self.env['github.organization'].create({
            'name': 'Organization 2',
            'github_login': 'login',
        })

        self.repository2 = self.env['github.repository'].create({
            'name': 'Repository2',
            'organization_id': self.organization2.id,
        })

        self.branch2 = self.env['github.repository.branch'].create({
            'name': 'master',
            'repository_id': self.repository2.id,
        })

        self.odoo_module2 = self.env['odoo.module'].create({
            'technical_name': 'odoo_module2',
        })

        self.attribute = self.env.ref(
            'apps_product_creator.attribute_odoo_version')
        self.version = self.env.ref('apps_product_creator.odoo_version_100')

        self.odoo_module2_version2 = self.env['odoo.module.version'].create({
            'name': 'Odoo Module 2',
            'technical_name': 'odoo_module2',
            'module_id': self.odoo_module2.id,
            'repository_branch_id': self.branch2.id,
            'license': 'AGPL-3',
            'summary': 'Summary Test',
            'website': 'Website Test',
            'description_rst': 'Description Test',
            'version': '10.0',
            'author': 'OCA',
            'depends': 'base',
            'external_dependencies': '{}',
        })

    def test_product_author_version_info(self):
        self.assertFalse(self.odoo_module2.product_template_id)
        self.odoo_module2.action_create_product()
        self.assertTrue(self.odoo_module2.product_template_id)
        self.odoo_module2.product_template_id.write({
            'attribute_line_ids': [(0, 0, {
                'attribute_id': self.attribute.id,
                'value_ids': [(6, 0, [self.version.id])],
            })]
        })
        action = self.odoo_module2.action_view_products()
        self.assertEqual(
            self.odoo_module2.product_template_id.product_variant_ids.ids[0],
            action['res_id']
        )
        self.odoo_module2.product_template_id.get_author_details()
        self.odoo_module2.product_template_id.get_version_info()
