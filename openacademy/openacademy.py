#
# module openacademy
#

from osv import osv, fields

class Course(osv.Model):
    _name = 'openacademy.course'

    _columns = {
        'name': fields.char('Name', size = 128, required = True),
        'description': fields.text('Description'),

        "session_ids" : fields.one2many("openacademy.session", "course_id", string="Session"),
        "responsible_id" : fields.many2one("res.users", string = "Responsible"),
    }

class Session(osv.Model):
	_name = 'openacademy.session'

	def _calculate_percentage_filled(self, cr, uid, ids, name, arg, context = None):
		res = {}
		for session in self.browse(cr, uid, ids, context):
			res[session.id] = 100 * float(len(session.attendee_ids)) / float(session.seats) if session.seats else 0
		return res

	_columns = {
		'name': fields.char('Name', size = 128, required = True),
		"startdate" : fields.datetime("StartDate"),
		"duration" : fields.float("Duration", digits = (5,1), help = "The duration of the session in hours"),
		"seats" : fields.integer("Seats"),
		"percentage_filled" : fields.function(_calculate_percentage_filled, type="integer", string="Percentage Filled"),

		"instructor_id" : fields.many2one("res.partner", string="Instructor", 
			domain = ['|', ("is_instructor", '=', True), ("category_id", "child_of", "Teacher")]
		),
		"course_id" : fields.many2one("openacademy.course", required = True, string = "Related Course"),
		"attendee_ids" : fields.one2many("openacademy.attendee", "session_id", string = "Attendees"),
		"partner_id" : fields.many2one("res.partner", required = True)
	}
	
class Attendee(osv.Model):
	_name = 'openacademy.attendee'

	_columns = {
        'name': fields.char('Name', size = 128, required = False),

        "partner_id" : fields.many2one("res.partner", string="Partner"),
    	"session_id" : fields.many2one("openacademy.session", required = True)
    }
