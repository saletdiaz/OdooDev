# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)

class LigaEficientePartido(models.Model):
    # Nombre y descripcion del modelo
    _name = 'liga_eficiente.partido'
    _description = 'Un partido de la liga'
    _rec_name = 'equipo_casa'
    
    #Atributos del modelo
    fecha_partido = fields.Datetime(string="Fecha del Partido")
    ubicacion = fields.Char(string="Ubicación")
    notas = fields.Html(string="Notas")
    
    # Nombre del equipo que juega en casa
    equipo_casa = fields.Many2one(
        'liga_eficiente.equipo',
        string='Equipo local',
    )
    # Goles equipo de casa
    goles_casa= fields.Integer()

    # Nombre del equipo que juega fuera
    equipo_fuera = fields.Many2one(
        'liga_eficiente.equipo',
        string='Equipo visitante',
    )
    # Goles equipo de casa
    goles_fuera= fields.Integer()
    
    # Constraints de atributos
    @api.constrains('equipo_casa')
    def _check_mismo_equipo_casa(self):
        for record in self:
            if not record.equipo_casa:
                raise models.ValidationError('Debe seleccionarse un equipo local.')
            if record.equipo_casa == record.equipo_fuera:
                raise models.ValidationError('Los equipos del partido deben ser diferentes.')


    # Constraints de atributos
    @api.constrains('equipo_fuera')
    def _check_mismo_equipo_fuera(self):
        for record in self:
            if not record.equipo_fuera:
                raise models.ValidationError('Debe seleccionarse un equipo visitante.')
            if record.equipo_fuera and record.equipo_casa == record.equipo_fuera:
                raise models.ValidationError('Los equipos del partido deben ser diferentes.')

    # Funcion para actualizar la clasificacion de manera más eficiente, sin recalcular todo
    def actualizar_estadisticas(self, partido, eliminar=False):
        factor = -1 if eliminar else 1

        equipo_casa = partido.equipo_casa
        equipo_fuera = partido.equipo_fuera

        # Actualizar estadísticas del equipo local
        if equipo_casa:
            equipo_casa.goles_a_favor += factor * partido.goles_casa
            equipo_casa.goles_en_contra += factor * partido.goles_fuera

            if partido.goles_casa > partido.goles_fuera:
                equipo_casa.victorias += factor
            elif partido.goles_casa < partido.goles_fuera:
                equipo_casa.derrotas += factor
            else:
                equipo_casa.empates += factor

        # Actualizar estadísticas del equipo visitante
        if equipo_fuera:
            equipo_fuera.goles_a_favor += factor * partido.goles_fuera
            equipo_fuera.goles_en_contra += factor * partido.goles_casa

            if partido.goles_fuera > partido.goles_casa:
                equipo_fuera.victorias += factor
            elif partido.goles_fuera < partido.goles_casa:
                equipo_fuera.derrotas += factor
            else:
                equipo_fuera.empates += factor


    @api.model
    def create(self, values):
        record = super(LigaEficientePartido, self).create(values)
        self.actualizar_estadisticas(record)
        return record
    
    def write(self, values):
        for record in self:
            # Restar estadísticas actuales
            self.actualizar_estadisticas(record, eliminar=True)

        result = super(LigaEficientePartido, self).write(values)

        for record in self:
            # Sumar estadísticas nuevas
            self.actualizar_estadisticas(record)
        return result
    
    # Actualización temporal
    @api.onchange('equipo_casa', 'goles_casa', 'equipo_fuera', 'goles_fuera')
    def actualizar(self):
        if self.equipo_casa and self.equipo_fuera:
            self.actualizar_estadisticas(self)


    #Sobrescribo el borrado (unlink)
    def unlink(self):
        for record in self:
            self.actualizar_estadisticas(record, eliminar=True)
        return super(LigaEficientePartido, self).unlink()

    escudo_casa = fields.Image(related='equipo_casa.escudo', string="Escudo Local", readonly=True)
    escudo_fuera = fields.Image(related='equipo_fuera.escudo', string="Escudo Visitante", readonly=True)
