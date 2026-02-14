from odoo import models, fields, api
from odoo.exceptions import UserError

class KarmaTicket(models.Model):
    _name = 'karma_helpdesk_ticket'
    _description = 'Gestión de incidencias con Karma'

    name = fields.Char(string="Título", required=True)
    description = fields.Text(string="Descripción del problema")
    user_id = fields.Many2one('res.users', string="Usuario que reporta", default=lambda self: self.env.user)
    tecnico_id = fields.Many2one('res.users', string="Técnico asignado")
    
    gravedad = fields.Selection([
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta')
    ], string="Gravedad", default='baja')

    state = fields.Selection([
        ('abierto', 'Abierto'),
        ('en_progreso', 'En progreso'),
        ('resuelto', 'Resuelto'),
        ('cerrado', 'Cerrado')
    ], string="Estado", default='abierto')

    def action_resolver(self):
        for record in self:
            if not record.tecnico_id:
                raise UserError("Debe asignar un técnico para resolver la incidencia.")
            
            puntos = 3 if record.gravedad == 'alta' else 1
            # Importante: Asegúrate de que el campo 'karma' existe en res.users
            record.tecnico_id.karma += puntos

            # Registro en el historial
            self.env['karma.history'].create({
                'name': f"Resolución: {record.name}",
                'user_id': record.tecnico_id.id,
                'puntos': puntos,
                'motivo': f"Ticket '{record.name}' resuelto (Gravedad: {record.gravedad})",
                'karma_ticket_id': record.id,
                'gravedad': record.gravedad
            })
            record.state = 'resuelto'

    def action_reabrir(self):
        for record in self:
            if record.state != 'resuelto':
                continue
                
            puntos_negativos = -3
            if record.tecnico_id:
                record.tecnico_id.karma += puntos_negativos
                
                self.env['karma.history'].create({
                    'name': f"Reapertura: {record.name}",
                    'user_id': record.tecnico_id.id,
                    'puntos': puntos_negativos,
                    'motivo': f"Reapertura de incidencia '{record.name}'",
                    'karma_ticket_id': record.id
                })
            record.state = 'en_progreso'