odoo.define('pos_product_order.pos_product_order', function (require) {
"use strict";

var core = require('web.core');
var models = require('point_of_sale.models');
var screens = require('point_of_sale.screens');

var QWeb = core.qweb;


screens.ProductCategoriesWidget.include({
    init: function(parent, options) {
        var self = this;
        this._super(parent, options);
        this.order_products_handler = function(event) {
            var products = self.pos.db.get_product_by_category(self.category.id); 
            self.product_list_widget.set_product_list(self.order_products(products));
        };
    },

    renderElement: function() {
        this._super();
        var products = this.pos.db.get_product_by_category(this.category.id); 
        this.product_list_widget.set_product_list(this.order_products(products));
        this.el.querySelector('.pos-product-order').addEventListener('change', this.order_products_handler);
    },

    clear_search: function(){
        this._super();
        var products = this.pos.db.get_product_by_category(this.category.id);
        this.product_list_widget.set_product_list(this.order_products(products));
    },

    perform_search: function(category, query, buy_result){
        var products;
        if (query) {
            products = this.pos.db.search_product_in_category(category.id,query);
            products = this.order_products(products);
            if (buy_result && products.length === 1) {
                this.pos.get_order().add_product(products[0]);
                this.clear_search();
            } else {
                this.product_list_widget.set_product_list(products);
            }
        } else {
            products = this.pos.db.get_product_by_category(this.category.id);
            this.product_list_widget.set_product_list(this.order_products(products));
        }
    },

    order_products: function(products) {
        if (document.getElementById('pos-product-order-name-asc')
                && document.getElementById('pos-product-order-name-asc').selected) {
            products.sort(function(x, y) {
                if (x.display_name.toLowerCase() < y.display_name.toLowerCase()) return -1;
                if (x.display_name.toLowerCase() > y.display_name.toLowerCase()) return 1;
                return 0;
            });
        } else if (document.getElementById('pos-product-order-name-desc')
                   && document.getElementById('pos-product-order-name-desc').selected) {
            products.sort(function(x, y) {
                if (x.display_name.toLowerCase() > y.display_name.toLowerCase()) return -1;
                if (x.display_name.toLowerCase() < y.display_name.toLowerCase()) return 1;
                return 0;
            });
        } else if (document.getElementById('pos-product-order-price-asc')
                   && document.getElementById('pos-product-order-price-asc').selected) {
            products.sort(function(x, y) {
                if(parseFloat(x.list_price) < parseFloat(y.list_price)) return -1;
                if(parseFloat(x.list_price) > parseFloat(y.list_price)) return 1;
                return 0;
            });
        } else if (document.getElementById('pos-product-order-price-desc')
                   && document.getElementById('pos-product-order-price-desc').selected) {
            products.sort(function(x, y) {
                if(parseFloat(x.list_price) > parseFloat(y.list_price)) return -1;
                if(parseFloat(x.list_price) < parseFloat(y.list_price)) return 1;
                return 0;
            });
        }
        return products;
    },
});

});
