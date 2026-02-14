# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ListaTareas(models.Model):
    # Define el nombre y la descripción del modelo de datos para la lista de tareas.
    _name = 'ej02.lista.tareas'
    _description = 'Lista de tareas''Modelo para gestionar una lista de tareas'

    # El atributo _rec_name se usa para especificar qué campo se debe utilizar para mostrar
    # el nombre del registro en la interfaz. Aquí, se utiliza el campo 'tarea'.
    _rec_name = "tarea"

    # Definición de los campos del modelo.
    # Tipos de campos: https://www.odoo.com/documentation/18.0/developer/reference/backend/orm.html#fields
    # 'tarea' es un campo de texto para describir la tarea.
    # 'prioridad' es un campo numérico que representa la prioridad de la tarea.
    # 'urgente' es un campo booleano calculado, que indica si la tarea es urgente o no.
    # 'realizada' es un campo booleano que indica si la tarea ha sido completada.
    
    tarea = fields.Char(string="Descripción de la Tarea")
    prioridad = fields.Integer(string="Prioridad de la Tarea")
    urgente = fields.Boolean(string="¿Es Urgente?", compute="_value_urgente", store=True)
    realizada = fields.Boolean(string="¿Está Realizada?")

    @api.depends('prioridad')
    def _value_urgente(self):
        # La función _value_urgente calcula si una tarea es urgente basándose en su prioridad.
        # Una tarea se considera urgente si su prioridad es mayor que 10.
        print("IDS:", self.ids)
        for record in self:
            print(
                "ID:", record.id,
                "PRIORIDAD:", record.prioridad,
                "URGENTE:", record.prioridad > 10
            )
        record.urgente = record.prioridad > 10