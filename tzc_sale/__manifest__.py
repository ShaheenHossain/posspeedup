# -*- coding: utf-8 -*-
{
    'name': 'Tanzacan: sale',
    'summary': 'Tanzacan: Sales Catalog',
    'description': """
    * Function spec:
		- Sales person will go to products (default to list view with image) 
		- Select items they want to add to the catalog with the check box 
		- there will be an item in "action" to add to catalog, they will be asked if they want to add to existing or a new catalog 
		- Once all the items are added to the catalog, they can adjust the qty and pricing to send to the customer. 
		- They can also decide if they do not want the customer to see the pricing and/or qty 
		- They can then select "Send" and select from the existing customer list. This should be a check box list, so they can select 15+ customers at once 
		- The email sent will have good size images (both image associated with the product)  size of images TBD.
		- When the email is sent it should create a quotation and use the link to the online quotation in the email  
		- If the customer wishes to purchase they can click a button at the bottom of the email (wording of the button is TBD) 
		- This redirects them to the quotation page, this will show the products in the catalog with image. They will be able to edit the qty
		- If they want to change the pricing they can send a message to the salesperson from this page to discuss
		- If the customer adds more qty than what is available a pop up warning should appear to let them know what the real stock is. and that the remaining items may be back ordered. 
		- The catalogs should live in a menu item in sales. The sales person should be able to tick the box next to several catalogs and merge
		- Button on catalog that links to all quotations created from that catalog 
		- Button on the SO that links to the catalog used (if any) 
		- On the catalog we will need it to show the current stock on the back and front end. There should be a button on the catalog to "update real inventory" that should re-cacluate the inventory on hand set on the catalog 
		- If the sales price gets changed in the SO that should log a note in the chatter per item changed (ie it should say "product a changed from $100 --> $90, product b changed from $50 --> $35, etc) 
		- option to see if the quote was opened by the customer 
    """,
    'license': 'OEEL-1',
    'author': 'Odoo Inc',
    'version': '0.1',
    'depends': ['sale_stock', 'website_sale', 'website_quote'],
    'data': [
        'security/ir.model.access.csv',
        'security/sale_catalog_groups.xml',
        'data/mail_templates.xml',
        'views/mail_compose_message.xml',
        'wizard/sale_catalog_wizard.xml',
        'wizard/product_template_wizard.xml',
        'views/sale_catalog.xml',
        'views/sale_order.xml',
        'views/product_template.xml',
        'views/website_sale.xml',
        'views/sale_portal_templates.xml'
    ],
}