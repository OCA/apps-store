# Copyright 2017-2018 Odoo Community Association (OCA)
# Copyright 2019 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Github product creator',
    'summary': 'Create a product variant (by version) for every module found '
               'in the Github repositories',
    'version': '12.0.1.0.0',
    'category': 'Connector',
    'website': 'https://github.com/OCA/apps-store',
    'license': 'AGPL-3',
    'author': 'Odoo Community Association (OCA), BizzAppDev',
    'depends': [
        'github_connector_oca',
        'github_connector_odoo',
        'product',
        'website_sale',
    ],
    'data': [
        'data/ir_cron.xml',
        'data/product_attribute.xml',
        'data/product_public_categ_data.xml',
        'views/view_odoo_module.xml',
        'views/view_product_product.xml',
    ],
    'installable': True,
}
