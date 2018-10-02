# Copyright 2017-2018 BizzAppDev
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import tests
import mock
import os

mock_get_module_path = (
    'odoo.addons.apps_download.models.product_product.ProductProduct'
    '._get_module_path'
)


@tests.common.at_install(False)
@tests.common.post_install(True)
class TestUi(tests.HttpCase):

    def setUp(self):
        super(TestUi, self).setUp()
        self.tour = "odoo.__DEBUG__.services['web_tour.tour']"

    def test_download_zip_tour(self):
        test_path = os.path.dirname(os.path.realpath(__file__))
        test_path = test_path.split('/website_apps_store')[0]
        test_module_path = os.path.join(
            test_path + '/apps_download' + '/tests', 'test_modules',
            'second_module')
        with mock.patch(mock_get_module_path) as mock_func:
            mock_func.return_value = test_module_path
            self.phantom_js(
                "/shop", self.tour + ".run('download_zip')",
                self.tour + ".tours.download_zip.ready", login="admin"
            )

    def test_select_version_search_tour(self):
        self.phantom_js(
            "/shop",
            self.tour + ".run('select_version_search')",
            self.tour + ".tours.select_version_search.ready",
            login="admin"
        )

    def test_select_category_search_tour(self):
        self.phantom_js(
            "/shop",
            self.tour + ".run('select_category_search')",
            self.tour + ".tours.select_category_search.ready",
            login="admin"
        )

    def test_module_search_tour(self):
        self.phantom_js(
            "/shop",
            self.tour + ".run('module_search')",
            self.tour + ".tours.module_search.ready",
            login="admin"
        )
