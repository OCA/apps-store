# -*- coding: utf-8 -*-

import logging
import os
import tempfile
import shutil
import base64
import time

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
                    '|', '|', '|', '|', '|', '|', ('name', 'ilike', srch),
                    ('description', 'ilike', srch),
                    ('description_sale', 'ilike', srch),
                    ('product_variant_ids.default_code', 'ilike', srch),
                    ('product_variant_ids.attribute_value_ids.name',
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
        pricelist_context = dict(request.env.context)
        if not pricelist_context.get('pricelist'):
            pricelist = request.website.get_current_pricelist()
            pricelist_context['pricelist'] = pricelist.id
        else:
            pricelist = request.env['product.pricelist'].browse(
                pricelist_context['pricelist'])

        request.context = dict(request.context, pricelist=pricelist.id,
                               partner=request.env.user.partner_id)
        if post.get('version'):
            domain += [('product_variant_ids.attribute_value_ids.name',
                        'ilike', post.get('version'))]
        if post.get('author'):
            domain += [('product_variant_ids.app_author_ids.name',
                        'ilike', post.get('author'))]

        url = "/shop"
        if search:
            post["search"] = search
        if category:
            category = request.env['product.public.category'].browse(
                int(category))
            url = "/shop/category/%s" % slug(category)
        if attrib_list:
            post['attrib'] = attrib_list

        categs = request.env['product.public.category'].search(
            [('parent_id', '=', False)])
        versions = request.env['product.attribute.value'].search([])
        authors = request.env['odoo.author'].search([])
        Product = request.env['product.template']

        parent_category_ids = []
        if category:
            parent_category_ids = [category.id]
            current_category = category
            while current_category.parent_id:
                parent_category_ids.append(current_category.parent_id.id)
                current_category = current_category.parent_id

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

        from_currency = request.env.user.company_id.currency_id
        to_currency = pricelist.currency_id
        compute_currency = lambda price: from_currency.compute(
            price, to_currency)

        values = {
            'search': search,
            'category': category,
            'attrib_values': attrib_values,
            'attrib_set': attrib_set,
            'pager': pager,
            'pricelist': pricelist,
            'products': products,
            'search_count': product_count,  # common for all searchbox
            'bins': TableCompute().process(products, ppg),
            'rows': PPR,
            'categories': categs,
            'versions': versions,
            'authors': authors,
            'attributes': attributes,
            'compute_currency': compute_currency,
            'keep': keep,
            'parent_category_ids': parent_category_ids,
        }
        if category:
            values['main_object'] = category
        return request.render("website_sale.products", values)

    @http.route(['/shop/change_attribute_version'], type='json',
                auth="public", website=True)
    def change_product_attribute_version(self, **kwargs):
        product_id = kwargs.get('product_id', False)
        product = request.env['product.product'].browse(product_id)
        vals = {
            'technical_name': product.odoo_module_version_id.name,
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
            product = product_tmpl.product_variant_ids[-1]
        return product.id

    @http.route(
        '/shop/download_product_zip/<model("product.product"):product>',
        type='http', auth="public", website=True)
    def download_product_zip(self, product, **kwargs):
        tmp_dir = tempfile.mkdtemp()
        tmp_module_path = os.path.join(
            tmp_dir, os.path.split(product.module_path)[-1])
        module_path = product.module_path + '/'\
            + product.odoo_module_version_id.module_id.technical_name
        tmp_module_path = tmp_module_path + '/'\
            + product.odoo_module_version_id.module_id.technical_name
        shutil.copytree(module_path, tmp_module_path)
        time_version_value = time.strftime(
            '_%y%m%d_%H%M%S')
        if product.attribute_value_ids:
            time_version_value = '_%s%s' % (
                '_'.join([name.replace('.', '_') for name in
                          product.attribute_value_ids.mapped('name')]),
                time_version_value)

        tmp_zip_file = (os.path.join(product.name) +
                        time_version_value)
        shutil.make_archive(tmp_zip_file, 'zip', tmp_dir)
        tmp_zip_file = '%s.zip' % tmp_zip_file
        with open(tmp_zip_file, "rb") as file_obj:
            data_encode = base64.encodestring(file_obj.read())
        filecontent = base64.b64decode(data_encode)
        disposition = 'attachment; filename=%s' % tmp_zip_file
        return request.make_response(
            filecontent, [('Content-Type', 'application/csv'),
                          ('Content-Length', len(filecontent)),
                          ('Content-Disposition', disposition)])
