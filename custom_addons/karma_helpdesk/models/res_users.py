from odoo import models, fields, api 

class ResUsers(models.Model):
    _inherit = 'res.users' 

    karma = fields.Integer(string="Karma", default=0)
    nivel_reputacion = fields.Char(string="Nivel de reputación", compute="_compute_nivel_reputacion")

    @api.depends('karma')
    def _compute_nivel_reputacion(self):
        for user in self:
            if user.karma < 0:
                user.nivel_reputacion = 'Malo'
            elif user.karma < 10:
                user.nivel_reputacion = 'Regular'
            elif user.karma < 20:
                user.nivel_reputacion = 'Bueno'
            else:
                user.nivel_reputacion = 'Excelente'