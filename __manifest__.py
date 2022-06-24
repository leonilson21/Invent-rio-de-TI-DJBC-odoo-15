# -*- coding: utf-8 -*-
{
    'name': "DJBC IT Inventory",

    'summary': """
        Laporan IT Inventory DJBC""",

    'description': """
        Laporan IT Inventory DJBC untuk fasilitas TPB (KB, PLB, GB), KITE dan Non Fasilitas (Umum). 
    """,

    'author': "Oktovan Rezman",
    'website': 'https://www.prune.id',
    'license': 'AGPL-3',
    'images': [
     #   'images/ptp.png', 
     #   'images/tes.png', 
        'images/main_screenshot.png'
    ],

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Extra Tools',
    'version': '15.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['stock','product'],

    # always loaded
    'data': [
	    'views/stock_location.xml',
        'views/stock_picking.xml',
	    #'views/stock_picking_type.xml',
	    'security/security.xml',
        'security/ir.model.access.csv',
	    'views/doctype.xml',
        'views/docs.xml',
        'views/hscode.xml',
	    'views/categs.xml',
        #'views/stock_move.xml',
        'views/menu.xml',
        #'views/stock_inventory.xml',
        'views/product_template.xml',
        'views/container.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'application' : True
}
