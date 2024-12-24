from odoo import api, fields, models, _, tools

class SaleOrderInh(models.Model):
    _inherit = "sale.order"
    _description = "Sale Order Inherited"

    sale_description = fields.Text(string="Sale Description")
