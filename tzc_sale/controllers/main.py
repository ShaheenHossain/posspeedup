# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import json
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

_logger = logging.getLogger(__name__)


class WebsiteSale(http.Controller):

    @http.route(['/shop/catalog'], type='http', auth="public", website=True)
    def catalog(self, access_token=None, revive='', **post):
        """
        Main catalog management + abandoned cart revival
        access_token: Abandoned cart SO access token
        revive: Revival method when abandoned cart. Can be 'merge' or 'squash'
        """
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

    @http.route(['/shop/catalog/update'], type='http', auth="public", methods=['POST'], website=True, csrf=False)
    def catalog_update(self, product_id, add_qty=1, set_qty=0, **kw):
        request.website.sale_get_catalog_order()._catalog_update(
            product_id=int(product_id),
            add_qty=add_qty,
            set_qty=set_qty,
            attributes=self._filter_attributes(**kw),
        )
        return request.redirect("/shop/catalog")

    @http.route(['/shop/catalog/update_json'], type='json', auth="public", methods=['POST'], website=True, csrf=False)
    def catalog_update_json(self, product_id, line_id=None, add_qty=None, set_qty=None, display=True):
        order = request.website.sale_get_catalog_order()
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
            'suggested_products': []
        })
        return value