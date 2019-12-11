odoo.define('pos_multi_image.pos_multi_image', function (require) {
"use strict";
    var models = require('point_of_sale.models');
    var screens = require('point_of_sale.screens');
    var gui = require('point_of_sale.gui');
    var PosPopWidget = require('point_of_sale.popups');
    var core = require('web.core');
    // var Model = require('web.DataModel');
    var QWeb = core.qweb;
    var _t = core._t;


    models.load_fields("product.product",['product_multi_img_id','image','image_secondary','attribute_value_ids']);
    
    screens.ProductScreenWidget.include({
        show: function(){
            var self = this;
            this._super();
            $(".product_review").click(function(event){
                var product_id = $(this).attr("data-product-id");
                var product = self.pos.db.get_product_by_id(product_id);
                debugger;
                self.gui.show_popup('multi-img-popup',{'product':product});
                event.preventDefault();
                event.stopPropagation();
            });
        },

    });    

    var MultiImgPopupWidget = PosPopWidget.extend({
    template: 'MultiImgPopupWidget',
        
        renderElement: function(options){
            this._super(); 
            var self = this;
            $('.bxslider').bxSlider({
                auto: false,
                autoControls: true,
                stopAutoOnClick: true,
                pager: true,
                slideWidth: 900,
                adaptiveHeight: true,
            });
            $(".add_to_cart_button").click(function(){
                var order = self.pos.get_order();
                order.add_product(options.product);
                self.gui.show_screen('products');
            });
        },
        show: function(options){
            this.options = options || {};
            var self = this;
            this._super(options); 
            this.renderElement(options);
        },
    });

    gui.define_popup({
        'name': 'multi-img-popup', 
        'widget': MultiImgPopupWidget,
    });

    

});
