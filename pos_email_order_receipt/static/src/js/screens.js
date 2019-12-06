/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : <https://store.webkul.com/license.html/> */

odoo.define('pos_email_order_receipt.screens', function (require) {
    "use strict";
    var screens = require("point_of_sale.screens")

    screens.PaymentScreenWidget.include({
        show: function(){
            this._super();
            var self = this;
            var order = this.pos.get_order();
            var client = order.get_client();
            if(this.$('.e-receipt-section').hasClass("e-receipt-active")){
                order.email_data_backup.email_receipt = true;
                order.email_data_backup.client_id = client && client.id || false;
                order.email_data_backup.receipt_email = client && client.email || '';
                order.email_data_backup.update_record = false
            }
        },
        renderElement: function() {
            var self = this;
            this._super();
            this.$('.e-receipt-section').on("click", function(event){
                var order = self.pos.get_order();
                var client = order.get_client();
                $(this).toggleClass("e-receipt-active");
                if($(this).hasClass("e-receipt-active")){
                    order.email_data_backup.email_receipt = true;
                    order.email_data_backup.client_id = client && client.id || false;
                    order.email_data_backup.receipt_email = client && client.email || '';
                    order.email_data_backup.update_record = false
                    if(!client || (client && !client.email)){
                        self.pos.gui.show_popup("email_edit_popup", {
                            client: order.get_client(),
                            email_data_backup: order.email_data_backup,
                        });
                    }
                }else{
                    order.reset_email_backup_data();
                }
            });
            this.$('.edit-email').on("click", function(event){
                event.stopPropagation();
                var order = self.pos.get_order();
                var client = order.get_client();
                self.pos.gui.show_popup("email_edit_popup", {
                    client: client,
                    email_data_backup: order.email_data_backup,
                });
            });
        },
    });
});