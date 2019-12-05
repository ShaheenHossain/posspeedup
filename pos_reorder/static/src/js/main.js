/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : <https://store.webkul.com/license.html/> */
odoo.define('pos_reorder.pos_reorder', function (require) {
"use strict"
	var pos_orders = require("pos_orders.pos_orders");
	var core = require('web.core');
	var popup_widget = require('point_of_sale.popups');
	var _t = core._t;
	var gui = require('point_of_sale.gui');

	pos_orders.include({
		show: function(){
			var self = this;
			this._super();
			this.$('.wk-order-list-contents').delegate('.wk_reorder_content', 'click', function(event){
				var order_line_data = self.pos.db.pos_all_order_lines;
				var order_id = this.id;
				var order = self.pos.get_order();
				var product_list = [];
				var all_product_available = true;
				for(var i=0; i<order_line_data.length;i++) {
					if(order_line_data[i].order_id[0] == this.id)
					{	
						var product = self.pos.db.get_product_by_id(order_line_data[i].product_id[0]);
						if (product)
							product_list.unshift({'product':product,'qty':order_line_data[i].qty});
						else
							all_product_available= false;
					}
				}
				if(all_product_available){
					product_list.forEach(function(product){
						order.add_product(product.product,{quantity:product.qty});
					});
					self.gui.show_screen('products');
				}
				else{
					var message;
					if(product_list.length)
						message = "Some products are not available in POS. Are you sure to reorder remaining available products ? Clicking 'Confirm' will reorder remaining available products.";
					self.pos.gui.show_popup('product_not_available',{
						'title':_t("Product(s) Not Available !!!"),
						'body':_t(message),
						'product_list':product_list
					});
				}
			});
		},
	});

	var ProductNotAvailablePopup = popup_widget.extend({
		template:'ProductNotAvailablePopup',
		
		events:{
			'click .cancel': 'click_cancel',
			'click .confirm': 'wk_click_confirm',
		},
		click_cancel: function(){
			this.pos.gui.close_popup();
		},
		wk_click_confirm:function(options) {
			var self = this;
			var order = self.pos.get_order();
			var reorder_products = self.options.product_list;
			reorder_products.forEach(function(product){
				order.add_product(product.product,product.qty);
			})
			self.pos.gui.close_popup();
			self.pos.gui.show_screen('products');
		},
		show:function(options) {
			var self = this;
			self.options = options;
			self._super(options);
		}
	});
	gui.define_popup({ name: 'product_not_available', widget: ProductNotAvailablePopup });
	
});