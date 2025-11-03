# Copyright 2017-2018 BizzAppDev
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import os
from unittest import mock

from odoo.tests import HttpCase, tagged

mock_get_module_path = (
    "odoo.addons.apps_download.models.product_product.ProductProduct._get_module_path"
)
mock_verify_recaptcha_token = (
    "odoo.addons.google_recaptcha.models.ir_http.Http._verify_recaptcha_token"
)


@tagged("post_install", "-at_install")
class TestUi(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env.ref("website_sale.products").active = True
        cls._req_patcher = mock.patch(
            "odoo.addons.github_connector_odoo.models.github_repository.requests.get"
        )
        cls._mock_get = cls._req_patcher.start()
        cls.addClassCleanup(cls._req_patcher.stop)
        resp = mock.MagicMock()
        resp.status_code = 200
        resp.text = "login/Repository1 1234\n"
        resp.json.return_value = ["login/Repository1 1234"]
        resp.iter_lines.return_value = [b"login/Repository1 1234"]
        resp.raise_for_status.return_value = None
        resp.__iter__.return_value = iter([b"login/Repository1 1234"])
        cls._mock_get.return_value = resp

        cls.env["product.public.category"].create({"name": "Category"})
        cls.organization = cls.env.ref("github_connector.oca_organization")

        cls.organization_serie = cls.env["github.organization.serie"].create(
            {"name": "14.0", "sequence": 1, "organization_id": cls.organization.id}
        )
        cls.repository = cls.env["github.repository"].create(
            {"name": "Repository1", "organization_id": cls.organization.id}
        )
        cls.branch = cls.env["github.repository.branch"].create(
            {
                "name": "14.0",
                "repository_id": cls.repository.id,
                "organization_id": cls.organization.id,
            }
        )
        cls.odoo_module = cls.env["odoo.module"].create(
            {"technical_name": "odoo_module"}
        )
        cls.attribute = cls.env.ref("apps_product_creator.attribute_odoo_version")
        cls.version = cls.env.ref("apps_product_creator.odoo_version_140")
        cls.env["odoo.module.version"].create(
            {
                "name": "Odoo Module",
                "technical_name": "odoo_module",
                "module_id": cls.odoo_module.id,
                "repository_branch_id": cls.branch.id,
                "license": "AGPL-3",
                "summary": "Summary Test",
                "website": "Website Test",
                "description_rst": "Description Test",
                "version": "14.0",
                "author": "OCA",
                "depends": "base",
                "external_dependencies": "{}",
            }
        )
        cls.odoo_module.action_create_product()

    def test_successfully_download_zip_tour(self):
        test_path = os.path.dirname(os.path.realpath(__file__))
        test_path = test_path.split("/website_apps_store")[0]
        test_module_path = os.path.join(
            test_path + "/apps_download" + "/tests", "test_modules", "second_module"
        )
        with mock.patch(mock_get_module_path) as mock_mod_path:
            mock_mod_path.return_value = test_module_path
            with mock.patch(mock_verify_recaptcha_token) as mock_verify:
                mock_verify.return_value = "is_human"
                self.start_tour(
                    "/shop/page/2", "successfully_download_zip", login="admin"
                )

    def test_download_zip_failed_tour(self):
        with mock.patch(mock_verify_recaptcha_token) as mock_verify:
            mock_verify.return_value = "is_bot"
            self.start_tour("/shop/page/2", "download_zip_failed", login="admin")

    def test_select_version_search_tour(self):
        self.start_tour("/shop", "select_version_search", login="admin")

    def test_select_category_search_tour(self):
        self.start_tour("/shop", "select_category_search", login="admin")

    def test_module_search_tour(self):
        self.start_tour("/shop", "module_search", login="admin")

    def test_technical_name_search_tour(self):
        self.start_tour("/shop", "technical_name_search", login="admin")
