odoo.define('pos_partial_pay.pos_partial_pay', function (require) {
"use strict";

var module = require('point_of_sale.models');
var chrome = require('point_of_sale.chrome');
var core = require('web.core');
var PosPopWidget = require('point_of_sale.popups');
var PosBaseWidget = require('point_of_sale.BaseWidget');
var gui = require('point_of_sale.gui');
var rpc = require('web.rpc');
var screens = require('point_of_sale.screens');
var _t = core._t;

    screens.PaymentScreenWidget.include({
	    renderElement: function() {
            var self = this;
            this._super();
            this.$('.partially_pay').click(function(){
                debugger;
                var order = self.pos.get_order();

            	// var total_amount = order.get_total_with_tax();
            	// var total_percentage = (total_amount * self.pos.config.min_amount)/100;
            	// var paid_order = order.get_total_paid();
            	// if(paid_order >= total_percentage){
            	// 	self.pos.push_order(order);
	            // 	// self.gui.show_screen('receipt');
            	// }
            	// else{
            	// 	alert("You want to pay at least "+self.pos.config.min_amount+"% amount");
                // }
                
                var invoiced = self.pos.push_and_invoice_order(order);
                this.invoicing = true;
                invoiced.fail(function(error) {
                    self.invoicing = false;
                    order.finalized = false;
                    if (error.message === 'Missing Customer') {
                        self.gui.show_popup('confirm', {
                            'title': _t('Please select the Customer'),
                            'body': _t('You need to select the customer before you can invoice an order.'),
                            confirm: function() {
                                self.gui.show_screen('clientlist');
                            },
                        });
                    } else if (error.code < 0) {
                        self.gui.show_popup('error', {
                            'title': _t('The order could not be sent'),
                            'body': _t('Check your internet connection and try again.'),
                        });
                    } else if (error.code === 200) {
                        self.gui.show_popup('error-traceback', {
                            'title': error.data.message || _t("Server Error"),
                            'body': error.data.debug || _t('The server encountered an error while receiving your order.'),
                        });
                    } else {
                        self.gui.show_popup('error', {
                            'title': _t("Unknown Error"),
                            'body': _t("The order could not be sent to the server due to an unknown error"),
                        });
                    }
                });
                invoiced.done(function() {
                    self.invoicing = false;
                    self.gui.show_screen('receipt');
                });

            	
            	
            });
        },

    });
    
    screens.define_action_button({
        'name': 'partiallypaymentbutton',
        'widget': PartiallyPaymentButton,
        'condition': function(){
            return this.pos.config.allow_partial_pay;
        },
    });

    var _super_order = module.Order.prototype;
    module.Order = module.Order.extend({
        export_as_JSON: function() {
            var json = _super_order.export_as_JSON.apply(this,arguments);
            json.reference_number = this.uid.replace(/-/g, '');
            return json;
        },
        init_from_JSON: function(json) {
            _super_order.init_from_JSON.apply(this,arguments);
            this.reference_number = json.uid.replace(/-/g, '');
        },
    });

    // invoice auto enabled
    screens.PaymentScreenWidget.include({
        renderElement: function() {
            var self = this;
            this._super();

            debugger;
            var order = this.pos.get_order();
            order.set_to_invoice(true);
            
            this.$('.js_invoice').addClass('highlight');
            this.$('.js_invoice').css("pointer-events", "none");

        },
    })
});

