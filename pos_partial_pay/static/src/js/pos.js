odoo.define('pos_partial_pay.pos', function (require) {
"use strict";

var core = require('web.core');
var screens = require('point_of_sale.screens');
var _t = core._t;

screens.PaymentScreenWidget.include({
    renderElement: function() {
        //debugger;
        var self = this;
        this._super();

        this.$('.js_invoice').addClass('highlight');
        this.$('.js_invoice').css("pointer-events", "none");
        this.$('.js_invoice').css("display", "none");

        this.$('.partially_pay').click(function(){
            //debugger;
            var order = self.pos.get_order();
            order.set_to_invoice(true);

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
    show: function() {
        //debugger;
        this._super();

        this.$('.js_invoice').css("display", "none");

        this.pos.get_order().set_to_invoice(true);

    },

});
    
screens.define_action_button({
    'name': 'partiallypaymentbutton',
    'widget': PartiallyPaymentButton,
    'condition': function(){
        return this.pos.config.allow_partial_pay;
    },
});


});

