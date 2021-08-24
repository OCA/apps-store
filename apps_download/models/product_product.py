# Copyright (C) 2017-Today: Odoo Community Association (OCA)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


import base64
import logging
import os
import shutil
import tempfile
import time

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    _inherit = "product.product"

    module_path = fields.Char(
        related="odoo_module_version_id.repository_branch_id.local_path", readonly=True
    )

    @api.constrains("dependent_product_ids")
    def check_dependent_recursion(self):
        if not self._check_m2m_recursion("dependent_product_ids"):
            raise ValidationError(_("Error: You cannot create recursive dependency."))

    @api.model
    def child_dependency(self, children):
        res = self.env["product.product"]
        for child in children:
            if not child.dependent_product_ids:
                continue
            res |= child.dependent_product_ids
            res |= self.child_dependency(child.dependent_product_ids)
        return res

    def create_dependency_list(self):
        ret_val = {}
        for product in self:
            ret_val[product.id] = product.dependent_product_ids
            if product.dependent_product_ids:
                ret_val[product.id] |= self.child_dependency(
                    product.dependent_product_ids
                )
        return ret_val

    def _get_module_path(self):
        return self.module_path + "/" + self.odoo_module_version_id.technical_name

    def generate_zip_file(self):
        for product in self.filtered("module_path"):
            tmp_dir = tempfile.mkdtemp()
            tmp_dir_2 = tempfile.mkdtemp()
            dependent_products = product.create_dependency_list()
            dependent_products = dependent_products[product.id]

            for dependent_pro in dependent_products.filtered("module_path"):
                tmp_module_path = os.path.join(
                    tmp_dir, dependent_pro.odoo_module_version_id.technical_name
                )
                shutil.copytree(
                    dependent_pro.module_path
                    + "/"
                    + dependent_pro.odoo_module_version_id.technical_name,
                    tmp_module_path,
                )

            tmp_module_path = os.path.join(
                tmp_dir, product.odoo_module_version_id.technical_name
            )
            module_path = product._get_module_path()
            try:
                shutil.copytree(module_path, tmp_module_path)
            except FileNotFoundError:
                raise UserError(
                    _(
                        "Module code not downloaded yet."
                        " Please initialize the code in the associated"
                        " Github Repository Branch by downloading the source code."
                    )
                )
            time_version_value = time.strftime("_%y%m%d_%H%M%S")
            attr_values = product.product_template_attribute_value_ids
            if attr_values:
                time_version_value = "_{}{}".format(
                    "_".join(
                        [name.replace(".", "_") for name in attr_values.mapped("name")]
                    ),
                    time_version_value,
                )

            tmp_zip_file = os.path.join(tmp_dir_2, product.name) + time_version_value
            shutil.make_archive(tmp_zip_file, "zip", tmp_dir)
            tmp_zip_file = "%s.zip" % tmp_zip_file
            with open(tmp_zip_file, "rb") as file_obj:
                try:
                    data_encode = base64.encodestring(file_obj.read())
                    self.env["ir.attachment"].create(
                        {
                            "datas": data_encode,
                            "store_fname": (
                                product.name.replace(" ", "-")
                                + time_version_value
                                + ".zip"
                            ),
                            "type": "binary",
                            "name": product.name + time_version_value + ".zip",
                            "res_model": product._name,
                            "res_id": product.id,
                            "product_downloadable": True,
                        }
                    )
                except Exception as exc:
                    _logger.error(
                        "Error creating attachment %s Error is: %s"
                        % (tmp_zip_file, str(exc))
                    )
            try:
                shutil.rmtree(tmp_dir)
            except OSError as exc:
                _logger.warning(
                    "Could not remove Tempdir {}, Errormsg {}".format(tmp_dir, str(exc))
                )
            try:
                shutil.rmtree(tmp_dir_2)
            except OSError as exc:
                _logger.warning(
                    "Could not remove Tempdir 2 {}, Errormsg {}".format(
                        tmp_dir, str(exc)
                    )
                )

    @api.model
    def generate_zip_file_batch(self):
        self.search([]).generate_zip_file()
