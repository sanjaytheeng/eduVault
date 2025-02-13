
{
    'name': "eduvault Admission",
    'version': '18.0.1.0',
    'license': 'LGPL-3',
    'category': 'eduvault',
    'sequence': 3,
    'summary': "Manage Admissions""",
    'complexity': "easy",
    'author': 'eduvault Inc',
    'website': 'https://www.eduvault.org',
    'depends': [
        'eduvault_core',
        'eduvault_fees'
    ],
    'data': [
        'security/op_admission_security.xml',
        'security/ir.model.access.csv',
        'data/admission_sequence.xml',
        'data/parameter_data.xml',
        'views/admission_register_view.xml',
        'views/admission_view.xml',
        'report/report_admission_analysis.xml',
        'report/report_menu.xml',
        'wizard/admission_analysis_wizard_view.xml',
        'menus/op_menu.xml',
    ],
    'demo': [
        'demo/admission_register_demo.xml',
        'demo/admission_demo.xml',
    ],
    'test': [],
    'images': [
        'static/description/eduvault_admission_banner.jpg',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
