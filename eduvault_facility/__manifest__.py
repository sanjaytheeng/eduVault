

{
    'name': 'eduvault Facility',
    'version': '18.0.1.0',
    'license': 'LGPL-3',
    'category': 'Education',
    "sequence": 3,
    'summary': 'Manage Facility',
    'complexity': "easy",
    'author': 'eduvault Inc',
    'website': 'https://www.eduvault.org',
    'depends': ['eduvault_core'],
    'data': [
        'security/ir.model.access.csv',
        'views/facility_view.xml',
        'views/facility_line_view.xml',
        'menus/op_menu.xml',
    ],
    'demo': [
        'demo/facility_demo.xml'
    ],
    'images': [
        'static/description/eduvault_facility_banner.jpg',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
