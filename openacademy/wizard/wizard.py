#
# openacademy wizards
#

from osv import osv, fields


class Subscribe(osv.TransientModel):
    _name = 'openacademy.wizard.subscribe'

    _columns = {
        'session_id': fields.many2one('openacademy.session', string='Session', required=True),
        'attendee_ids': fields.one2many('openacademy.wizard.attendee', 'wizard_id', string='Attendees'),
    }

    def action_subscribe(self, cr, uid, ids, context=None):
        attendee_model = self.pool.get('openacademy.attendee')
        wizard = self.browse(cr, uid, ids[0], context)
        for attendee in wizard.attendee_ids:
            values = {
                'session_id': wizard.session_id.id,
                'partner_id': attendee.partner_id.id,
            }
            attendee_model.create(cr, uid, values, context)
        return {}


class Attendee(osv.TransientModel):
    _name = 'openacademy.wizard.attendee'

    _columns = {
        'wizard_id': fields.many2one('openacademy.wizard.subscribe'),
        'partner_id': fields.many2one('res.partner', string='Partner', required=True),
    }
