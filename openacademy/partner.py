#
# module openacademy
#

from osv import osv, fields


class Partner(osv.Model):
	_inherit = "res.partner"

	_columns = {
		"is_instructor" : fields.boolean('Is Instructor'),

		#"session_ids" : fields.one2many("openacademy.session", "partner_id", String = "Instructor For")
	}