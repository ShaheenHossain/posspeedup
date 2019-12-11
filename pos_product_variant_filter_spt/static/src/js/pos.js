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


    models.load_fields("product.product",['attribute_value_ids']);
    models.load_models([{
		model:  'product.attribute',
        fields: ['name', 'value_ids','type'],
        loaded: function(self, product_attributes){
            var attribute_by_id = {};
            _.each(product_attributes, function (attribute) {
                attribute_by_id[attribute.id] = attribute;
            });

            self.product_attributes = product_attributes;
            self.db.add_product_attributes(product_attributes);
        }

    },
    {
        model:  'product.attribute.value',
        fields: [  'name',
                'attribute_id',
                ],
        loaded: function(self,values){
            self.product_attribute_values = values;
            self.db.add_product_attribute_values(values);
        },
    }]);
    
    screens.ProductCategoriesWidget.include({
        renderElement: function () {
            debugger;
			var self = this;
			this._super();
            
            this.el.querySelector('.filter_spt').addEventListener('click', function () {
                debugger;
                
                $('.offCanvas').toggleClass('left0');
                $('.overlay_filter').toggleClass('visible');

            });
		},
    });
    
    screens.ProductScreenWidget.include({
        show: function () {
			this._super();
            var self = this;
            
            this.el.querySelector('.overlay_filter').addEventListener('click', function () {
                debugger;
                $('.offCanvas').removeClass('left0');
                $('.overlay_filter').removeClass('visible');
                
                // Reset offcanvas scroll to the top after half a second to avoid scroll to jump up when closing
                setTimeout(function(){
                $('.offCanvas').scrollTop(0) 
                }, 500)

            });


            // this.product_variant_widget = new ProductVariantWidget(this,{
            //     product_list_widget: this.product_list_widget,
            // });
            // this.product_variant_widget.replace(this.$('.placeholder-ProductVariantWidget'));

            // debugger;
            // var product_tmpl_id = self.gui.get_current_screen_param('product_tmpl_id');
			// var template = this.pos.db.template_by_id[product_tmpl_id];
			// this.$('#variant-title-name').html(template.name);

			// // Render Variants
			// var variant_ids = this.pos.db.template_by_id[product_tmpl_id].product_variant_ids;
			// var variant_list = [];
			// for (var i = 0, len = variant_ids.length; i < len; i++) {
			// 	variant_list.push(this.pos.db.get_product_by_id(variant_ids[i]));
			// }
			// var attribute_ids = this.pos.db.attribute_by_template_id(template.id);
			// var attribute_list = [];
			// for (var i = 0, len = attribute_ids.length; i < len; i++) {
			// 	attribute_list.push(this.pos.db.get_product_attribute_by_id(attribute_ids[i]));
			// }

            var Accordion = function(el, multiple) {
                debugger;
                this.el = el || {};
                this.multiple = multiple || false;
        
                // Variables privadas
                var links = this.el.find('.link');
                // Evento
                links.on('click', {el: this.el, multiple: this.multiple}, this.dropdown)
            }
        
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
        
            var accordion = new Accordion($('#accordion'), false);
        }
    });

    // var ProductVariantWidget = PosBaseWidget.extend({
    //     template: 'ProductVariantWidget',
    //     init: function(parent, options){
    //         debugger;
    //         var self = this;
    //         this._super(parent,options);
    //         this.product_type = options.product_type || 'all';  // 'all' | 'weightable'
    //         this.onlyWeightable = options.onlyWeightable || false;
    //         this.category = this.pos.root_category;
    //         this.breadcrumb = [];
    //         this.product_list_widget = options.product_list_widget || null;
    //         this.start_categ_id = this.pos.config.iface_start_categ_id ? this.pos.config.iface_start_categ_id[0] : 0;
    //         this.set_category(this.pos.db.get_category_by_id(this.start_categ_id));
            
    //         this.switch_category_handler = function(event){
    //             self.set_category(self.pos.db.get_category_by_id(Number(this.dataset.categoryId)));
    //             self.renderElement();
    //         };
            
    //         this.clear_search_handler = function(event){
    //             self.clear_search();
    //         };
    
    //         var search_timeout  = null;
    //         this.search_handler = function(event){
    //             if(event.type == "keypress" || event.keyCode === 46 || event.keyCode === 8){
    //                 clearTimeout(search_timeout);
    
    //                 var searchbox = this;
    
    //                 search_timeout = setTimeout(function(){
    //                     self.perform_search(self.category, searchbox.value, event.which === 13);
    //                 },70);
    //             }
    //         };
    //     },
    
    //     // changes the category. if undefined, sets to root category
    //     set_category : function(category){
    //         var db = this.pos.db;
    //         if(!category){
    //             this.category = db.get_category_by_id(db.root_category_id);
    //         }else{
    //             this.category = category;
    //         }
    //         this.breadcrumb = [];
    //         var ancestors_ids = db.get_category_ancestors_ids(this.category.id);
    //         for(var i = 1; i < ancestors_ids.length; i++){
    //             this.breadcrumb.push(db.get_category_by_id(ancestors_ids[i]));
    //         }
    //         if(this.category.id !== db.root_category_id){
    //             this.breadcrumb.push(this.category);
    //         }
    //         debugger;
    //     },
    
    //     render_category: function( category, with_image ){
    //         var category_html = QWeb.render('CategorySimpleButton',{ 
    //                 widget:  this, 
    //                 category: category, 
    //             });
    //             category_html = _.str.trim(category_html);
    //         var category_node = document.createElement('div');
    //             category_node.innerHTML = category_html;
    //             category_node = category_node.childNodes[0];
    //         return category_node;
    //     },
    
    //     renderElement: function(){
    
    //         var el_str  = QWeb.render(this.template, {widget: this});
    //         var el_node = document.createElement('div');
    
    //         el_node.innerHTML = el_str;
    //         el_node = el_node.childNodes[1];
    
    //         if(this.el && this.el.parentNode){
    //             this.el.parentNode.replaceChild(el_node,this.el);
    //         }
    
    //         this.el = el_node;
    
    //         var withpics = this.pos.config.iface_display_categ_images;
    
    //         var list_container = el_node.querySelector('.category-list');
    //         if (list_container) { 
    //             debugger;
    //             if (!withpics) {
    //                 list_container.classList.add('simple');
    //             } else {
    //                 list_container.classList.remove('simple');
    //             }
    //         }
    
    //         var buttons = el_node.querySelectorAll('.js-category-switch');
    //         for(var i = 0; i < buttons.length; i++){
    //             buttons[i].addEventListener('click',this.switch_category_handler);
    //         }
    
    //         var products = this.pos.db.get_product_by_category(this.category.id); 
    //         this.product_list_widget.set_product_list(products); // FIXME: this should be moved elsewhere ... 
    
    //         this.el.querySelector('.searchbox input').addEventListener('keypress',this.search_handler);
    
    //         this.el.querySelector('.searchbox input').addEventListener('keydown',this.search_handler);
    
    //         this.el.querySelector('.search-clear').addEventListener('click',this.clear_search_handler);
    
    //         if(this.pos.config.iface_vkeyboard && this.chrome.widget.keyboard){
    //             this.chrome.widget.keyboard.connect($(this.el.querySelector('.searchbox input')));
    //         }
    //     },
    
    // });

    // screens.ProductScreenWidget.include({
    //     show: function(){
    //         var self = this;
    //         this._super();
    //         $(".product_review").click(function(event){
    //             var product_id = $(this).attr("data-product-id");
    //             var product = self.pos.db.get_product_by_id(product_id);
    //             debugger;
    //             self.gui.show_popup('multi-img-popup',{'product':product});
    //             event.preventDefault();
    //             event.stopPropagation();
    //         });
    //     },

    // }); 
    
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
