from odoo import http 
from odoo.http import request

class KarmaHelpdeskAPI(http.Controller):

    # 1. Incidencias asociadas a un usuario
    @http.route('/api/usuarios/<int:user_id>/incidencias', auth='user', type='json', methods=['GET'])
    def get_user_incidences(self, user_id, **kwargs):
        if request.env.user.id != user_id and not request.env.user._is_admin():
            return {'status': 'error', 'message': 'No tienes permiso.'}

        karma = request.env['karma_helpdesk_ticket'].search([('user_id', '=', user_id)])

        incidences_data = []
        for incidence in karma: 
            puntos = 3 if incidence.gravedad == 'alta' else 1
            incidences_data.append({
                'id': incidence.id,
                'asunto': incidence.name,
                'estado': incidence.state,
                'gravedad': incidence.gravedad,
                'impacto_karma': puntos,
                'karma_usuario': puntos if incidence.state == 'resuelto' else 0,
                'tecnico': incidence.tecnico_id.name if incidence.tecnico_id else "No asignado",
            })

        return {
            'status': 'success',
            'total_incidences': len(incidences_data),
            'data': incidences_data
        }

    # 2. Estado y rendimiento del técnico (¡CORREGIDO!)
    @http.route('/api/tecnicos/<int:tecnico_id>/estado', auth='user', type='json', methods=['GET'])
    def get_tecnico_status(self, tecnico_id, **kwargs):
        tecnico = request.env['res.users'].browse(tecnico_id)

        if not tecnico.exists():
            return {'status': 'error', 'message': 'Técnico no encontrado.'}
        
        incidencias_resueltas = request.env['karma_helpdesk_ticket'].search_count([
            ('tecnico_id', '=', tecnico_id), 
            ('state', '=', 'resuelto')
        ])

        incidencias_totales = request.env['karma_helpdesk_ticket'].search_count([
            ('tecnico_id', '=', tecnico_id)
        ])

        rendimiento = (incidencias_resueltas / incidencias_totales * 100) if incidencias_totales > 0 else 0

        return {
            'status': 'success',
            'data': {
                'id': tecnico.id,
                'nombre': tecnico.name,
                'karma_acumulado': tecnico.karma,
                'rango': tecnico.nivel_reputacion, 
                'metricas': {
                    'incidencias_resueltas': incidencias_resueltas,
                    'incidencias_totales': incidencias_totales,
                    'rendimiento': f"{rendimiento:.2f}%"
                },
                'impacto_funcional': f"El técnico {tecnico.name} ha resuelto {incidencias_resueltas} de {incidencias_totales} incidencias."
            }
        }

    # 3. Resumen global del sistema
    @http.route('/api/sistema/resumen', auth='user', type='json', methods=['GET'])
    def get_sistema_resumen(self, **kwargs):
        TModel = request.env['karma_helpdesk_ticket']
        
        return {
            'status': 'success',
            'data': {
                'total': TModel.search_count([]),
                'abiertos': TModel.search_count([('state', '=', 'abierto')]),
                'en_progreso': TModel.search_count([('state', '=', 'en_progreso')]),
                'resueltos': TModel.search_count([('state', '=', 'resuelto')])
            }
        }