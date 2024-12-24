# -*- coding: utf-8 -*-
{
    'name': 'Hospital',
    'version': '16.0.0',
    'summary': 'Hospital Management',
    'author': 'Abdullah Javed',
    'sequence': -1,
    'description': """
        Hospital Management System
    """,
    'category': 'Hospital',

    'depends': ['web', 'sale', 'mail', 'report_xlsx'],

    'data': [
        'security/ir.model.access.csv',

        'data/data.xml',

        'wizard/create_appointment_wizard.xml',

        'views/patient.xml',
        'views/kids_view.xml',
        'views/sale_order.xml',
        'views/patient_gender_view.xml',
        'views/appointment_view.xml',
        'views/doctor.xml',
        'views/view_partner_inherit.xml',

        'views/menu.xml',

        'report/patient_card_template.xml',
        'report/report.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,

    'license': 'LGPL-3',
}
