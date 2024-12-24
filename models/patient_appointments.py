from odoo import api, fields, models, _, tools
from odoo.exceptions import ValidationError
from datetime import date, datetime



class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _description = "Hospital Appointments"
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name = fields.Char(
        string="Appointment Reference",
        required=True, copy=False, readonly=True,
        default=lambda self: _('New'))

    patient_id = fields.Many2one("hospital.patient", required=True, string="Patient")

    gender = fields.Char(string="Gender", readonly=1)
    patient_address = fields.Text(related="patient_id.address")

    note = fields.Text(string="Description", tracking=True)

    state = fields.Selection([
        ('draft', 'Draft'), ('confirm', 'Confirmed'),
        ('done', 'Done'), ('cancel', 'Cancelled')
    ], default='draft', string='Status', tracking=True)

    ap_booking_date = fields.Date(string="Booking Date", default=date.today(), readonly=1)
    checkup_date = fields.Datetime(string="Checkup Time", default=date.today())

    doctor_id = fields.Many2one("hospital.doctor", string="Doctor", tracking=True, required=1)
    prescription = fields.Text(string="Prescription")
    prescription_line_ids = fields.One2many("appointment.prescription.lines", "appointment_id")


    saleorder_count = fields.Integer(string="Sale Orders", compute="_compute_saleorders")

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    def action_done(self):
        for rec in self:
            if rec.state == 'confirm':
                rec.state = 'done'
            else:
                raise ValidationError('You can only move to Done from Confirm.')

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    @api.model
    def create(self, vals):
        print(vals)

        vals['name'] = self.env['ir.sequence'].next_by_code("hospital.appointment")
        res = super(HospitalAppointment, self).create(vals)

        return res

    def unlink(self):
        for rec in self:
            if rec.state == 'done':
                raise ValidationError('You cannot delete an Appointment at Done State.')
            else:
                return super(HospitalAppointment, rec).unlink()

    @api.onchange('patient_id')
    def onchange_gender(self):
        if self.patient_id:
            self.gender = self.patient_id.gender

    @api.constrains('ap_booking_date', 'checkup_date')
    def validate_appointment_date(self):
        for rec in self:
            if rec.ap_booking_date and rec.checkup_date:
                checkup_date = rec.checkup_date.date()

                if checkup_date < rec.ap_booking_date:
                    raise ValidationError("Checkup Time must come after Booking Time")


    def action_create_saleorder(self):
        print("Button Sale order")
        line_ids = []

        for line in self.prescription_line_ids:
            line_ids.append((0, 0, {
                'product_id': line.product_id.id,
                'name': line.name,
                'product_uom_qty': line.qty,
                'price_unit': line.price,
            }))

        print("Partner=>",self.patient_id.partner_id)

        record = self.env['sale.order'].create({
            'partner_id': self.patient_id.partner_id.id,
            'date_order': self.checkup_date,
            'sale_description': self.note,
            'order_line': line_ids,
        })


    def _compute_saleorders(self):
        for rec in self:
            saleorders = self.env['sale.order'].search_count([('partner_id', '=', rec.patient_id.partner_id.id)])

            rec.saleorder_count = saleorders


    def action_view_saleorders(self):
        action = self.env.ref('sale.action_quotations_with_onboarding').read()[0]
        action['domain'] = [('partner_id', '=', self.patient_id.partner_id.id)]
        return action




class AppointmentPrescriptionLines(models.Model):
    _name = "appointment.prescription.lines"
    _description = "Appointment Prescription Lines"

    name = fields.Char(string="Name")
    product_id = fields.Many2one("product.product", string="Product Id")
    qty = fields.Integer(string="Quantity")
    price = fields.Float(related="product_id.lst_price", string="Price")
    total = fields.Float(string="Total", readonly=True)

    appointment_id = fields.Many2one("hospital.appointment", string="Appointment Id")

    @api.onchange('price', 'qty')
    def _onchange_total(self):
        self.total = self.qty * self.price

