{
    'name': 'eduvault eLearning',
    'version': '18.0.1.0',
    'license': 'LGPL-3',
    'category': 'eduvault',
    "sequence": 3,
    'summary': 'Manage eLearning courses of students',
    'complexity': "easy",
    'author': 'eduvault Inc',
    'depends': [
        'eduvault_core',
        'eduvault_fees',
        'eduvault_core',
    ],
    'data': [
        'views/extend_course_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
