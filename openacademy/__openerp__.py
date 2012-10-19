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
    ],
}
