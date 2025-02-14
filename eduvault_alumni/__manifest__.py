{
    'name': 'eduvault Alumni',
    'version': '18.0.1.0',
    'license': 'LGPL-3',
    'category': 'eduvault',
    "sequence": 3,
    'summary': 'Manage Alumni',
    'complexity': "easy",
    'author': 'eduvault Inc',
    'website': 'https://www.eduvault.org',
    'depends': ['base','eduvault_core'],
    'data': [
        'views/alumni_menu.xml',
        'views/alumni_view.xml',
        'views/op_student_alumni_button.xml',
        'security/ir.model.access.csv',

    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
