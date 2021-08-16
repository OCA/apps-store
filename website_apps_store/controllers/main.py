# Copyright 2017-2018 BizzAppDev
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import base64
import logging

from odoo import _, http
from odoo.exceptions import UserError, ValidationError
from odoo.http import request

from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website_sale.controllers.main import TableCompute, WebsiteSale

_logger = logging.getLogger(__name__)

PPG = 20  # Products Per Page
PPR = 4  # Products Per Row


class WebsiteSaleCustom(WebsiteSale):
    def _get_search_domain(
        self, search, category, attrib_values, search_in_description=True
    ):
        domain = request.website.sale_product_domain()
        if search:
            for srch in search.split(" "):
                domain += [
                    "|",
                    "|",
                    "|",
                    "|",
                    "|",
                    "|",
                    "|",
                    "|",
                    ("name", "ilike", srch),
                    ("technical_name", "ilike", srch),
                    ("description", "ilike", srch),
                    ("description_sale", "ilike", srch),
                    ("product_variant_ids.default_code", "ilike", srch),
                    (
                        "product_variant_ids.product_template_attribute_value_ids.name",
                        "ilike",
                        srch,
                    ),
                    ("product_variant_ids.app_description_rst_html", "ilike", srch),
                    ("product_variant_ids.app_author_ids.name", "ilike", srch),
                    ("product_variant_ids.app_summary", "ilike", srch),
                ]
        if category:
            domain += [("public_categ_ids", "child_of", int(category))]

        if attrib_values:
            attrib = None
            ids = []
            for value in attrib_values:
                if not attrib:
                    attrib = value[0]
                    ids.append(value[1])
                elif value[0] == attrib:
                    ids.append(value[1])
                else:
                    domain += [("attribute_line_ids.value_ids", "in", ids)]
                    attrib = value[0]
                    ids = [value[1]]
            if attrib:
                domain += [("attribute_line_ids.value_ids", "in", ids)]

        return domain

    @http.route()
    def shop(self, page=0, category=None, search="", ppg=False, **post):
        res = super().shop(page=page, category=category, search=search, ppg=ppg, **post)

        if ppg:
            try:
                ppg = int(ppg)
            except ValueError:
                ppg = PPG
            post["ppg"] = ppg
        else:
            ppg = PPG

        attrib_list = request.httprequest.args.getlist("attrib")
        attrib_values = [[int(x) for x in v.split("-")] for v in attrib_list if v]
        attributes_ids = {v[0] for v in attrib_values}
        attrib_set = {v[1] for v in attrib_values}
        domain = self._get_search_domain(search, category, attrib_values)

        keep = QueryURL(
            "/shop",
            category=category and int(category),
            search=search,
            attrib=attrib_list,
            order=post.get("order"),
            maturity=post.get("maturity"),
            version=post.get("version"),
            author=post.get("author"),
        )
        if post.get("version"):
            field_name = (
                "product_variant_ids.product_template_attribute_value_ids"
                + ".product_attribute_value_id.id"
            )
            domain += [
                (
                    field_name,
                    "=",
                    post.get("version"),
                )
            ]
        if post.get("author"):
            domain += [
                ("product_variant_ids.app_author_ids.id", "=", post.get("author"))
            ]
        if post.get("maturity", False):
            domain += [
                (
                    "product_variant_ids.app_development_status",
                    "=",
                    post.get("maturity"),
                )
            ]

        url = "/shop"
        if search:
            post["search"] = search
        if attrib_list:
            post["attrib"] = attrib_list

        if category:
            category = request.env["product.public.category"].browse(int(category))
            url = "/shop/category/%s" % slug(category)

        attribute_id = request.env.ref("apps_product_creator.attribute_odoo_version")
        category_all = request.env["product.public.category"].search([])
        versions = request.env["product.attribute.value"].search(
            [("attribute_id", "=", attribute_id.id)]
        )
        authors = request.env["odoo.author"].search([])
        Product = request.env["product.template"]

        product_count = Product.search_count(domain)
        pager = request.website.pager(
            url=url, total=product_count, page=page, step=ppg, scope=7, url_args=post
        )
        products = Product.search(
            domain,
            limit=ppg,
            offset=pager["offset"],
            order=self._get_search_order(post),
        )

        ProductAttribute = request.env["product.attribute"]
        if products:
            # get all products without limit
            selected_products = Product.search(domain, limit=False)
            attributes = ProductAttribute.search(
                [("attribute_line_ids.product_tmpl_id", "in", selected_products.ids)]
            )
        else:
            attributes = ProductAttribute.browse(attributes_ids)

        res.qcontext.update(
            {
                "search": search,
                "category": category,
                "attrib_values": attrib_values,
                "attrib_set": attrib_set,
                "pager": pager,
                "products": products,
                "search_count": product_count,  # common for all searchbox
                "bins": TableCompute().process(products, ppg),
                "category_all": category_all,
                "versions": versions,
                "authors": authors,
                "version": post.get("version"),
                "author": post.get("author"),
                "attributes": attributes,
                "keep": keep,
                "maturity": post.get("maturity"),
            }
        )
        return res

    @http.route(
        [
            '/shop/download_product_zip/<model("product.template"):product_tmpl>'
            '/<model("product.product"):product>/'
            "<string:recaptcha_token_response>",
            '/shop/download_product_zip/<model("product.template"):product_tmpl>/'
            "<string:recaptcha_token_response>",
        ],
        type="http",
        auth="public",
        website=True,
    )
    def download_product_zip(
        self, product_tmpl, product=False, recaptcha_token_response="", **kwargs
    ):
        request.params["recaptcha_token_response"] = recaptcha_token_response
        try:
            # The except clause below should not let what has been done inside
            # here be committed. It should not either roll back everything in
            # this controller method. Instead, we use a savepoint to roll back
            # what has been done inside the try clause.
            with request.env.cr.savepoint():
                if request.env["ir.http"]._verify_request_recaptcha_token(
                    "download_product_zip"
                ):
                    return self._handle_download_product_zip(product_tmpl, product)
            error = _("Suspicious activity detected by <b>Google reCaptcha<b/>.")
        except (ValidationError, UserError) as e:
            error = e.args[0]
        values = {"error_msg": error}
        return request.render("website_apps_store.suspicious_product_download", values)

    def _handle_download_product_zip(self, product_tmpl, product):
        if not product:
            product = product_tmpl.get_version_info()
        attachment = (
            request.env["ir.attachment"]
            .sudo()
            .search(
                [("res_id", "=", product.id), ("res_model", "=", product._name)],
                limit=1,
            )
        )
        if not attachment:
            product.sudo().generate_zip_file()
            attachment = (
                request.env["ir.attachment"]
                .sudo()
                .search(
                    [("res_id", "=", product.id), ("res_model", "=", product._name)],
                    limit=1,
                )
            )
        if attachment:
            filecontent = base64.b64decode(attachment.datas)
            disposition = 'attachment; filename="%s"' % attachment.name
            # increasing count for the product downloadg
            product.sudo().download_count += 1
            return request.make_response(
                filecontent,
                [
                    ("Content-Type", "application/zip, application/octet-stream"),
                    ("Content-Length", len(filecontent)),
                    ("Content-Disposition", disposition),
                ],
            )
        return False
