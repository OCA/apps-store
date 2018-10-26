# Copyright (C) 2017-Today: Odoo Community Association (OCA)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Github product creator',
    'summary': 'Create a product variant (by version) for every module found '
               'in the Github repositories',
    'version': '11.0.1.1.3',
    'category': 'Connector',
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
