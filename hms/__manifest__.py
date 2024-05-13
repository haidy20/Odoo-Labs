
{
    'name': 'hms',
    'version': '1.0',
    'description': 'Module for managing patient data in hospitals',
    'author': 'mo-ismail',
    'depends': ['crm'],
    'data': [
        'security/ir.model.access.csv',
        'security/res_group.xml',
        'views/patient_views.xml',
        'views/department_views.xml',
        'views/doctor.views.xml',
        #'views/patient_log_views.xml',
        'views/customer.views.xml',
        'reports/hms_patient_template.xml',
        'reports/reports.xml',
    ],
}