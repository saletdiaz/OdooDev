{
    'name': 'Karma HelpDesk',
    'version': '1.0',
    'category': 'Services/Helpdesk',
    'summary': 'Gestión de incidencias con sistema de gamificación (Karma)',
    'description': """
        Módulo para la gestión de incidencias técnicas.
        Incluye:
        - Sistema de karma positivo/negativo.
        - Niveles de reputación para técnicos y usuarios.
        - Historial de acciones.
    """,
    'author': 'Salet Diaz',
    'depends': ['base', 'mail'], 
    'data': [
        'security/ir.model.access.csv', 
        'views/views.xml',       
    ],
    'demo': [
        'data/demo_data.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}