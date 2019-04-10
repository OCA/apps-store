# Copyright (C) 2017-Today: Odoo Community Association (OCA)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
from odoo import tools
import lxml


def urljoin(*args):
    """
    Joins given arguments into an url. Trailing but not leading slashes are
    stripped for each argument.
    """

    return "/".join(map(lambda x: str(x).rstrip('/'), args))


def hook_github_image_url(rst_desc, github_url):
    html_node = lxml.html.fromstring(rst_desc)
    github_url = github_url.replace('/tree/', '/blob/')
    for node in html_node.xpath('//img'):
        if not node.attrib['src'].startswith("/"):
            continue
        node.attrib['src'] = urljoin(
            github_url, '/'.join(node.attrib['src'].split("/")[2:]),
            '?raw=true')
    return lxml.html.tostring(html_node)


class ProductProduct(models.Model):
    _inherit = 'product.product'

    odoo_module_version_id = fields.Many2one(
        'odoo.module.version',
        'Odoo Module Version',
    )
    app_license_id = fields.Many2one(
        comodel_name='odoo.license',
        string='License',
        readonly=True,
        related="odoo_module_version_id.license_id",
        store=True,
    )
    app_summary = fields.Char(
        'Summary (Manifest)',
        readonly=True,
        related="odoo_module_version_id.summary",
        store=True,
    )
    app_website = fields.Char(
        'Website (Manifest)',
        readonly=True,
        related="odoo_module_version_id.website",
        store=True,
    )
    app_description_rst_html = fields.Html(
        'HTML of the RST Description',
        compute='_compute_app_description_rst_html',
        readonly=True,
        store=True,
    )
    app_version = fields.Char(
        'Version (Manifest)',
        readonly=True,
        related="odoo_module_version_id.version",
        store=True,
    )
    app_author_ids = fields.Many2many(
        string='Authors', comodel_name='odoo.author',
        relation='product_module_author_rel',
        column1='product_id',
        column2='author_id',
        multi='author',
        related="odoo_module_version_id.author_ids",
        store=True,)
    app_github_url = fields.Char(
        'Github URL',
        readonly=True,
        related="odoo_module_version_id.github_url",
        store=True,
    )
    app_development_status = fields.Selection(
        'Module maturity',
        readonly=True,
        related="odoo_module_version_id.development_status",
        store=True,
    )

    @api.depends('odoo_module_version_id',
                 'odoo_module_version_id.description_rst_html')
    @api.multi
    def _compute_app_description_rst_html(self):
        for product in self:
            rst_desc = product.odoo_module_version_id.description_rst_html
            if rst_desc and '<img' in rst_desc:
                rst_desc = hook_github_image_url(
                    rst_desc, product.app_github_url)
            product.app_description_rst_html = rst_desc

    @api.model
    def create(self, values):
        self._manage_product_module(values)
        return super(ProductProduct, self).create(values)

    @api.model
    def _manage_product_module(self, values):
        """
        Manage product variants related to modules.
        During the creation of a new product.product (who is a variant), we
        check if the product is used to save a module (by the odoo_module_id
        field).
        Then check into given variant attributes if we find the variant used
        to save the module version (with XML ID:
        apps_product_creator.attribute_odoo_version).
        If it's the case, we check the version (based on the attribute value)
        and just link the product.product to this version
        :param values: dict
        :return: bool
        """
        product_tmpl_key = "product_tmpl_id"
        attr_key = "attribute_value_ids"
        check_keys = [
            product_tmpl_key,
            attr_key,
        ]
        values_keys = values.keys()
        # Check if mandatory keys (for product module) are given
        if all([k in values_keys for k in check_keys]):
            product_obj = self.env['product.template']
            module_version = self.env['odoo.module.version']
            product_variant = self.env['product.product']
            product = product_obj.browse(values.get(product_tmpl_key, []))
            # If the product template is used to save an Odoo module
            if self._check_related_to_module(product):
                attribute = self._get_version_attribute(values)
                versions = self._get_version_with_attribute(
                    product.odoo_module_id.module_version_ids, attribute)
                for version in versions:
                    module = version.module_id
                    mod_ver_ids = module.dependence_module_version_ids.ids
                    dependency_modules = module_version.search([
                        ('id', 'in', mod_ver_ids),
                        ('repository_branch_id', '=',
                         version.repository_branch_id.id)
                    ])
                    product_ids = []
                    for dep in dependency_modules:
                        product_variant_data = product_variant.search([
                            ('name', '=', dep.name),
                            ('odoo_module_version_id.module_id', '=',
                             dep.module_id.id),
                            ('attribute_value_ids.name', '=',
                             dep.repository_branch_id.name),
                        ])
                        if product_variant_data:
                            for pro in product_variant_data:
                                product_ids.append(pro.id)
                        if not product_variant_data:
                            product_data = dep.module_id._create_product()
                            product_variant_data = \
                                product_data.product_variant_ids.search([
                                    ('attribute_value_ids.name', '=',
                                     dep.repository_branch_id.name),
                                    ('odoo_module_version_id.module_id',
                                     '=', dep.module_id.id), ])
                            if product_variant_data:
                                product_ids.append(product_variant_data.id)
                            values.update({
                                'dependent_product_ids': [
                                    (6, 0, product_ids)
                                ] if product_ids else False,
                            })
                        else:
                            values.update({
                                'dependent_product_ids': [
                                    (6, 0, product_ids)
                                ] if product_ids else False,
                            })

                    # If we don't have a result, the ID will be False
                    values.update({
                        'odoo_module_version_id': version.id,
                    })
        return True

    @api.model
    def _get_version_with_attribute(self, versions, attribute):
        """
        Get the version recordset (odoo.module.version) into the given version
        (versions) based on the attribute name.
        :param versions: odoo.module.version recordset
        :param attribute: product.attribute.value recordset
        :return: odoo.module.version recordset
        """
        # Attribute value (so the name field) must be the serie name
        # (so the version). So we can compare name without managing
        # translations.
        version = versions.filtered(
            lambda x: x.organization_serie_id.name == attribute.name)
        return version

    @api.model
    def _check_related_to_module(self, product):
        """
        Check if the product template is related to a module or not
        :param product: product.template recordset
        :return: bool
        """
        return bool(product.odoo_module_id)

    @api.model
    def _get_version_attribute(self, values):
        """
        Get the attribute value used to save the Module version (using the
        xml id) if it's into the given dict values.
        :param values: dict
        :return: product.attribute.value recordset (0 or 1 recordset)
        """
        attr_obj = self.env['product.attribute.value']
        attr_xml_id = "apps_product_creator.attribute_odoo_version"
        attr_key = "attribute_value_ids"
        version_attribute = self.env.ref(attr_xml_id)
        attr_raw_ids = values.get(attr_key, [])
        attr_ids = []
        # The MAGIC NUMBER used to create variants are (6, _, list) so we must
        # have the last element of the tuple
        if attr_raw_ids and len(attr_raw_ids[0]) > 1:
            attr_ids = attr_raw_ids[0][2]
        attributes = attr_obj.browse(attr_ids)
        # We should have 0 or 1 result maximum. Because we compare id.
        attribute = attributes.filtered(
            lambda a: a.attribute_id.id == version_attribute.id)
        return attribute

    @api.multi
    @api.depends('image_variant', 'product_tmpl_id.image', 'image_module',
                 'odoo_module_version_id')
    def _compute_images(self):
        products = self.filtered(
            lambda p: p.odoo_module_version_id and p.image_module)
        other_products = self.filtered(lambda p: p not in products)
        for product in products:
            if self._context.get('bin_size'):
                product.image_medium = product.image_module
                product.image_small = product.image_module
                product.image = product.image_module
            else:
                resized_images = tools.image_get_resized_images(
                    product.image_module, return_big=True,
                    avoid_resize_medium=True)
                product.image_medium = resized_images.get('image_medium')
                product.image_small = resized_images.get('image_small')
                product.image = resized_images.get('image')
            if not product.image_medium:
                product.image_medium = product.product_tmpl_id.image_medium
            if not product.image_small:
                product.image_small = product.product_tmpl_id.image_small
            if not product.image:
                product.image = product.product_tmpl_id.image
        if other_products:
            super(ProductProduct, other_products)._compute_images()
