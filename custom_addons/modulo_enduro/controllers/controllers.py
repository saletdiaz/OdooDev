# from odoo import http


# class ModuloEnduro(http.Controller):
#     @http.route('/modulo_enduro/modulo_enduro', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/modulo_enduro/modulo_enduro/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('modulo_enduro.listing', {
#             'root': '/modulo_enduro/modulo_enduro',
#             'objects': http.request.env['modulo_enduro.modulo_enduro'].search([]),
#         })

#     @http.route('/modulo_enduro/modulo_enduro/objects/<model("modulo_enduro.modulo_enduro"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('modulo_enduro.object', {
#             'object': obj
#         })

