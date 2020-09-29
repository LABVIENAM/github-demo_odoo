from odoo import models, fields, api
from odoo.exceptions import except_orm, ValidationError
from odoo.osv import osv
import xlrd
import base64
from datetime import datetime
from dateutil.relativedelta import relativedelta


class StockInventoryCustomer(models.Model):
    _inherit = 'stock.inventory.customer.update'

    type = fields.Selection(
        [('product', 'Product'), ('coin', 'Coin'), ('money', 'Money'), ('service_history', 'Service History')],
        default='coin')
    history_id = fields.One2many('import.service.history', 'inventory_id')

    @api.multi
    def download_template(self):
        return {
            "type": "ir.actions.act_url",
            "url": '/import_service_history/static/template/1.xlsx',
            "target": "_parent",
        }

    @api.multi
    def download_template_coin_product_money(self):
        return {
            "type": "ir.actions.act_url",
            "url": '/import_service_history/static/template/2.xlsx',
            "target": "_parent",
        }

    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    @api.multi
    def import_service_history(self):
        try:
            if not self._check_format_excel(self.field_binary_name):
                raise osv.except_osv("Cảnh báo!",
                                     (
                                         "File không được tìm thấy hoặc không đúng định dạng. Vui lòng kiểm tra lại định dạng file .xls hoặc .xlsx"))
            data = base64.decodestring(self.field_binary_import)
            excel = xlrd.open_workbook(file_contents=data, encoding_override="cp1252")
            sheet = excel.sheet_by_index(0)
            index = 2
            lines = []
            while index < sheet.nrows:
                emp_ids = []
                emp1_ids = []
                doc_ids = []
                # customer_code = sheet.cell(index, 0).value
                # customer_id = self.env['res.partner'].search([('x_code', '=', customer_code)])
                partner_code = sheet.cell(index, 0).value
                if self.is_number(partner_code):
                    partner_code = '0' + str(int(partner_code))
                customer_id = self.env['res.partner'].search(
                    ['|', '|', '|', ('x_code', '=', partner_code.strip().upper()),
                     ('x_old_code', '=', partner_code.strip().upper()), ('phone', '=', partner_code.strip().upper()),
                     ('mobile', '=', partner_code.strip().upper())], limit=1)
                if not customer_id:
                    raise ValidationError(
                        'Không tìm thấy khách hàng có mã %s.Vui lòng kiểm tra lại dòng %s' % (partner_code, index + 1))
                date = sheet.cell(index, 2).value
                type_ = sheet.cell(index, 3).value
                type = type_.upper()
                if type not in ['DV', 'TDV', 'BH']:
                    raise ValidationError('Bạn chưa chọn đúng loại dịch vụ.Vui lòng chọn lại.Xin cám ơn!')
                service_code = sheet.cell(index, 4).value
                service_id = self.env['product.product'].search([('default_code', '=', service_code)])
                if not service_id:
                    raise ValidationError(
                        'Không tìm thấy dịch vụ có mã %s.Vui lòng kiểm tra lại dòng %s' % (service_code, index + 1))
                amount = sheet.cell(index, 6).value
                if amount <= 0:
                    raise ValidationError(
                        'Số lượng phải lớn hơn 0 tại dòng %s' % (index + 1))
                employee_code = sheet.cell(index, 7).value
                emp_code = employee_code.split(',')
                for emp in emp_code:
                    if emp:
                        department_ids = self.env['hr.department'].search(
                            [('x_branch_id', '=', self.session_id.config_id.pos_branch_id.id)])
                        for line in department_ids:
                            ids_o2m = self.env['hr.employee'].search(
                                [('department_id', '=', line.id), ('x_work_service', '=', True),
                                 ('x_employee_code', '=', emp)])
                        if ids_o2m:
                            for id in ids_o2m:
                                emp_ids.append(id.id)
                        else:
                            raise ValidationError(
                                    'Vui lòng kiểm tra lại kĩ thuật viên có mã %s tại dòng %s' % (emp, index + 1))

                employee1_code = sheet.cell(index, 9).value
                emp1_code = employee1_code.split(',')
                for emp1 in emp1_code:
                    if emp1:
                        department_ids = self.env['hr.department'].search(
                            [('x_branch_id', '=', self.session_id.config_id.pos_branch_id.id)])
                        for line in department_ids:
                            ids_o2m = self.env['hr.employee'].search(
                                [('department_id', '=', line.id), ('x_work_service', '=', True),
                                 ('x_employee_code', '=', emp1)])
                        if ids_o2m:
                            for id in ids_o2m:
                                emp1_ids.append(id.id)
                        else:
                            raise ValidationError(
                                'Vui lòng kiểm tra lại kĩ thuật viên phụ có mã %s tại dòng %s' % (emp1, index + 1))
                doctor_code = sheet.cell(index, 11).value
                doctor_code_ = doctor_code.split(',')
                for doc in doctor_code_:
                    if doc:
                        doctor_ids = self.env['hr.employee'].search(
                            [('x_employee_code', '=', doc), ('job_id.x_code', '=', 'BS')])
                        if doctor_ids:
                            doc_ids.append(doctor_ids.id)
                        else:
                            raise ValidationError(
                                'Vui lòng kiểm tra lại bác sĩ có mã %s tại dòng %s' % (doc, index + 1))

                note = sheet.cell(index, 13).value
                date_cvt = datetime.strptime(date, '%d/%m/%Y').date()
                val = {
                    'customer_id': customer_id.id,
                    'date': date_cvt,
                    'type': type,
                    'service_id': service_id.id,
                    'amount': amount,
                    'employee_ids': [(4, k) for k in emp_ids],
                    'employee1_ids': [(4, k) for k in emp1_ids],
                    'doctor_ids': [(4, x) for x in doc_ids],
                    'note': note,
                }
                lines.append(val)
                index += 1
            self.history_id = lines
            self.field_binary_import = None
            self.field_binary_name = None

        except ValueError as e:
            raise osv.except_osv("Warning!",
                                 (e))

    @api.multi
    def action_update(self):
        if self.state != 'draft':
            return True
        if self.type == 'product':
            self.import_product()
        elif self.type == 'coin':
            self.import_coin()
        elif self.type == 'money':
            self.import_money()
        else:
            self.import_service_history()
        self.state = 'updated'

    @api.multi
    def action_check(self):
        for i in self.history_id:
            if i.amount <= 0:
                raise ValidationError('Số lượng phải lớn hơn 0!')
            doc_ids = []
            emp_ids = []
            emp1_ids = []
            if i.type == 'DV':
                type = 'service'
            elif i.type == 'TDV':
                type = 'card'
            elif i.type == 'BH':
                type = 'guarantee'
            else:
                raise ValidationError('Bạn chưa chọn đúng loại dịch vụ.Vui lòng chọn lại.Xin cám ơn!')

            if type == 'card':
                for emp in i.employee_ids:
                    employee_ids = self.env['hr.employee'].search([('id', '=', emp.id)])
                    emp_ids.append(employee_ids.id)
                for doc in i.doctor_ids:
                    doctor_ids = self.env['hr.employee'].search([('id', '=', doc.id)])
                    doc_ids.append(doctor_ids.id)
                for emp1 in i.employee1_ids:
                    employee1_ids = self.env['hr.employee'].search([('id', '=', emp1.id)])
                    emp1_ids.append(employee1_ids.id)

                service_card_ids = {
                    'service_id': i.service_id.id,
                    'quantity': i.amount,
                    'employee_ids': [(4, k) for k in emp_ids],
                    'employee1_ids': [(4, y) for y in emp1_ids],
                    'doctor_ids': [(4, x) for x in doc_ids],
                    'customer_comment': i.note
                }
                res = self.env['izi.service.card.using'].create({
                    'type': type,
                    'customer_id': i.customer_id.id,
                    'redeem_date': i.date,
                    'date': i.date,
                    'date_start': i.date,
                    'date_end': i.date,
                    'service_card_ids': [(0, 0, service_card_ids)],
                    'state': 'done',
                    'pos_session_id': self.session_id.id
                })
                res.service_card_ids.write({
                    'state': 'done'
                })

            if type == 'service' or type == 'guarantee':
                for emp in i.employee_ids:
                    employee_ids = self.env['hr.employee'].search([('id', '=', emp.id)])
                    emp_ids.append(employee_ids.id)
                for doc in i.doctor_ids:
                    doctor_ids = self.env['hr.employee'].search([('id', '=', doc.id)])
                    doc_ids.append(doctor_ids.id)
                for emp1 in i.employee1_ids:
                    employee1_ids = self.env['hr.employee'].search([('id', '=', emp1.id)])
                    emp1_ids.append(employee1_ids.id)
                service_card_ids = {
                    'service_id': i.service_id.id,
                    'quantity': i.amount,
                    'employee_ids': [(4, k) for k in emp_ids],
                    'employee1_ids': [(4, y) for y in emp1_ids],
                    'doctor_ids': [(4, x) for x in doc_ids],
                    'customer_comment': i.note
                }
                res = self.env['izi.service.card.using'].create({
                    'type': type,
                    'customer_id': i.customer_id.id,
                    'redeem_date': i.date,
                    'date': i.date,
                    'date_start': i.date,
                    'date_end': i.date,
                    'service_card1_ids': [(0, 0, service_card_ids)],
                    'state': 'done',
                    'pos_session_id': self.session_id.id
                })
                res.service_card1_ids.write({
                    'state': 'done'
                })

        super(StockInventoryCustomer, self).action_check()

    @api.multi
    def action_back(self):
        self.history_id = None
        super(StockInventoryCustomer, self).action_back()
