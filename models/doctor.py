from email.policy import default

from odoo import api, fields, models, _, tools


class HospitalDoctor(models.Model):
    _name = "hospital.doctor"
    _description = "Hospital Doctor"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name", required=True, tracking=True)
    age = fields.Integer(string="Age", tracking=True, default=18, copy=False)
    active = fields.Boolean('Active', default=True)

    reference = fields.Char(
        string="Doctor Reference",
        required=True, copy=False, readonly=True,
        default=lambda self: _('New'))

    gender = fields.Selection([
        ("male", "Male"),
        ("female", "Female"),
    ], required=True, default='male', tracking=True)

    specialties = fields.Selection([
        ("al_immun", "Allergy and Immunology"),
        ("anesthesiology", "Anesthesiology"),
        ("cardiology", "Cardiology"),
        ("dermatology", "Dermatology"),
        ("forensic", "Forensic Pathology"),
    ], required=True, default='al_immun', tracking=True)

    address = fields.Text(string="Home Address", tracking=True, copy=False)

    image = fields.Binary(string="Image")

    @api.model
    def create(self, vals):
        vals['reference'] = self.env['ir.sequence'].next_by_code("hospital.doctor")
        res = super(HospitalDoctor, self).create(vals)
        return res


    def copy(self, default=None):
        if default is None:
            default = {}
        print(default)
        if not default.get('name'):
            default['name'] = _("%s (Copy)", self.name)

        return super(HospitalDoctor, self).copy(default)
