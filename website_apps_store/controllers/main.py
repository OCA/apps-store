# -*- coding: utf-8 -*-
# Copyright 2018 BizzAppDev
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
import base64

from odoo import http
from odoo.http import request
from odoo.addons.website.models.website import slug
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website_sale.controllers.main import WebsiteSale, TableCompute

_logger = logging.getLogger(__name__)

PPG = 20  # Products Per Page
PPR = 4   # Products Per Row


class WebsiteSaleCustom(WebsiteSale):

    def _get_search_domain(self, search, category, attrib_values):
        domain = request.website.sale_product_domain()
        if search:
            for srch in search.split(" "):
                domain += [
                    '|', '|', '|', '|', '|', '|', '|', ('name', 'ilike', srch),
                    ('description', 'ilike', srch),
                    ('description_sale', 'ilike', srch),
                    ('product_variant_ids.default_code', 'ilike', srch),
                    ('product_variant_ids.attribute_value_ids.name',
                     'ilike', srch),
                    ('product_variant_ids.app_description_rst_html',
                     'ilike', srch),
                    ('product_variant_ids.app_author_ids.name', 'ilike', srch),
                    ('product_variant_ids.app_summary', 'ilike', srch)]
        if category:
            domain += [('public_categ_ids', 'child_of', int(category))]

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
                    domain += [('attribute_line_ids.value_ids', 'in', ids)]
                    attrib = value[0]
                    ids = [value[1]]
            if attrib:
                domain += [('attribute_line_ids.value_ids', 'in', ids)]

        return domain

    @http.route([
        '/shop',
        '/shop/page/<int:page>',
        '/shop/category/<model("product.public.category"):category>',
        '/shop/category/<model("product.public.category"):category>\
        /page/<int:page>'
    ], type='http', auth="public", website=True)
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        res = super(WebsiteSaleCustom, self).shop(
            page=page, category=category, search=search, ppg=ppg, **post)

        if ppg:
            try:
                ppg = int(ppg)
            except ValueError:
                ppg = PPG
            post["ppg"] = ppg
        else:
            ppg = PPG

        attrib_list = request.httprequest.args.getlist('attrib')
        attrib_values = [map(int, v.split("-")) for v in attrib_list if v]
        attributes_ids = set([v[0] for v in attrib_values])
        attrib_set = set([v[1] for v in attrib_values])
        domain = self._get_search_domain(search, category, attrib_values)

        keep = QueryURL('/shop', category=category and int(category),
                        search=search, attrib=attrib_list,
                        order=post.get('order'),
                        version=post.get('version'), author=post.get('author'))
        if post.get('version'):
            domain += [('product_variant_ids.attribute_value_ids.id',
                        '=', post.get('version'))]
        if post.get('author'):
            domain += [('product_variant_ids.app_author_ids.id',
                        '=', post.get('author'))]

        url = "/shop"
        if category:
            category = request.env['product.public.category'].browse(
                int(category))
            url = "/shop/category/%s" % slug(category)

        category_all = request.env['product.public.category'].search([])
        versions = request.env['product.attribute.value'].search([])
        authors = request.env['odoo.author'].search([])
        Product = request.env['product.template']

        product_count = Product.search_count(domain)
        pager = request.website.pager(url=url, total=product_count,
                                      page=page, step=ppg,
                                      scope=7, url_args=post)
        products = Product.search(domain, limit=ppg, offset=pager['offset'],
                                  order=self._get_search_order(post))

        ProductAttribute = request.env['product.attribute']
        if products:
            # get all products without limit
            selected_products = Product.search(domain, limit=False)
            attributes = ProductAttribute.search(
                [('attribute_line_ids.product_tmpl_id', 'in',
                  selected_products.ids)])
        else:
            attributes = ProductAttribute.browse(attributes_ids)

        res.qcontext.update({
            'search': search,
            'category': category,
            'attrib_values': attrib_values,
            'attrib_set': attrib_set,
            'pager': pager,
            'products': products,
            'search_count': product_count,  # common for all searchbox
            'bins': TableCompute().process(products, ppg),
            'category_all': category_all,
            'versions': versions,
            'authors': authors,
            'version': post.get('version'),
            'author': post.get('author'),
            'attributes': attributes,
            'keep': keep,
        })
        return res

    @http.route(['/shop/change_attribute_version'], type='json',
                auth="public", website=True)
    def change_product_attribute_version(self, **kwargs):
        product_id = kwargs.get('product_id', False)
        product = request.env['product.product'].browse(product_id)
        vals = {
            'name_product': product.name,
            'technical_name':
                product.odoo_module_version_id.module_id.technical_name,
            'license': product.app_license_id.name,
            'license_url': product.app_license_id.website,
            'author': ', '.join(
                author.name for author in product.app_author_ids),
            'website': product.app_website,
            'repository': product.app_github_url,
            'rst_html': product.app_description_rst_html,
            'app_summary': product.app_summary,
        }
        return vals

    @http.route('/shop/cart/download_source', type='json',
                auth="public", website=True)
    def download_source_product(self, **kwargs):
        product_id = kwargs.get('product_id', False)
        tmpl_id = kwargs.get('product_template_id', False)
        product = request.env['product.product'].browse(product_id)
        if not product:
            product_tmpl = request.env['product.template'].browse(tmpl_id)
            product = product_tmpl.get_version_info()
        return product.id

    @http.route(
        '/shop/download_product_zip/<model("product.product"):product>',
        type='http', auth="public", website=True)
    def download_product_zip(self, product, **kwargs):
        attachment = request.env['ir.attachment'].search([
            ('res_id', '=', product.id),
            ('res_model', '=', product._name),
        ], limit=1)
        if not attachment:
            product.generate_zip_file()
            attachment = request.env['ir.attachment'].search([
                ('res_id', '=', product.id),
                ('res_model', '=', product._name),
            ], limit=1)

        if attachment:
            filecontent = base64.b64decode(attachment.datas)
            disposition = 'attachment; filename=%s' % attachment.datas_fname
            return request.make_response(
                filecontent,
                [('Content-Type', 'application/zip, application/octet-stream'),
                 ('Content-Length', len(filecontent)),
                 ('Content-Disposition', disposition)])
        return False
