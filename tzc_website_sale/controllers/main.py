# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSalePortal(WebsiteSale):
    @http.route([
        '/shop',
        '/shop/page/<int:page>',
        '/shop/category/<model("product.public.category"):category>',
        '/shop/category/<model("product.public.category"):category>/page/<int:page>'
    ], type='http', auth="public", website=True)
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        if not request.session.login:
            return request.redirect('/web/login?redirect=%s' % request.httprequest.path)
        return super(WebsiteSalePortal, self).shop(page, category, search, ppg, **post)

    @http.route(['/shop/product/<model("product.template"):product>'], type='http', auth="public", website=True)
    def product(self, product, category='', search='', **kwargs):
        if not request.session.login:
            return request.redirect('/web/login?redirect=%s' % request.httprequest.path)
        return super(WebsiteSalePortal, self).product(product, category, search, **kwargs)
