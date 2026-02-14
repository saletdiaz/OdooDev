# from odoo import http


# class Ej02ListaTareas(http.Controller):
#     @http.route('/ej02_lista_tareas/ej02_lista_tareas', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ej02_lista_tareas/ej02_lista_tareas/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ej02_lista_tareas.listing', {
#             'root': '/ej02_lista_tareas/ej02_lista_tareas',
#             'objects': http.request.env['ej02_lista_tareas.ej02_lista_tareas'].search([]),
#         })

#     @http.route('/ej02_lista_tareas/ej02_lista_tareas/objects/<model("ej02_lista_tareas.ej02_lista_tareas"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ej02_lista_tareas.object', {
#             'object': obj
#         })

