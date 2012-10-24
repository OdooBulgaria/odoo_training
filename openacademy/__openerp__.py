#
# openacademy manifest
#
{
    'name': 'Open Academy',
    'author': 'The Dream Team',
    'version': '1.0',
    'category': 'Tools',
    'description': """
        This module manages training stuff:
         - training courses,
         - training sessions,
         - attendee subscription
    """,
    'depends': ['base'],
    'data': [
        'openacademy_view.xml',
	    'partner_view.xml',
        'openacademy_data.xml',
        'workflow/openacademy.xml',
        'access/openacademy_groups.xml',
        'access/ir.model.access.csv',
        'wizard/openacademy_wizard_view.xml'
    ],
}
