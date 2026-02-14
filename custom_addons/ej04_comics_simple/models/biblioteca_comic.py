# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

# Modelo abstracto BaseArchive como base para otros modelos.
# Sirve para implementar funcionalidades comunes que pueden ser heredadas.
class BaseArchive(models.AbstractModel):
    _name = 'base.archive'
    _description = 'Fichero abstracto'

    # Campo booleano 'activo' para marcar registros como activos o inactivos.
    activo = fields.Boolean(default=True)

    # Método 'archivar' para alternar el estado de 'activo'.
    def archivar(self):
        for record in self:
            record.activo = not record.activo

# Modelo BibliotecaComic que hereda de BaseArchive.
# Este modelo representa un comic en una biblioteca.
class BibliotecaComic(models.Model):
    _name = 'biblioteca.comic'
    _inherit = ['base.archive'] # Este atributo indica que BibliotecaComic hereda del modelo base.archive.
    _description = 'Comic de biblioteca'
    _order = 'fecha_publicacion desc, nombre'
    _rec_name = 'nombre'

    # Campos del modelo con sus descripciones y configuraciones.
    nombre = fields.Char('Titulo', required=True, index=True)
    estado = fields.Selection(
        [('borrador', 'No disponible'),
         ('disponible', 'Disponible'),
         ('perdido', 'Perdido')],
        'Estado', default="borrador")
    descripcion = fields.Html('Descripción', sanitize=True, strip_style=False)
    portada = fields.Binary('Portada Comic')
    fecha_publicacion = fields.Date('Fecha publicación')
    precio = fields.Float('Precio')
    paginas = fields.Integer('Numero de páginas', groups='base.group_user',
                             estados={'perdido': [('readonly', True)]},
                             help='Total numero de paginas', company_dependent=False)
    valoracion_lector = fields.Float('Valoración media lectores', digits=(14, 4))
    autor_ids = fields.Many2many('res.partner', string='Autores')

    # Restricciones de SQL para garantizar unicidad y validación de datos.
    _sql_constraints = [
        ('name_uniq', 'UNIQUE (nombre)', 'El titulo Comic debe ser único.'),
        ('positive_page', 'CHECK(paginas>0)', 'El comic debe tener al menos una página.')
    ]

    # Restricción en Python para asegurar que la fecha de publicación no sea futura.
    @api.constrains('fecha_publicacion')
    def _check_release_date(self):
        for record in self:
            if record.fecha_publicacion and record.fecha_publicacion > fields.Date.today():
                raise models.ValidationError('La fecha de lanzamiento debe ser anterior a la actual')
            
    @api.constrains('paginas')
    def _check_paginas(self):
        for record in self:
            if record.paginas <= 0:
                raise ValidationError("El cómic debe tener al menos una página.")