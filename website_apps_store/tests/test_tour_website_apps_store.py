# -*- coding: utf-8 -*-

from odoo import tests


@tests.common.at_install(False)
@tests.common.post_install(True)
class TestUi(tests.HttpCase):

    def setUp(self):
        super(TestUi, self).setUp()
        self.tour = "odoo.__DEBUG__.services['web_tour.tour']"

    def test_download_zip_tour(self):
        self.phantom_js(
            "/shop",
            self.tour + ".run('download_zip')",
            self.tour + ".tours.download_zip.ready",
            login="admin"
        )

    def test_select_version_search_tour(self):
        self.phantom_js(
            "/shop",
            self.tour + ".run('select_version_search')",
            self.tour + ".tours.select_version_search.ready",
            login="admin"
        )

    def test_select_author_search_tour(self):
        self.phantom_js(
            "/shop",
            self.tour + ".run('select_author_search')",
            self.tour + ".tours.select_author_search.ready",
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
