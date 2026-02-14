# -*- coding: utf-8 -*-
{
    'name': "EJ06-LigaFutbolEficiente",
    'summary': "Gestionar una liga de futbol",
    'description': """
                        Gestor de Liga de futbol + Eficiente
                        ==============
                   """,  
    'application': True,
    'author': "Tu mismo ;)",
    'website': "",
    'category': 'Tools',
    'version': '0.1',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/liga_equipo.xml',
        'views/liga_equipo_clasificacion.xml',
        'views/liga_partido.xml',     
    ],
}
