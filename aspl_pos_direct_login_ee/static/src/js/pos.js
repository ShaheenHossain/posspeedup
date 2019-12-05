odoo.define('aspl_pos_direct_login_ee.pos', function (require) {
    "use strict";

    var chrome = require('point_of_sale.chrome');
    var framework = require('web.framework');
    var models = require('point_of_sale.models');
    var gui = require('point_of_sale.gui');
    var PopupWidget = require('point_of_sale.popups');

    models.load_fields("res.users", ['login_with_pos_screen']);

    chrome.HeaderButtonWidget.include({
        renderElement: function(){
            var self = this;
            this._super();
            if(this.action){
                this.$el.click(function(){
                    self.gui.show_popup('confirm_close_pos_wizard');
                });
            }
        },
    });

    var ConfirmClosePosPopupWizard = PopupWidget.extend({
        template: 'ConfirmClosePosPopupWizard',
        show: function(){
            this._super();
            var self = this;
        },
        click_confirm: function(){
            var self = this;
            var cashier = self.pos.user || false;
            if(cashier && cashier.login_with_pos_screen){
                framework.redirect('/web/session/logout');
            } else{
                self.pos.gui.close();
            }
        },
    });
    gui.define_popup({name:'confirm_close_pos_wizard', widget: ConfirmClosePosPopupWizard});

});