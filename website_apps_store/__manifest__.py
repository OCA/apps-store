# Copyright 2018 BizzAppDev
# Copyright 2018-2021 Tecnativa
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Website Apps Store",
    "version": "18.0.1.0.0",
    "author": "Odoo Community Association (OCA), BizzAppDev",
    "website": "https://github.com/OCA/apps-store",
    "license": "AGPL-3",
    "category": "Sales",
    "depends": [
        "website_sale",
        "apps_download",
        "apps_product_creator",
    ],
    "summary": "Website Apps Store",
    "data": [
        "views/templates.xml",
        "views/suspicious_templates.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "website_apps_store/static/src/scss/main.scss",
            "website_apps_store/static/src/js/website_sale.js",
        ],
        "web.assets_tests": [
            "website_apps_store/static/src/js/website_apps_store_tour.js",
        ],
    },
    "installable": True,
    "auto_install": False,
    "application": False,
}
