# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request, Response
import json


#Clase del controlador web
class Main(http.Controller):
    #Decorador que indica que la url "/ligafutbol/equipo/json" atendera por HTTP, sin autentificacion
    #Devolvera texto que estará en formato JSON
    #Se puede probar accediendo a http://localhost:8069/ligafutbol/equipo/json
    @http.route('/ligafutbol/equipos', type='http', auth='none')
    def obtenerDatosEquiposJSON(self):
        #Obtenemos la referencia al modelo de Equipo
        equipos = request.env['liga.equipo'].sudo().search([])
        
        #Generamos una lista con informacion que queremos sacar en JSON
        listaDatosEquipos=[]
        for equipo in equipos:
             listaDatosEquipos.append([
                 equipo.id,
                 equipo.nombre,
                 str(equipo.fecha_fundacion),
                 equipo.jugados,
                 equipo.puntos,
                 equipo.victorias,
                 equipo.empates,
                 equipo.derrotas
             ])
        #Convertimos la lista generada a JSON
        json_result=json.dumps(listaDatosEquipos)

        return json_result
    
    @http.route('/ligafutbol/equipo-goles', type='http', auth='none')
    def obtenerDatosEquiposGolesJSON(self, goles=None):
        # Si se proporciona el parámetro 'goles', lo usamos para filtrar
        if goles is not None:
            try:
                goles = int(goles)
                partidos = request.env['liga.partido'].sudo().search([('goles_casa', '>=', goles)])
                equipos_ids = partidos.mapped('equipo_casa').ids
            except ValueError:
                return "Parámetro 'goles' inválido", 400
        else:
            equipos_ids = request.env['liga.equipo'].sudo().search([]).ids
        equipos = request.env['liga.equipo'].sudo().browse(equipos_ids)
        listaDatosEquipos = [[equipo.nombre, equipo.goles_a_favor, equipo.goles_en_contra] for equipo in equipos]
        json_result = json.dumps(listaDatosEquipos)
        return Response(json_result, mimetype='application/json')
    
    @http.route(['/ligafutbol/equipo/<string:nombre_equipo>/partidos'], type='http', auth='public', methods=['GET'])
    def obtenerPartidosEquipoJSON(self, nombre_equipo):
        # Buscamos el equipo por nombre
        equipo = request.env['liga.equipo'].sudo().search([('nombre', 'ilike', '%' + nombre_equipo + '%')], limit=1)
        
        # Verificamos si encontramos el equipo
        if not equipo:
            error_message = json.dumps({'error': 'Equipo no encontrado'})
            return Response(error_message, status=404, mimetype='application/json')

        # Obtenemos los partidos donde el equipo es local o visitante
        partidos = request.env['liga.partido'].sudo().search(['|', ('equipo_casa', '=', equipo.id), ('equipo_fuera', '=', equipo.id)])
        
        # Preparamos la lista de partidos
        listaPartidos = []
        for partido in partidos:
            listaPartidos.append({
                'equipo_local': partido.equipo_casa.nombre if partido.equipo_casa else "Desconocido",
                'goles_local': partido.goles_casa,
                'equipo_visitante': partido.equipo_fuera.nombre if partido.equipo_fuera else "Desconocido",
                'goles_visitante': partido.goles_fuera,
            })

        # Convertimos la lista a JSON y la devolvemos
        json_result = json.dumps(listaPartidos)
        return Response(json_result, mimetype='application/json')