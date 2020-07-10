# Copyright (C) 2017-Today: Odoo Community Association (OCA)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class OdooModule(models.Model):
    _inherit = "odoo.module"

    @api.depends("product_template_id", "product_template_id.product_variant_ids")
    def _compute_product_qty(self):
        for module in self:
            module.product_qty = len(module.product_template_id.product_variant_ids)

    product_template_id = fields.Many2one("product.template", "Product Template",)
    product_qty = fields.Integer(
        "# of Products", compute="_compute_product_qty", store=True
    )

    def action_view_products(self):
        action = self.env.ref("product.product_normal_action_sell")
        result = action.read()[0]
        product_ids = self.mapped("product_template_id.product_variant_ids").ids
        # choose the view_mode accordingly
        if len(product_ids) > 1:
            result["domain"] = "[('id','in', %s)]" % str(product_ids)
        elif len(product_ids) == 1:
            res = self.env.ref("product.product_normal_form_view", False)
            result["views"] = [(res and res.id or False, "form")]
            result["res_id"] = product_ids[0]
        return result

    def action_create_product(self):
        self._create_product()

    def action_update_product(self):
        self._update_product()

    def _create_product(self):
        """
        Create the product template related to the module in current recordset.
        :return: product.template recordset
        """
        product_obj = self.env["product.template"]
        products = self.env["product.template"]
        modules = self.filtered(lambda m: not m.product_template_id)
        domain = [
            ("odoo_module_id", "in", modules.ids),
        ]
        matching_products = product_obj.search(domain)
        for odoo_module in modules:
            product = matching_products.filtered(
                lambda p: p.odoo_module_id == odoo_module
            )
            if not product and not odoo_module.product_template_id:
                product_values = odoo_module._prepare_template()
                new_product = product_obj.create(product_values)
                odoo_module.write({"product_template_id": new_product.id})
                products |= new_product
        return products

    def _update_product(self):
        attribute = self.env.ref("apps_product_creator.attribute_odoo_version")
        attribute_val = self.env["product.attribute.value"]
        modules = self.filtered("product_template_id")
        self._update_series_product_attribute_values()
        for module in modules:
            series = module.module_version_ids.mapped(
                "repository_branch_id.organization_serie_id.name"
            )
            product = module.product_template_id
            att_line = product.attribute_line_ids.filtered(
                lambda a: a.attribute_id.id == attribute.id
            )
            att_vals = att_line.mapped("value_ids.name")
            to_update_vals = list(set(series) - set(att_vals))
            att_val_ids = attribute_val.search(
                [("name", "in", to_update_vals), ("attribute_id", "=", attribute.id)]
            )
            att_line.write({"value_ids": [[4, record.id] for record in att_val_ids]})
            product._create_variant_ids()

    @api.model
    def _update_series_product_attribute_values(self):
        attribute = self.env.ref("apps_product_creator.attribute_odoo_version")
        attribute_val = self.env["product.attribute.value"]
        series = self.env["github.organization.serie"].search([])
        for serie in series:
            attribute_val = attribute_val.search([("name", "=", serie.name)], limit=1)
            if not attribute_val:
                attribute_val.create({"name": serie.name, "attribute_id": attribute.id})

    def _prepare_template(self):
        """
        Create the dict to create a product.template recordset based on the
        current recordset.
        The values dict contains info to link the future product with the
        current module. It also fill the name of the future product with the
        name of the current module.
        :return: dict
        """
        self.ensure_one()
        attribute_obj = self.env["product.attribute.value"]
        categ_obj = self.env["product.public.category"]
        series = self.module_version_ids.mapped(
            "repository_branch_id.organization_serie_id.name"
        )
        attributes = attribute_obj.search([("name", "in", series)])
        attribute = self.env.ref("apps_product_creator.attribute_odoo_version")
        attribute_line_values = {
            "attribute_id": attribute.id,
            "value_ids": [(6, 0, attributes.ids)],
        }
        version_categ = self.module_version_ids.mapped("category_id")
        category = False
        if version_categ:
            category = categ_obj.search([("name", "=", version_categ[0].name)], limit=1)
        if not category:
            category = self.env.ref("apps_product_creator.other")
        values = {
            "odoo_module_id": self.id,
            "type": "service",
            "name": self.name,
            "purchase_ok": False,
            "list_price": 0,
            "standard_price": 0,
            "image_1920": self.image,
            "attribute_line_ids": [(0, 0, attribute_line_values)],
            "public_categ_ids": [(4, category._ids)] or None,
            "website_published": True,
        }
        return values

    def write(self, values):
        to_update = "image" in values
        result = super().write(values)
        if to_update:
            for odoo_module in self.filtered("product_template_id"):
                odoo_module.product_template_id.write({"image_1920": odoo_module.image})
        return result

    @api.model
    def cron_create_product(self):
        modules = self.search(
            [("product_template_id", "=", False), ("module_version_qty", "!=", 0)]
        )
        modules.action_create_product()
        # Calling Update product for updating/creating new product Variants
        # based on new versions added
        modules = self.search([("module_version_qty", "!=", 0)])
        modules.action_update_product()
        return True

    @api.model
    def cron_update_product(self):
        return True
