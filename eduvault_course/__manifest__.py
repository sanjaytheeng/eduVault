# -*- coding: utf-8 -*-
{
    'name': "eduvault_course",
    'summary': "Course Management Feature",
    'description': """
Long description of module's purpose
    """,
    'author': "Pranish Lama",
    'license': 'LGPL-3',
    'category': 'eduvault',
    "sequence": 3,
    'version': '0.1',
    'depends': ['base', 'eduvault_core'],
    'data': [
        'security/ir.model.access.csv',
        'views/student_course.xml',
    ],
}

