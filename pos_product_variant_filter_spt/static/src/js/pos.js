odoo.define('product_variant_filter_spt.pos', function (require) {
"use strict";
    var PosBaseWidget = require('point_of_sale.BaseWidget');
    var models = require('point_of_sale.models');
    var screens = require('point_of_sale.screens');
    var gui = require('point_of_sale.gui');
    var PosPopWidget = require('point_of_sale.popups');
    var core = require('web.core');
    var DB = require('point_of_sale.DB');
    // var Model = require('web.DataModel');
    var QWeb = core.qweb;
    var _t = core._t;


    models.load_fields("product.product",['attribute_value_ids','brand','model']);

    models.load_models([{
		model:  'product.attribute',
        fields: ['name', 'value_ids','type'],
        loaded: function(self, product_attributes){
            var attribute_by_id = {};
            _.each(product_attributes, function (attribute) {
                attribute_by_id[attribute.id] = attribute;
            });

            //debugger;
            self.product_attributes = product_attributes;
            self.db.add_product_attributes(product_attributes);

            var pos_products_bm = self.db.product_by_id;

            var product_brands = Object.values(pos_products_bm).filter(function (product) {
                return product.brand != false;
            }).map(function (product_b){
                return product_b.brand;
            });

            let product_uniq_brand = [...new Set(product_brands)];
            self.product_brands = product_uniq_brand;

            var product_models = Object.values(pos_products_bm).filter(function (product) {
                return product.model != false;
            }).map(function (product_m){
                return product_m.model;
            });

            let product_uniq_models = [...new Set(product_models)];
            self.product_models = product_uniq_models;

        }
    },
    {
        model:  'product.attribute.value',
        fields: [  'name',
                'attribute_id',
                'html_color'
                ],
        loaded: function(self,values){
            self.product_attribute_values = values;
            self.db.add_product_attribute_values(values);
        },
    }]);
    
    screens.ProductCategoriesWidget.include({
        renderElement: function () {
            //debugger;
			var self = this;
            this._super();
            self.pos.filter_ids = [];
            
            this.el.querySelector('.filter_spt').addEventListener('click', function () {
                //debugger;
                
                $('.offCanvas').toggleClass('left0');
                $('.overlay_filter').toggleClass('visible');

            });

            this.el.querySelector('.clear_filter').addEventListener('click', function () {
                //debugger;
                $('.filter_chk:checkbox').removeAttr('checked');
                // var filter_ids = [];
                // $('.submenu').css("display","none");
                var pos_products = self.pos.db.get_product_by_category(self.category.id);
                self.product_list_widget.set_product_list(Object.values(pos_products));
                self.pos.filter_ids = [];
                self.pos.product_filtered = pos_products;
                $('.filter_clear_spt').hide("fast");
            });
            
		},
    });
    
    screens.ProductScreenWidget.include({
        start: function () {
			var self = this;
            self._super();
            //debugger;
        },
        show: function () {
            //debugger;
			this._super();
            var self = this;
            
            // var filter_ids = [];
            
            var Accordion = function(el, multiple) {
                //debugger;
                this.el = el || {};
                this.multiple = multiple || false;
        
                // Variables privadas
                var links = this.el.find('.link');
                // Evento
                links.on('click', {el: this.el, multiple: this.multiple}, this.dropdown);
                //debugger;
                var selection = this.el.find('.filter_chk');
                selection.on('change', {el: this.el, multiple: this.multiple}, this.filter);
            }

            
            this.el.querySelector('.overlay_filter').addEventListener('click', function () {
                //debugger;
                $('.offCanvas').removeClass('left0');
                $('.overlay_filter').removeClass('visible');
                
                // Reset offcanvas scroll to the top after half a second to avoid scroll to jump up when closing
                setTimeout(function(){
                $('.offCanvas').scrollTop(0) 
                }, 500)

            });


            
        
            Accordion.prototype.dropdown = function(e) {
               
                var $el = e.data.el;
                var $this = $(this);
                var $next = $this.next();
        
                $next.slideToggle();
                $this.parent().toggleClass('open');
        
                if (!e.data.multiple) {
                    $el.find('.submenu').not($next).slideUp().parent().removeClass('open');
                };
            }	

            Accordion.prototype.filter = function(e) 
            {
                //debugger;
                var $this = $(this);

                var current_id = parseInt($this.attr('id'))?parseInt($this.attr('id')):$this.val();
                
                if($this.is(":checked")){
                    self.pos.filter_ids.push(current_id);
                }
                else{
                    for( var i = 0; i < self.pos.filter_ids.length; i++){ 
                        if ( self.pos.filter_ids[i] === current_id) {
                            self.pos.filter_ids.splice(i, 1); 
                        }
                     }
                }

                var pos_products = self.pos.db.get_product_by_category(self.product_categories_widget.category.id)
                // self.pos.db.product_by_id;
                // self.pos.db.get_product_by_category(self.product_categories_widget.category.id)

                if (self.pos.filter_ids.length > 0){
                     // var filterd_products = products.filter()
                    var filterd_products = Object.values(pos_products).filter(function (product) {
                        return (product.attribute_value_ids.some(p=> self.pos.filter_ids.indexOf(p) >= 0) || 
                            self.pos.filter_ids.indexOf(product.brand) > -1 || 
                            self.pos.filter_ids.indexOf(product.model) > -1);
                    });

                    self.product_list_widget.set_product_list(filterd_products);
                    self.pos.product_filtered = filterd_products;
                    $('.filter_clear_spt').show("fast");
                    //debugger;
                }
                else{
                    self.product_list_widget.set_product_list(Object.values(pos_products));
                    self.pos.product_filtered = pos_products;
                    $('.filter_clear_spt').hide("fast");
                }
            }
        
            var accordion = new Accordion($('#accordion'), false);
        }
    });

    
    
    DB.include({
        init: function(options){
			this._super.apply(this, arguments);

			this.template_by_id = {};
            this.product_attribute_by_id = {};
            this.product_attribute_value_by_id = {};
        },
        add_product_attributes: function(product_attributes){
            for(var i=0 ; i < product_attributes.length; i++){
                // store Product Attributes
                this.product_attribute_by_id[product_attributes[i].id] = product_attributes[i];
            }
        },

        add_product_attribute_values: function(product_attribute_values){
            for(var i=0 ; i < product_attribute_values.length; i++){
                // store Product Attribute Values
                this.product_attribute_value_by_id[product_attribute_values[i].id] = product_attribute_values[i];
            }
        },
        get_product_attribute_by_id: function(attribute_id){
            return this.product_attribute_by_id[attribute_id];
        },

        get_product_attribute_value_by_id: function(attribute_value_id){
            return this.product_attribute_value_by_id[attribute_value_id];
        },
        
        attribute_by_template_id: function(template_id){
            var template = this.template_by_id[template_id];
            return this.attribute_by_attribute_value_ids(template.attribute_value_ids);
        },
        attribute_by_attribute_value_ids: function(value_ids){
            var attribute_ids = [];
            for (var i = 0; i < value_ids.length; i++){
                var value = this.product_attribute_value_by_id[value_ids[i]];
                if (attribute_ids.indexOf(value.attribute_id[0])==-1){
                    attribute_ids.push(value.attribute_id[0]);
                }
            }
            return attribute_ids;
        },
    });

    // return {
    //     ProductVariantWidget: ProductVariantWidget,
    // };

});
