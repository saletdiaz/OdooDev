# -*- coding: utf-8 -*-
from odoo.http import request
from odoo import http
import logging
import json

_logger = logging.getLogger(__name__)
# _logger.info(f"Ruta invocada con el nombre del equipo: {nombre}")

#Clase del controlador web
class Main(http.Controller):
    #Decorador que indica que la url "/ligafutbol/equipo" atendera por HTTP, sin autentificacion
    #Devolvera texto que estará en formato JSON
    #Se puede probar accediendo a http://localhost:8069/ligafutbol/equipos
    @http.route('/ligafutbol/equipos', type='http', auth='none')
    def obtenerDatosEquiposJSON(self):
        #Obtenemos la referencia al modelo de Equipo
        equipos = request.env['liga.equipo'].sudo().search([])
        
        # Generamos una lista con informacion que queremos sacar en JSON
        listaDatosEquipos=[]
        for equipo in equipos:
             listaDatosEquipos.append([
                 equipo.id, # agregado
                 equipo.nombre,
                 str(equipo.fecha_fundacion),
                 equipo.jugados,
                 equipo.puntos,
                 equipo.victorias,
                 equipo.empates,
                 equipo.derrotas
             ])

        # O podemos generar la lista con "comprehension list"
        # agregado
        listaDatosEquipos = [[
            e.id, 
            e.nombre, 
            str(e.fecha_fundacion),
            e.jugados,
            e.puntos,
            e.victorias,
            e.empates,
            e.derrotas
            ] for e in equipos]

        #Convertimos la lista generada a JSON
        json_result=json.dumps(listaDatosEquipos)
        # Agregado, devolvemos un objeto "Response HTTP" con contenido tipo JSON
        # lo he dejado en aules, debajo de "EJ06-LigaFutbol"
        return request.make_response(json_result, headers=[('Content-Type', 'application/json')])
    
    @http.route('/ligafutbol/prueba', type='http', auth='none')
    def prueba_ruta(self):
        _logger.info(f"Ruta invocada")
        return "¡Ruta funcionando!"

    @http.route('/ligafutbol/equipo/<string:nombre>', type='http', auth='none')
    def obtenerEquipoPorNombre(self, nombre):
        _logger.info(f"Ruta invocada con el nombre del equipo: {nombre}")

        # Buscar el equipo por nombre
        equipo = request.env['liga_eficiente.equipo'].sudo().search(
            [('nombre', '=', nombre)], limit=1
        )

        # Comprobar si el equipo fue encontrado
        if not equipo:
            _logger.warning(f"Equipo no encontrado con nombre: {nombre}")
            return json.dumps({'error': f'Equipo "{nombre}" no encontrado'}, ensure_ascii=False, indent=4)

        _logger.info(f"Equipo encontrado: {equipo.nombre}")

        # Datos del equipo
        equipo_data = {
            'nombre': equipo.nombre,
            'fecha_fundacion': str(equipo.fecha_fundacion),
            'jugados': equipo.jugados,
            'puntos': equipo.puntos,
            'victorias': equipo.victorias,
            'empates': equipo.empates,
            'derrotas': equipo.derrotas,
        }

        _logger.info(f"Datos del equipo: {equipo_data}")

        # Datos de partidos como local
        partidos_local = [
            {
                'id': partido.id,
                'equipo_visitante': partido.equipo_fuera.nombre,
                'goles_local': partido.goles_casa,
                'goles_visitante': partido.goles_fuera,
                'fecha': str(partido.fecha_partido),
            }
            for partido in equipo.partidos_jugados
        ]

        _logger.info(f"Partidos como local: {partidos_local}")

        # Datos de partidos como visitante
        partidos_visitante = [
            {
                'id': partido.id,
                'equipo_local': partido.equipo_casa.nombre,
                'goles_local': partido.goles_casa,
                'goles_visitante': partido.goles_fuera,
                'fecha': str(partido.fecha_partido),
            }
            for partido in equipo.partidos_visitante
        ]

        _logger.info(f"Partidos como visitante: {partidos_visitante}")

        # Construir el resultado
        resultado = {
            'equipo': equipo_data,
            'partidos_local': partidos_local,
            'partidos_visitante': partidos_visitante,
        }

        _logger.info(f"Resultado final construido: {resultado}")

        return json.dumps(resultado, ensure_ascii=False, indent=4)
