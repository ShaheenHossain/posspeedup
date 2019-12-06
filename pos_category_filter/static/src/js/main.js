/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : <https://store.webkul.com/license.html/> */
odoo.define('pos_category_filter.pos_category_filter', function (require) {
	"use strict";
	var pos_models = require('point_of_sale.models');
	var models = pos_models.PosModel.prototype.models;
	var category_model = null;

	for(var i = 0; i < models.length; i++) {
		if(models[i].model === 'pos.category') {
			category_model = models[i];
			break;
		}
	}

	category_model.domain = function(self) {
		var categories_ids = self.config.wk_product_category_ids;
		if (categories_ids.length == 0)
			return null;
		return ['|',['id','in',categories_ids],['parent_id','in',categories_ids]];
	};

	category_model.loaded = function(self, categories){
		var category_ids=self.config.wk_product_category_ids;
		if(category_ids.length != 0){
			for(var i=0;i<categories.length;i++){
				if(categories[i].parent_id != false && (category_ids.indexOf(categories[i].parent_id[0]) == -1)){
					categories[i].parent_id = false;
				}   
			}
		}
		self.db.add_categories(categories);
	};
});