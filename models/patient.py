from odoo import api, fields, models, _, tools
from odoo.exceptions import ValidationError


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _description = "Hospital Patient"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _inherits = {'res.partner': 'partner_id'}

    @api.model
    def default_get(self, fields_list):
        res = super(HospitalPatient, self).default_get(fields_list)
        res['note'] = "N/A"
        return res

    #name = fields.Char(string="Name", required=True, tracking=True)
    age = fields.Integer(string="Age", tracking=True, default=18)

    reference = fields.Char(
        string="Patient Reference",
        required=True, copy=False, readonly=True,
        default=lambda self: _('New'))

    gender = fields.Selection([
        ("male", "Male"),
        ("female", "Female"),
    ], required=True, default='male', tracking=True)

    note = fields.Text(string="Description", tracking=True)

    state = fields.Selection([
        ('draft', 'Draft'), ('confirm', 'Confirmed'),
        ('done', 'Done'), ('cancel', 'Cancelled')
    ], default='draft', string='Status', tracking=True)

    responsible_id = fields.Many2one("res.partner", string="Responsible")

    appointment_count = fields.Integer(string="Appointments", compute="_compute_appointments")

    address = fields.Text(string="Home Address", tracking=True)

    #image = fields.Binary(string="Image")
    #email = fields.Char(string="Email")
    #mobile_no = fields.Char(string="Mobile No")

    partner_id = fields.Many2one("res.partner", string="Partner")
    website = fields.Char(string="Website Link")
    active = fields.Boolean(string="Active", default=True)

    appointment_line_ids = fields.One2many("hospital.appointment", "patient_id", string="Appointment Lines")

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    def go_to_website(self):
        if not self.website:
            raise ValidationError("Website is not Given")
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': self.website,
        }

    @api.model
    def create(self, vals):

        if not vals['note']:
            vals['note'] = "No Description"

        vals['reference'] = self.env['ir.sequence'].next_by_code("hospital.patient")
        res = super(HospitalPatient, self).create(vals)


        # record = self.env['res.partner'].create({
        #     'name': res['name'],
        #     'phone': res['mobile_no'],
        #     'email': res['email'],
        #     'image_1920': res['image'],
        # })
        #
        # res['partner_id'] = record.id

        return res

    def unlink(self):
        for rec in self:
            if rec.state == 'done':
                raise ValidationError('You cannot delete a Patient at Done State.')
            elif self.appointment_count:
                raise ValidationError('You cannot delete a Patient with Appointments.')
            else:
                record = self.env["res.partner"].browse(rec.partner_id.id)
                print(record.id, record.name)
                record.unlink()
                return super(HospitalPatient, rec).unlink()

    def _compute_appointments(self):
        for rec in self:
            appointments = self.env["hospital.appointment"].search_count([('patient_id', '=', rec.id)])
            rec.appointment_count = appointments

    # def _compute_appointments(self):
    #     appointments = self.env["hospital.appointment"].search([])
    #     for patient in self:
    #         count = 0
    #         for rec in appointments:
    #             if rec.patient_id.id == patient.id:
    #                 count += 1
    #
    #         patient.appointment_count = count

    def action_view_appointments(self):
        action = self.env.ref('hospital.action_hospital_appointment').read()[0]
        action['domain'] = [('patient_id', '=', self.id)]
        return action

    def name_get(self):
        return [(record.id, "[%s] %s" % (record.reference, record.name)) for record in self]