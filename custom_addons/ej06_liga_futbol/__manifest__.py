# -*- coding: utf-8 -*-
{
    'name': "EJ06-LigaFutbol",
    'summary': "Gestionar una liga de futbol",
    'description': """
                        Gestor de Liga de futbol
                        ==============
                   """,  
    'application': True,
    'author': "Tu mismo ;)",
    'website': "",
    'category': 'Tools',
    'version': '0.1',
    'depends': ['base'],
    'data': [
        'security/groups.xml', 
        'security/ir.model.access.csv',
        'views/liga_equipo.xml',
        'views/liga_equipo_clasificacion.xml',
        #Vista a un informe
        'report/liga_equipo_clasificacion_report.xml',
        #Aqui vista sobre los partidos
        'views/liga_partido.xml',
        #Añadimos un Wizard para introducir equipos
        # 'wizard/liga_equipo_wizard.xml'      
    ],    
}
