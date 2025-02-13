
{
    'name': 'eduvault Assignment',
    'version': '18.0.1.0',
    'license': 'LGPL-3',
    'category': 'eduvault',
    "sequence": 3,
    'summary': 'Manage Assgiments',
    'complexity': "easy",
    'author': 'eduvault Inc',
    'website': 'https://www.eduvault.org',
    'depends': [
        'base_automation',
        'eduvault_core',
    ],
    'data': [
        'security/op_security.xml',
        'security/ir.model.access.csv',
        'views/assignment_view.xml',
        'views/assignment_type_view.xml',
        'views/assignment_sub_line_view.xml',
        'views/student_view.xml',
        'data/action_rule_data.xml',
        'menus/op_menu.xml',
    ],
    'demo': [
        'demo/assignment_type_demo.xml',
        'demo/assignment_demo.xml',
        'demo/assignment_sub_line_demo.xml'
    ],
    'images': [
        'static/description/eduvault_assignment_banner.jpg',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
