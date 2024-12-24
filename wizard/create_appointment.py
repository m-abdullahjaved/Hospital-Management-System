from odoo import api, fields, models, _

class CreateAppointmentWizard(models.TransientModel):
    _name = "create.appointment.wizard"
    description = "Create Appointment Wizard"

    def default_get(self,fields_list):
        res = super(CreateAppointmentWizard, self).default_get(fields_list)
        if self._context.get('active_id'):
            print(self._context)
            print("Here=>",self._context.get('active_id'))
            res['patient_id'] = self._context.get('active_id')
        return res

    patient_id = fields.Many2one("hospital.patient", string="Patient Id")
    date_appointment = fields.Date(string="Appointment Date")


    def action_create_appointment(self):
        vals = {
            'patient_id': self.patient_id.id,
            'ap_booking_date': self.date_appointment,
        }

        appointment_id = self.env["hospital.appointment"].create(vals)
        if appointment_id:
            appointment_id.onchange_gender()

        return {
            "type": "ir.actions.act_window",
            "res_model": "hospital.appointment",
            "res_id": appointment_id.id,
            "view_mode": "form",
            "target": "new",
            "name": _("Appointment"),
        }