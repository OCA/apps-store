# Copyright 2018 BizzAppDev
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Website Apps Store",
    "version": "11.0.3.0.0",
    'author': 'Odoo Community Association (OCA), BizzAppDev',
    "website": "https://github.com/OCA/apps-store",
    "license": "AGPL-3",
    "category": "Sales",
    "depends": [
        'website_sale',
        'website_form_recaptcha',
        'apps_download',
        'apps_product_creator',
    ],
    "summary": "Website Apps Store",
    "data": [
        'views/assets.xml',
        'views/templates.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False
}
