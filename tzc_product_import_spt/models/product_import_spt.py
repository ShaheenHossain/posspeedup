# -*- coding: utf-8 -*-
# Part of SnepTech. See LICENSE file for full copyright and licensing details.##
###############################################################################

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import base64
from odoo.exceptions import UserError
from odoo.modules import get_module_resource
try:
    import paramiko
except ImportError:
    raise ImportError(
        'This module needs paramiko to automatically write backups to the FTP through SFTP. Please install paramiko on your system. (sudo pip3 install paramiko)')

class product_import_spt(models.Model):
    _name = 'product.import.spt'
    _rec_name = 'attach_file_name'

    date = fields.Date('Date')
    attach_file = fields.Binary("Attach File")
    attach_file_name = fields.Char("Attach File Name")

    import_line_ids = fields.One2many('product.import.line.spt', 'import_id', 'Product Lines')

    number_of_product = fields.Integer('Number Of Product', compute='_get_number_of_product')
    product_ids = fields.Many2many('product.template', 'product_import_product_tmpl_rel_spt', 'product_import_id', 'product_tmpl_id', string='Products', copy=False)
    # server_id = fields.Many2one('ftp.server.spt', 'Server')
    image_path = fields.Char('Image Path')
    state = fields.Selection([
        ('draft','Draft'),
        ('process','In Process'),
        ('done','Done'),
    ], string='State', default='draft')

    categ_id = fields.Many2one('product.category', 'Default Category')

    @api.multi
    def action_view_products(self):
        self.ensure_one()
        
        try:
            list_view = self.env.ref('product.product_template_tree_view')
            form_view = self.env.ref('product.product_template_only_form_view')
            
        except ValueError:
            list_view = False
            form_view = False

        return {
            'name': 'Products',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'product.template',
            'view_id': False,
            'views': [(list_view.id, 'tree'),(form_view.id, 'form')],
            'type': 'ir.actions.act_window',
            'target':'current',
            'domain':[('id','in',self.product_ids.ids)],
        }   

    @api.multi
    def _get_number_of_product(self):
        for record in self:
            record.number_of_product = len(record.product_ids)

    @api.multi
    def action_set_to_done(self):
        for record in self:
            record.state = 'done'

    @api.multi
    def action_create_product(self):
        import_line_obj = self.env['product.import.line.spt']
        attribute_obj = self.env['product.attribute']
        attribute_value_obj = self.env['product.attribute.value']
        attribute_line_obj = self.env['product.attribute.line']
        product_temp_obj = self.env['product.template']
        product_pro_obj = self.env['product.product']
        categ_obj = self.env['product.category']
        for record in self:
            # import_line_rec = import_line_obj.search([('import_id','=',record.id),'|',('color','in',[False,'',' ']),('size','in',[False,'',' '])])
            # if import_line_rec.ids:
            #     raise UserError(_('color or size column can not be empty, please check following products!\n' + str([x.internal_reference for x in import_line_rec])))
            done_ids = []
            attribute_color = attribute_obj.search([('name','=','Color')],limit=1)
            if not attribute_color.id:
                attribute_color = attribute_obj.create({
                    'name':'Color',
                    'type':'color',
                    'create_variant':True,
                })
            attribute_size = attribute_obj.search([('name','=','Size')],limit=1)
            if not attribute_size.id:
                attribute_size = attribute_obj.create({
                    'name':'Size',
                    'type':'select',
                    'create_variant':True,
                })

            get_group = "select model,brand from product_import_line_spt where import_id=" + str(record.id) +  " group by brand,model"
            self.env.cr.execute(get_group)
            inv_line_list = [(x[0],x[1]) for x in self.env.cr.fetchall()]
            # s = paramiko.SSHClient()
            # s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # s.connect(record.server_id.server_ip, record.server_id.server_port, record.server_id.server_user, record.server_id.server_password, timeout=10,allow_agent=False,look_for_keys=False)
            # sftp = s.open_sftp()
            product_ids = []
            for line in inv_line_list:
                variants = import_line_obj.search([('import_id','=',record.id),('brand','=',line[1]),('model','=',line[0])])
                color_value_ids = []
                size_value_ids = []
                for variant in variants:
                    product_product = product_pro_obj.search([('barcode','=',variant.barcode)])
                    if not product_product.id:
                        # if variant.color:
                        color_value = attribute_value_obj.search([('attribute_id','=',attribute_color.id),('name','=',variant.color or 'None')])
                        if not color_value.id:
                            color_value = attribute_value_obj.create({
                                'attribute_id':attribute_color.id,
                                'name':variant.color  or 'None',
                            })
                        color_value_ids.append(color_value.id)
                        
                        # if variant.size:
                        size_value = attribute_value_obj.search([('attribute_id','=',attribute_size.id),('name','=',variant.size or 'None')])
                        if not size_value.id:
                            size_value = attribute_value_obj.create({
                                'attribute_id':attribute_size.id,
                                'name':variant.size or 'None',
                            })
                        size_value_ids.append(size_value.id)

                product_type = 'product'
                product = product_temp_obj.search([('brand','=',variant.brand),('model','=',variant.model)])
                if not product.id:
                    product = product_temp_obj.create({
                        'name':variant.brand + ' ' + variant.model,
                        # 'default_code':variant.internal_reference,
                        'active':variant.is_active,
                        'sale_ok':variant.sale_ok,
                        'purchase_ok':variant.purchase_ok,
                        'price_wholesale':variant.list_price,
                        'list_price': variant.standard_price, 
                        'price_msrp':variant.price_msrp,
                        'type':product_type,
                        # 'barcode':variant.barcode,
                        'brand':variant.brand,
                        'model':variant.model,
                        'categ_id':categ_obj.search([('name','=',variant.categ_id)],limit=1).id or categ_obj.create({'name':variant.categ_id}).id,
                        'attribute_line_ids':[(0,0,{'attribute_id':attribute_color.id,'value_ids':[(6,0,color_value_ids)]}),(0,0,{'attribute_id':attribute_size.id,'value_ids':[(6,0,size_value_ids)]})]
                    })
                else:
                    size = color = 0
                    for attr_line in product.attribute_line_ids:
                        if attr_line.attribute_id.id == attribute_color.id:
                            attr_line.value_ids = [(6,0,attr_line.value_ids.ids + color_value_ids)]
                            color = 1
                            
                        if attr_line.attribute_id.id == attribute_size.id:
                            attr_line.value_ids = [(6,0,attr_line.value_ids.ids + size_value_ids)]
                            size = 1

                    if color == 0:
                        attribute_line_obj.create({
                            'attribute_id':attribute_color.id,
                            'value_ids':[(6,0,color_value_ids)],
                            'product_tmpl_id':product.id,
                        })

                    if size == 0:
                        attribute_line_obj.create({
                            'attribute_id':attribute_size.id,
                            'value_ids':[(6,0,size_value_ids)],
                            'product_tmpl_id':product.id,
                        })
                product.create_variant_ids()
                product_ids.append(product.id)
                for variant in variants:
                    product_product = product_pro_obj.search([('barcode','=',variant.barcode)])
                    if not product_product.id:
                        color_value = attribute_value_obj.search([('attribute_id','=',attribute_color.id),('name','=',variant.color)])
                        size_value = attribute_value_obj.search([('attribute_id','=',attribute_size.id),('name','=',variant.size)])
                        value_ids = color_value.ids + size_value.ids
                        # remote_image1 = ''
                        # remote_image2 = ''
                        # try:
                        #     remote_image1 = sftp.open(record.image_path + variant.image_1.replace('\r',''))
                        #     remote_image1 = base64.encodestring(remote_image1.read())
                        # except:
                        #     # raise UserError(_(variant.image_1 + ' Image not found!'))
                        #         # /web/static/src/img/placeholder.png
                        #         img_path = get_module_resource('web', 'static/src/img', 'placeholder.png')
                        #         if img_path:
                        #             with open(img_path, 'rb') as f:
                        #                 image = f.read()
                        #         remote_image1 = base64.b64encode(image)
                        # try:
                        #     remote_image2 = sftp.open(record.image_path + variant.image_2.replace('\r',''))
                        #     remote_image2 = base64.encodestring(remote_image2.read())
                        # except:
                        #     # raise UserError(_(variant.image_2 + ' Image not found!'))
                        #     img_path = get_module_resource('web', 'static/src/img', 'placeholder.png')
                        #     if img_path:
                        #         with open(img_path, 'rb') as f:
                        #             image = f.read()
                        #     remote_image2 = base64.b64encode(image)
                        for product_pro in product.product_variant_ids:
                            value_ids.sort()
                            pro_value_ids = product_pro.attribute_value_ids.ids
                            pro_value_ids.sort()
                            if pro_value_ids == value_ids:
                                if product_pro.id:
                                    product_pro.write({
                                        # 'name':variant.name,
                                        # 'default_code':variant.internal_reference,
                                        'active':variant.is_active,
                                        'sale_ok':variant.sale_ok,
                                        'purchase_ok':variant.purchase_ok,
                                        'price_msrp':variant.price_msrp,
                                        'list_price': variant.standard_price, 
                                        'price_wholesale':variant.list_price,
                                        'type':product_type,
                                        'barcode':variant.barcode,
                                        'brand':variant.brand,
                                        'model':variant.model,
                                        'categ_id':categ_obj.search([('name','=',variant.categ_id)],limit=1).id or categ_obj.create({'name':variant.categ_id}).id,
                                        # 'image':remote_image1,
                                        # 'image_secondary':remote_image2,
                                        'image_url':variant.image_1_url or '',
                                        'image_secondary_url':variant.image_2_url or '',
                                    })
            record.product_ids = [(6,0,product_ids)]
            for tmpl_pro in record.product_ids:
                product_pro_obj.search([('product_tmpl_id','=',tmpl_pro.id),('barcode','in',[False, ' ', ''])]).unlink()
            record.state = 'done'

    @api.multi
    def action_import_product(self):
        for record in self:
            if record.attach_file:
                file_data = base64.b64decode(record.attach_file).decode("UTF-8").split('\n')
                file_data.pop(0)
                import_line_list = []
                record.import_line_ids.unlink()
                for line in file_data:
                    if line:
                        line = line.split(',')
                        print(line[0])
                        try:
                            import_line_list.append((0,0,{
                                'name':line[1],
                                # 'internal_reference':line[2],
                                'is_active':bool(int(line[2])),
                                'sale_ok':bool(int(line[3])),
                                'purchase_ok':bool(int(line[4])),
                                'list_price':float(line[5] or '0'),
                                'standard_price':float(line[6] or '0'),
                                'price_msrp': float(line[7] or '0'),
                                'type':line[8],
                                'barcode':line[9],
                                'brand':line[10],
                                'model':line[11],
                                'color':line[12] or 'None',
                                'size':line[13] or 'None',
                                'categ_id':line[14],
                                # 'image_1':line[15],
                                # 'image_2':line[16][:len(line[16])],
                                'image_1_url':line[15],
                                'image_2_url':line[16],
                            }))
                        except:
                            raise UserError(_('File is formet is not proper!'))
                record.import_line_ids = import_line_list
                record.state = 'process'

