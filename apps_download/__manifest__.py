# Copyright 2017-2018 BizzAppDev
# Copyright 2017 AgentERP
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Product Download for Appstore",
    "version": "11.0.2.0.1",
    "author": "BizzAppDev, AgentERP, Elico Corp, "
    "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/apps-store",
    "license": "AGPL-3",
    "category": "Sales",
    "depends": [
        'base',
        'website_sale_digital',
        'github_connector_odoo',
        'apps_product_creator',
    ],
    "summary": "Product Download for Appstore",
    "data": [
        'views/product_template_view.xml',
        'data/cron_scheduler.xml',
    ],
    'demo': [
        'demo/product_template_demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False
}
