{
    'name' : 'Order Manager v3',
    'version' : '1.0',
    'summary': 'Demo Model Relation',
    'sequence': 1,
    'description': """

    """,
    'category': '',
    'website': '',
    'depends' : ['base'],
    'data': [
        'views/order_view.xml',
        'views/product_view.xml',
        'views/customer_view.xml',

        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
