# -*- coding: utf-8 -*-
"""
Script de prueba de conexión a la base de datos PostgreSQL local (uao_db)
corriendo en el servidor local de pgAdmin4.

Uso desde terminal (PowerShell / CMD / VS Code terminal):

PowerShell:
    $env:DB_USER="postgres"
    $env:DB_PASSWORD="TU_CONTRASEÑA"
    $env:DB_NAME="uao_db"
    python test_db_connection.py

CMD:
    set DB_USER=postgres
    set DB_PASSWORD=TU_CONTRASEÑA
    set DB_NAME=uao_db
    python test_db_connection.py
"""

import os

from sqlalchemy import create_engine
from sqlalchemy import text
import pandas as pd

# Connection parameters (defaults point to the local PostgreSQL server in pgAdmin4)
host = os.getenv('DB_HOST', 'localhost')
port = int(os.getenv('DB_PORT', 5432))
user = os.getenv('DB_USER', 'postgres')
password = os.getenv('DB_PASSWORD', 'postgres')
database = os.getenv('DB_NAME', 'uao_db')

engine = create_engine(
    f'postgresql://{user}:{password}@{host}:{port}/{database}'
)

with engine.connect() as conn:
    df = pd.read_sql('SELECT COUNT(*) FROM enrolled_uao', conn)
    print(df)

print('CONEXIÓN OK: PostgreSQL local (pgAdmin4) -> uao_db')
