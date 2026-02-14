from odoo import models, fields
from odoo.exceptions import UserError

class KarmaHistory(models.Model):
    _name = 'karma.history'
    _description = 'Gestión de incidencias'

    name = fields.Char(string="Título") 
    description = fields.Text(string="Descripción")

    user_id = fields.Many2one('res.users', string="Usuario", default=lambda self: self.env.user)
    puntos = fields.Integer(string="Puntos")
    motivo = fields.Char(string="Motivo")
    tecnico_id = fields.Many2one('res.users', string="Técnico")
    karma_ticket_id = fields.Many2one('karma_helpdesk_ticket', string="Incidencia relacionada")

    gravedad = fields.Selection([
        ('baja', 'baja'),
        ('media', 'media'),
        ('alta', 'alta')
    ], string="Gravedad", default='baja')

    state = fields.Selection([
        ('abierto', 'Abierto'),
        ('en_progreso', 'En progreso'),
        ('resuelto', 'Resuelto'),
        ('cerrado', 'Cerrado')
    ], string="Estado", default='abierto')