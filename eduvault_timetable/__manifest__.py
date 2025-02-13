
{
    'name': 'eduvault Timetable',
    'version': '18.0.1.0',
    'license': 'LGPL-3',
    'category': 'eduvault',
    "sequence": 3,
    'summary': 'Manage TimeTables',
    'complexity': "easy",
    'author': 'eduvault Inc',
    'website': 'https://www.eduvault.org',
    'depends': ['eduvault_classroom'],
    'data': [
        'security/op_security.xml',
        'security/ir.model.access.csv',
        'views/timetable_view.xml',
        'views/timing_view.xml',
        'views/faculty_view.xml',
        'views/res_config_setting_view.xml',
        'report/report_timetable_student_generate.xml',
        'report/report_timetable_teacher_generate.xml',
        'report/report_menu.xml',
        'wizard/generate_timetable_view.xml',
        'wizard/time_table_report.xml',
        'wizard/session_confirmation.xml',
        'views/timetable_templates.xml',
        'menus/op_menu.xml',
    ],
    'demo': [
        'demo/timing_demo.xml',
        'demo/op_timetable_demo.xml'
    ],
    'images': [
        'static/description/eduvault_timetable_banner.jpg',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
