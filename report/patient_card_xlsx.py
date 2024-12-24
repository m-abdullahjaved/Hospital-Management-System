from odoo import models
import base64
import io


class PatientCardXlsx(models.AbstractModel):
    _name = 'report.hospital.patient_report_card_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, patients):
        sheet = workbook.add_worksheet('Patient ID Card')
        bold = workbook.add_format({'bold': True})
        format_id_card = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': 'yellow'})
        row = 3
        col = 3
        for obj in patients:
            sheet.merge_range(row, col, row, col + 1, "ID Card", format_id_card)
            row += 1

            if obj.image:
                patient_image = io.BytesIO(base64.b64decode(obj.image))
                sheet.insert_image(row, col, "image.png", {"image_data": patient_image, 'x_scale': 0.1, 'y_scale': 0.1})

                row += 5

            # Name
            sheet.write(row, col, 'Name', bold)
            sheet.write(row, col + 1, obj.name)
            row += 1
            # Age
            sheet.write(row, col, 'Age', bold)
            sheet.write(row, col + 1, obj.age)
            row += 1
            # Gender
            sheet.write(row, col, 'Gender', bold)
            sheet.write(row, col + 1, obj.gender)
            row += 1
            # Appointments
            sheet.write(row, col, 'Appointments', bold)
            sheet.write(row, col + 1, obj.appointment_count)

            row += 3
