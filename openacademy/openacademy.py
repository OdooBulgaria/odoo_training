#
# module openacademy
#

from osv import osv, fields
import time
from datetime import datetime, timedelta

class Course(osv.Model):
    _name = 'openacademy.course'

    def copy(self, cr, uid, id, values, context=None):
		if 'name' not in values:
			course = self.browse(cr, uid, id, context)
			values['name'] = '%s (copy)' % course.name
			values['session_ids'] = [] #prevent duplication of the sessions and the members
		return super(Course, self).copy(cr, uid, id, values, context=context)

    def _constraint_name(self, cr, uid, ids):
		for course in self.browse(cr, uid, ids):
			if course.name == course.description: 
				return False 
			return True


    _columns = {
        'name': fields.char('Name', size = 128, required = True),
        'description': fields.text('Description'),
		"active" : fields.boolean("Active"),

        "session_ids" : fields.one2many("openacademy.session", "course_id", string="Session"),
        "responsible_id" : fields.many2one("res.users", string = "Responsible"),
    }

    _defaults = {
		"active" : True
    }

    _constraints = [
    	(_constraint_name, "The course name and description must be different", ["name", "description"])
    ]

    _sql_constraints = [
    	('name_uniq','UNIQUE(name)', 'Course names must be unique')
    ]

class Session(osv.Model):
	_name = 'openacademy.session'

	def _calculate_percentage_filled(self, cr, uid, ids, name, arg, context = None):
		res = {}
		for session in self.browse(cr, uid, ids, context):
			res[session.id] = 100 * float(len(session.attendee_ids)) / float(session.seats) if session.seats else 0
		return res

	def _default_start_date(self, cr, uid, context):
		return time.strftime('%Y-%m-%d')

	def _calculate_stop_date(self, cr, uid, ids, name, args, context=None):
		res = {}
		for sess in self.browse(cr, uid, ids, context):
			if sess.startdate and sess.duration > 0:
				dt = datetime.strptime(sess.startdate, '%Y-%m-%d %H:%M:%S')
				dt = dt + timedelta(days=sess.duration, minutes=-1)
			res[sess.id] = dt.strftime('%Y-%m-%d %H:%M:%S')
		return res

	def action_reset(self, cr, uid, ids, context=None):
		for session in self.browse(cr, uid, ids, context):
			return self.write(cr, uid, session.id, {"state" : "draft"})

	def action_confirm(self, cr, uid, ids, context=None):
		for session in self.browse(cr, uid, ids, context):
			return self.write(cr, uid, session.id, {"state" : "confirmed"})

	def action_done(self, cr, uid, ids, context=None):
		for session in self.browse(cr, uid, ids, context):
			return self.write(cr, uid, session.id, {"state" : "done"})

	_columns = {
		'name': fields.char('Name', size = 128, required = True),
		"startdate" : fields.datetime("StartDate"),
		"stopdate" : fields.function(_calculate_stop_date, type="datetime", string="Stop Date"),
		"duration" : fields.float("Duration", digits = (5,1), help = "The duration of the session in days"),
		"seats" : fields.integer("Seats"),
		"percentage_filled" : fields.function(_calculate_percentage_filled, type="integer", string="Percentage Filled"),

		"state" : fields.selection(
			[
				("draft", "Draft"),
				("confirmed", "Confirmed"),
				("done", "Done")
			], 'Stage', required=True, readonly=True
		),

		"instructor_id" : fields.many2one("res.partner", string="Instructor", 
			domain = ['|', ("is_instructor", '=', True), ("category_id", "child_of", "Teacher")]
		),
		"course_id" : fields.many2one("openacademy.course", required = True, string = "Related Course"),
		"attendee_ids" : fields.one2many("openacademy.attendee", "session_id", string = "Attendees"),
		"partner_id" : fields.many2one("res.partner")
	}

	_defaults = {
		"startdate" : _default_start_date,
		"state" : "draft"
	}
	
class Attendee(osv.Model):
	_name = 'openacademy.attendee'

	_columns = {
        'name': fields.char('Name', size = 128, required = False),

        "partner_id" : fields.many2one("res.partner", string="Partner"),
    	"session_id" : fields.many2one("openacademy.session", required = True)
    }
