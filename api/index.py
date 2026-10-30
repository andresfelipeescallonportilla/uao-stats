import os
import sys

# Asegurar que el directorio raiz del proyecto esta en el path para poder importar la app Dash
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.app import app as dash_flask_app  # Dash instance

# WSGI app para Vercel (serverless): la app Flask subyacente de Dash
flask_app = dash_flask_app.server

# Exportar la aplicacion WSGI para el runtime de Vercel (@vercel/python)
application = flask_app
