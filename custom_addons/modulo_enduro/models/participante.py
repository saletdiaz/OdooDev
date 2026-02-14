from odoo import models, fields
# Participante model

class Participante(models.Model):
    _name = 'enduro.participant'
    _description = 'Participante en la competición de Enduro'

    name = fields.Char('Nombre del participante', required=True)
    moto = fields.Char('Modelo de moto')
    categoria = fields.Selection([
        ('profesional', 'Profesional'),
        ('amateur', 'Amateur')
    ], string='Categoría')
    edad = fields.Integer('Edad')
    finalizacion = fields.Boolean('Finalizó la competición', default=False)

    # Relacion Many2one con competicion
    competicio_id = fields.Many2one('enduro.competicio', string='Competición')