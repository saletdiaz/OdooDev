# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)

# Definimos modelo liga_eficiente_equipo, que almacenara información de cada equipo
class LigaEficienteEquipo(models.Model):
    # Nombre y descripcion del modelo
    _name = 'liga_eficiente.equipo'
    _description = 'Equipo de la liga'

    # Parametros de ordenacion por defecto
    _order = 'nombre'

    # ATRIBUTOS
    # Indicamos que atributo sera el que se usara para mostrar nombre.
    # Por defecto es "name", pero si no hay un atributo que se llama name, aqui lo indicamos
    _rec_name = 'nombre'

    # Atributo nombre
    nombre = fields.Char('Nombre equipo', required=True, index=True)
    # Dato binario, para guardar un binario (en la vista indicaremos que es una imagen) 
    escudo = fields.Image('Escudo equipo',max_width=50,max_height=50)

    # Año de fundacion
    fecha_fundacion = fields.Date('Fecha fundación')
    # Campo con HTML (Sanitizado) donde se guarda la descripción del comic
    descripcion = fields.Html('Descripción', sanitize=True, strip_style=False)
 
    #Partidos jugados, ganados, empatados, perdidos
    victorias=fields.Integer(default=0)
    empates=fields.Integer(default=0)
    derrotas=fields.Integer(default=0)
    
    jugados= fields.Integer( compute="_compute_jugados", store=True)
    @api.depends('victorias','empates','derrotas')
    def _compute_jugados(self):
        for record in self:
            record.jugados = record.victorias + record.empates + record.derrotas
    
    puntos= fields.Integer( compute="_compute_puntos",default=0, store=True)
    @api.depends('victorias','empates')
    def _compute_puntos(self):
        for record in self:
            record.puntos = record.victorias * 3 + record.empates
    
    #Goles a favor y en contra
    goles_a_favor=fields.Integer()
    goles_en_contra=fields.Integer()

    #Constraints de SQL del modelo
    _sql_constraints = [
        ('name_uniq', 'UNIQUE (nombre)', 'El nombre del equipo.')
    ]

    #Constraints de atributos
    @api.constrains('fecha_fundacion')
    def _check_release_date(self):
        for record in self:
            if record.fecha_fundacion and record.fecha_fundacion > fields.Date.today():
                raise models.ValidationError('La fecha de fundación del club debe ser anterior a la actual')
            
    # Para mostrar los partidos desde la ficha de Equipo
    partidos_jugados = fields.One2many(
        'liga_eficiente.partido',  # Relación al modelo de partidos
        'equipo_casa',  # Campo `Many2one` en el modelo `liga_eficiente.partido`
        string='Partidos como equipo local'
    )

    partidos_visitante = fields.One2many(
        'liga_eficiente.partido',
        'equipo_fuera',
        string='Partidos como equipo visitante'
    )

    def write(self, vals):
        if 'partidos_jugados' in vals or 'partidos_visitante' in vals:
            for record in self:
                for partido in record.partidos_jugados | record.partidos_visitante:
                    partido.actualizar_estadisticas(partido)
        return super(LigaEficienteEquipo, self).write(vals)
    
    @api.onchange('partidos_jugados', 'partidos_visitante')
    def _onchange_partidos(self):
        _logger.info(f"Recalculando estadísticas para equipo: {self.nombre}")
        for partido in self.partidos_jugados:
            _logger.info(f"Procesando partido local: {partido.id} - {partido.equipo_casa.nombre} vs {partido.equipo_fuera.nombre}")
        for partido in self.partidos_visitante:
            _logger.info(f"Procesando partido visitante: {partido.id} - {partido.equipo_casa.nombre} vs {partido.equipo_fuera.nombre}")