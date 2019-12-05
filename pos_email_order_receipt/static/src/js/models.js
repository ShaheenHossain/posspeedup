/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : <https://store.webkul.com/license.html/> */

odoo.define('pos_email_order_receipt.models', function (require) {
    "use strict";
    var models = require("point_of_sale.models");
    var SuperOrder = models.Order.prototype;

    models.Order = models.Order.extend({
        reset_email_backup_data: function(){
            this.email_data_backup.email_receipt = false;
            this.email_data_backup.update_record = false;
            this.email_data_backup.receipt_email = false;
            this.email_data_backup.client_id = null;
        },
        initialize: function(attributes,options){
            SuperOrder.initialize.call(this, attributes, options);
            this.email_data_backup = {
                email_receipt : false,
                update_record : false,
                receipt_email : false,
                client_id: false,
            }
        },
        export_as_JSON: function() {
            var self = this;
            var order_json=SuperOrder.export_as_JSON.call(this);
            if(self.email_data_backup){
                order_json.email_receipt=self.email_data_backup.email_receipt;
                order_json.update_record=self.email_data_backup.update_record;
                order_json.receipt_email=self.email_data_backup.receipt_email;
                order_json.email_client_id=self.email_data_backup.client_id;
            }
            return order_json;
        },
    });
});