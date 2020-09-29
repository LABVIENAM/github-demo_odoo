{
    'name': 'My Academy',
    'version':"1",
    'description':"Module Academy",
    'author':"Huu Phong",
    'depends':["base"],
    'data':[

        #views
        'views/student.xml',
        'views/course.xml',
        'views/order_course.xml',
        'views/session.xml',

        #security
        'security/account_security.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}