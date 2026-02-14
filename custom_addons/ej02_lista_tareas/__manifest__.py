# -*- coding: utf-8 -*-
{
    'name': "Lista de tareas",
    'summary': """Gestión de notas de alumnos""",
    'description': """ Wow, una lista de alumnos y las notas de sus exámenes.
                   """,
    'author': "",
    'website': "",
    'application': True,
    'category': 'Productivity',
    'version': '0.1',
    'depends': ['base'],
    'data': [
        # El primer fichero indica la politica de acceso del modelo
        # siempre tiene este nombre
        'security/ir.model.access.csv',

        # Cargamos las vistas y las plantillas
        'views/views.xml',
    ],
}
