# from odoo import models, fields, api


# class modulo_enduro(models.Model):
#     _name = 'modulo_enduro.modulo_enduro'
#     _description = 'modulo_enduro.modulo_enduro'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

