# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import json
import requests
import logging
from werkzeug.exceptions import Forbidden, NotFound

from odoo import http, tools, _
from odoo.http import request
from odoo.addons.base.ir.ir_qweb.fields import nl2br
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website.controllers.main import QueryURL
from odoo.exceptions import ValidationError
from odoo.addons.website.controllers.main import Website
from odoo.addons.website_form.controllers.main import WebsiteForm
from odoo.osv import expression
from odoo.addons.website_sale.controllers.main import WebsiteSale

_logger = logging.getLogger(__name__)


class WebsiteSale(WebsiteSale):

    @http.route(['/shop/catalog/product/<model("product.template"):product>'], type='http', auth="public", website=True)
    def catalog_product(self, product, category='', search='', **kwargs):
        product_context = dict(request.env.context,
                               active_id=product.id,
                               partner=request.env.user.partner_id)

        ProductCategory = request.env['product.public.category']

        if category:
            category = ProductCategory.browse(int(category)).exists()

        attrib_list = request.httprequest.args.getlist('attrib')
        attrib_values = [[int(x) for x in v.split("-")] for v in attrib_list if v]
        attrib_set = {v[1] for v in attrib_values}

        keep = QueryURL('/shop', category=category and category.id, search=search, attrib=attrib_list)

        categs = ProductCategory.search([('parent_id', '=', False)])

        pricelist = request.website.get_current_pricelist()

        from_currency = request.env.user.company_id.currency_id
        to_currency = pricelist.currency_id
        compute_currency = lambda price: from_currency.compute(price, to_currency)

        if not product_context.get('pricelist'):
            product_context['pricelist'] = pricelist.id
            product = product.with_context(product_context)

        values = {
            'search': search,
            'category': category,
            'pricelist': pricelist,
            'attrib_values': attrib_values,
            'compute_currency': compute_currency,
            'attrib_set': attrib_set,
            'keep': keep,
            'categories': categs,
            'main_object': product,
            'product': product,
            'get_attribute_value_ids': self.get_attribute_value_ids,
            'from_catalog': 1,
        }

        return request.render("website_sale.product", values)


    @http.route(['/shop/catalog'], type='http', auth="public", website=True)
    def catalog(self, access_token=None, revive='', **post):
        """
        Main catalog management + abandoned cart revival
        access_token: Abandoned cart SO access token
        revive: Revival method when abandoned cart. Can be 'merge' or 'squash'
        """

        if request.env.user != request.env.ref('base.public_user'):

            order = request.website.sale_get_catalog_order()
            values = {}
            if access_token:
                order = request.env['sale.order'].sudo().search([('access_token', '=', access_token), ('catalog_id', '!=', False)], limit=1)
            if order and not order.catalog_viewed:
                order.sudo().write({'catalog_viewed': True})

            values.update({
                'website_catalog_order': order,
                'suggested_products': [],
            })

            # if post.get('type') == 'popover':
            #     # force no-cache so IE11 doesn't cache this XHR
            #     return request.render("website_sale.catalog_popover", values, headers={'Cache-Control': 'no-cache'})

            return request.render("tzc_sale.catalog", values)
        else:
            return request.redirect('/web/login?redirect=%s' % request.httprequest.path)

    @http.route(['/shop/catalog/update'], type='http', auth="public", methods=['POST'], website=True, csrf=False)
    def catalog_update(self, product_id, add_qty=1, set_qty=0, **kw):
        value = request.website.sale_get_catalog_order()._catalog_update(
            product_id=int(product_id),
            add_qty=add_qty,
            set_qty=set_qty,
            attributes=self._filter_attributes(**kw),
        )
        return request.redirect("/shop/catalog")

    @http.route(['/shop/catalog/update_json'], type='json', auth="public", methods=['POST'], website=True, csrf=False)
    def catalog_update_json(self, product_id, line_id=None, add_qty=None, set_qty=None, display=True):
        order = request.website.sale_get_catalog_order()
        # this should not happen?
        if order.state not in ('draft', 'sent'):
            request.website.catalog_reset()
            return {}
        value = order._catalog_update(product_id=product_id, line_id=line_id, add_qty=add_qty, set_qty=set_qty)

        order = request.website.sale_get_catalog_order()
        from_currency = order.company_id.currency_id
        to_currency = order.pricelist_id.currency_id

        if not display:
            return value

        value['tzc_sale.catalog_lines'] = request.env['ir.ui.view'].render_template("tzc_sale.catalog_lines", {
            'website_catalog_order': order,
            'compute_currency': lambda price: from_currency.compute(price, to_currency),
            'suggested_products': [],
        })
        return value

    @http.route(['/shop/catalog/confirm'], type='http', auth="public", website=True)
    def confirm_order(self, **post):
        order = request.website.sale_get_catalog_order()
        # print(order)
        # order.action_confirm()
        if order:
            # todo: check qty here to see if try to buy more than already have
            return request.redirect("/my/orders/{}".format(str(order.id)))
        else:
            return request.redirect("/shop/catalog")