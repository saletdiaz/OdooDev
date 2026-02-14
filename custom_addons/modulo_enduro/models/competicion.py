from odoo import models, fields

# Definiremos aquí el modelo de Competición para el módulo de Enduro en Odoo.

class Competicion(models.Model):
    _name = 'enduro.competicio'
    _description = 'Competición de Enduro'

    name = fields.Char('Nombre de la competición', required=True)
    fecha = fields.Date('Fecha de inicio')
    terreno = fields.Selection([
        ('montaña', 'Montaña'),
        ('bosque', 'Bosque'),
        ('rambla', 'Rambla'),
        ('mixto', 'Mixto')
    ], string='Tipo de terreno')
    max_participantes = fields.Integer('Número máximo de participantes', default=100)
    description = fields.Text('Descripción de la competición')

    # Relacion One2many con participantes
    participant_ids = fields.One2many('enduro.participant', 'competicio_id', string='Participantes')
