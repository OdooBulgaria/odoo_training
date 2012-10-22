#
# module openacademy
#

from osv import osv, fields

class Course(osv.Model):
    _name = 'openacademy.course'

    _columns = {
        'name': fields.char('Name', size = 128, required = True),
        'description': fields.text('Description'),

        "session_ids" : fields.one2many("openacademy.session", "course_id", String="Session"),
        "responsible_id" : fields.many2one("res.users", String = "Responsible"),
    }

class Session(osv.Model):
	_name = 'openacademy.session'

	_columns = {
		'name': fields.char('Name', size = 128, required = True),
		"startdate" : fields.datetime("StartDate"),
		"duration" : fields.float("Duration", digits = (5,1), help = "The duration of the session in hours"),
		"seats" : fields.integer("Seats"),

		"instructor_id" : fields.many2one("res.partner", String="Instructor", 
			domain = ['|', ("is_instructor", '=', True), ("category_id", "child_of", "Teacher")]
		),
		"course_id" : fields.many2one("openacademy.course", required = True, String = "Related Course"),
		"attendee_ids" : fields.one2many("openacademy.attendee", "session_id", String = "Attendees"),
		"partner_id" : fields.many2one("res.partner", required = True)
	}
	
class Attendee(osv.Model):
	_name = 'openacademy.attendee'

	_columns = {
        'name': fields.char('Name', size = 128, required = False),

        "partner_id" : fields.many2one("res.partner", String="Partner"),
    	"session_id" : fields.many2one("openacademy.session", required = True)
    }
