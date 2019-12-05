/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : <https://store.webkul.com/license.html/> */

odoo.define('pos_email_order_receipt.popups', function (require) {
    "use strict";
    var gui = require('point_of_sale.gui');
    var popup_widget = require('point_of_sale.popups');

    var EmailEditPopup = popup_widget.extend({
        template: 'EmailEditPopup',
        events: {
            'click .email-update-cancel': 'click_cancel',
            'click .wk-update-email': 'update_email',
        },
        update_email: function(){
            var order = this.pos.get_order();
            order.email_data_backup.update_record = order.get_client() && this.$(".update-record-check").is(":checked") || false;
            order.email_data_backup.receipt_email = this.$(".email-edit-input").val();
            order.email_data_backup.client_id = this.options.client && this.options.client.id || false;
            this.click_cancel();
        },
        show: function(options){
            this._super(options);
            var self = this;
            var payment_screen = self.pos.chrome.screens.payment;
            $('body').off('keypress', payment_screen.keyboard_handler);
            $('body').off('keydown', payment_screen.keyboard_keydown_handler);
            window.document.body.removeEventListener('keypress',payment_screen.keyboard_handler);
            window.document.body.removeEventListener('keydown',payment_screen.keyboard_keydown_handler);
        },
        close: function(){
            this._super();
            var self = this;
            var payment_screen = self.pos.chrome.screens.payment;
            $('body').keypress(payment_screen.keyboard_handler);
            $('body').keydown(payment_screen.keyboard_keydown_handler);
            window.document.body.addEventListener('keypress',payment_screen.keyboard_handler);
            window.document.body.addEventListener('keydown',payment_screen.keyboard_keydown_handler);
        },
    });
    gui.define_popup({name:'email_edit_popup', widget: EmailEditPopup});
});