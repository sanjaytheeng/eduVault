

{
    'name': 'eduvault Alumni',
    'version': '18.0.1.0.0',
    'license': 'LGPL-3',
    'category': 'eduvault',
    "sequence": 3,
    'summary': 'Manage Alumni',
    'complexity': "easy",
    'description': """
        This module provide alumni management system over OpenERP
    """,
    'author': 'eduvault Inc',
    'website': 'http://www.eduvault.org',
    'depends': ['eduvault_core'],
    'data': [
        'views/alumni_view.xml'
    ],
    'demo': [
        'demo/student_demo.xml',
        'demo/roll_number_demo.xml',
    ],
    'images': [
        'static/description/eduvault_alumni_banner.jpg',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
