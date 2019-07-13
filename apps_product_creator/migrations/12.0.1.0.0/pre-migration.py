# Copyright 2019 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


def assign_new_version_attribute_xml_id(env):
    """This checks if 12.0 attribute has been manually added in previous
    version, so assigning the XML-ID for avoiding duplicate constraint error.
    """
    attrib = env.ref('apps_product_creator.attribute_odoo_version')
    value = env['product.attribute.value'].search([
        ('attribute_id', '=', attrib.id),
        ('name', '=', '12.0'),
    ])
    if value:
        env['ir.model.data'].create({
            'module': 'apps_product_creator',
            'name': 'odoo_version_120',
            'model': value._name,
            'res_id': value.id,
            'noupdate': True,
        })


@openupgrade.migrate()
def migrate(env, version):
    assign_new_version_attribute_xml_id(env)
