#
# module openacademy
#

from osv import osv, fields

class Course(osv.Model):
    _name = 'openacademy.course'

    _columns = {
        'name': fields.char('Name', size=128, required=True),
        'description': fields.text('Description'),
    }
