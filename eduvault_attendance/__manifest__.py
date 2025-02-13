

{
    'name': 'eduvault Attendance',
    'version': '18.0.1.0',
    'license': 'LGPL-3',
    'category': 'eduvault',
    "sequence": 3,
    'summary': 'Manage Attendances',
    'complexity': "easy",
    'author': 'eduvault Inc',
    'website': 'https://www.eduvault.org',
    'depends': ['eduvault_timetable'],
    'data': [
        'security/op_security.xml',
        'security/ir.model.access.csv',
        'data/attendance_sheet_sequence.xml',
        'wizards/student_attendance_wizard_view.xml',
        'views/attendance_register_view.xml',
        'views/attendance_sheet_view.xml',
        'views/attendance_line_view.xml',
        'views/attendance_type_view.xml',
        'views/attendance_session_view.xml',
        'views/student_view.xml',
        'report/student_attendance_report.xml',
        'report/report_menu.xml',
        'menus/op_menu.xml'
    ],
    'demo': [
        'demo/attendance_register_demo.xml',
        'demo/attendance_sheet_demo.xml',
        'demo/attendance_line_demo.xml',
    ],
    'images': [
        'static/description/eduvault_attendance_banner.jpg',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
