# -*- coding: utf-8 -*-
{
    'name': "Biblioteca Comics Simple",  # Titulo del módulo
    'summary': "Gestionar comics",  # Resumen de la funcionaliadad
    'description': """
                    Gestor de bibliotecas (Version Simple)
                    ==============
                    """,  
    'application': True,
    'author': "",
    'website': "",
    'category': 'Tools',
    'version': '0.1',
    'depends': ['base'],
    'data': [
        # Estos dos primeros ficheros:
        #  1) El primero indica grupo de seguridad basado en rol
        #  2) El segundo indica la politica de acceso del modelo
        # Mas información en https://www.odoo.com/documentation/17.0/es/developer/tutorials/getting_started/05_securityintro.html
        'security/groups.xml',
        'security/ir.model.access.csv',
        # Cargamos la vista de la biblioteca de comics
        'views/biblioteca_comic.xml'
    ],
}
