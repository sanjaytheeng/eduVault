

{
    'name': 'eduvault Health',
    'version': '18.0.1.0.0',
    'license': 'LGPL-3',
    'category': 'eduvault',
    "sequence": 3,
    'summary': 'Manage Health',
    'complexity': "easy",
    'description': """
        This module adds the feature of health in eduvault
    """,
    'author': 'eduvault Inc',
    'website': 'http://www.eduvault.org',
    'depends': ['base','eduvault_core'],
    'data': [
        'views/health_view.xml',
        'security/ir.model.access.csv',
        'health_menu.xml',
    ],
    'demo': [
        'demo/health_line_demo.xml',
        'demo/health_demo.xml'
    ],
    'images': [
        'static/description/eduvault_health_banner.jpg',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
