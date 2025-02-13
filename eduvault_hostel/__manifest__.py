

{
    'name': 'eduvault Hostel',
    'version': '18.0.1.0.0',
    'license': 'LGPL-3',
    'category': 'eduvault',
    "sequence": 3,
    'summary': 'Manage Hostels',
    'complexity': "easy",
    'description': """
        This module adds hostel management feature to eduvault_Core.
    """,
    'author': 'eduvault Inc',
    'website': 'http://www.eduvault.org',
    'depends': ['eduvault_core', 'eduvault_facility'],
    'data': [
        'views/room_view.xml',
        'views/hostel_view.xml',
        'views/hostel_room_view.xml',
        'hostel_menu.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [
        'demo/hostel_demo.xml',
        'demo/room_demo.xml',
        'demo/hostel_room_demo.xml',
    ],
    'images': [
        'static/description/eduvault_hostel_banner.jpg',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
