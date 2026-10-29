# UAO Stats — Dashboard local (PostgreSQL + Dash)

**UAO Stats** es el dashboard en Python **Dash** del proyecto *Characterization and prediction of students' population: Universidad Autónoma de Occidente - case of study* (Equipo 18 / Data Science for All – Colombia 3.0).

Este repositorio ha sido adaptado para funcionar **100% en local** (`localhost`) conectado a una **base de datos PostgreSQL llamada `uao_db`** que se encuentra corriendo en un servidor local administrado con **pgAdmin4**.

---

## 📌 ¿Cómo funciona el proyecto?

```
app/index_h.py  (entry point del dashboard)
        │
        └── app/lib/ (módulos de contenido: Home, Map, Visualization, Segmentation,
                      Characterization, Prediction, Work Team)
                │   SQLAlchemy: create_engine('postgresql://user:pass@host:port/db')
                └── pandas: pd.read_sql(query, connDB)  →  DataFrames → Gráficas Dash
```

- **Framework:** Python Dash + Dash Bootstrap Components + Plotly.
- **Backend / conexión a BD:** SQLAlchemy (`create_engine`) + `pandas.read_sql`.
- **Base de datos:** PostgreSQL (`uao_db`) en servidor local (pgAdmin4).
- **Dashboard:** se ejecuta en el puerto `8050`.

---

## ✅ Requisitos previos

1. **Python 3.8 o superior** (se recomienda Python 3.8 / 3.9).
2. **pgAdmin4** + **PostgreSQL** instalados y el servidor local corriendo (por defecto en `localhost:5432`).
3. **Visual Studio Code** con las extensiones:
   - **Python** (Microsoft) — para el intérprete y el terminal.
   - **PostgreSQL** (Microsoft) — opcional, para navegar consultas desde VS Code.
4. `pip` / `python -m pip`.

---

## 🚀 Pasos para que el proyecto funcione localmente

### Paso 1 — Levantar el servidor PostgreSQL local (pgAdmin4)

1. Abre **pgAdmin4**.
2. En la sección *Servers*, inicia el servidor **PostgreSQL** (botón *Start*). El estado debe quedar en **Running**.
3. El servidor local por defecto escucha en `localhost` y puerto `5432`.

### Paso 2 — Preparar la base de datos `uao_db`

1. En pgAdmin4: *Database* → *Create* → **Database name**: `uao_db`.
2. Si ya la tienes creada, este paso se omite.
3. El dashboard requiere las tablas: `enrolled_uao`, `registered_uao`, `deserters_uao`, `cities` y `rules` dentro de `uao_db`.

### Paso 3 — Configurar la conexión a la base de datos (`localhost`)

Los módulos de `app/lib/` construyen el motor SQLAlchemy así:

```python
host = os.getenv('DB_HOST', 'localhost')                   # Local instance (pgAdmin4)
port = int(os.getenv('DB_PORT', 5432))                   # default port
user = os.getenv('DB_USER', 'postgres')                 # database user
password = os.getenv('DB_PASSWORD', 'postgres')         # database password
database = os.getenv('DB_NAME', 'uao_db')               # database name
connDB = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}') #database connection (only once)
```

- **Por defecto** el proyecto apunta a: `localhost:5432`, base `uao_db`, usuario `postgres`, contraseña `postgres`.
- Si tu PostgreSQL local usa otro usuario / contraseña, define las variables de entorno correspondientes (`DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DB_NAME`).

### Paso 4 — Instalar las dependencias de Python

Desde la terminal (PowerShell / CMD / VS Code terminal):

```bash
cd C:\Users\x360\Desktop\uao_stats\app
python -m pip install -r requirements.txt
```

`requirements.txt` contiene el stack instalado y verificado para que el dashboard funcione en local (Python 3.15): Dash 2.18, Plotly 5.24, SQLAlchemy 2.x, psycopg, Flask/Werkzeug modernos, pandas, scikit-learn, folium, numpy, etc.

### Paso 5 — Ejecutar el dashboard

```bash
cd C:\Users\x360\Desktop\uao_stats\app
python index_h.py
```

- El servidor se levanta en `host="0.0.0.0"`, `port="8050"`, `debug=True`.
- Abre tu navegador en: **http://localhost:8050**

---

## 🔌 Cómo conectarse desde Visual Studio Code al PostgreSQL local (pgAdmin4)

**pgAdmin4** es la herramienta gráfica que administras tu servidor PostgreSQL local. El dashboard y Visual Studio Code se conectan al **mismo servidor PostgreSQL** que está corriendo en `localhost:5432`.

### Opción A — Conexión / prueba desde VS Code con Python (recomendada para el proyecto)

1. Abre la carpeta del proyecto en VS Code: `File → Open Folder` → `C:\Users\x360\Desktop\uao_stats`.
2. Instala las extensiones recomendadas:
   - **Python** (Microsoft) → para intérprete y terminal.
   - **PostgreSQL** (Microsoft) → opcional, para explorar la BD desde la UI de VS Code.
3. Selecciona el intérprete de Python: `Ctrl+Shift+P` → **Python: Select Interpreter** → elige el entorno venv o el intérprete global.
4. Abre la terminal integrada de VS Code (`Ctrl+` `) y ejecuta:

```bash
cd C:\Users\x360\Desktop\uao_stats\app
python -m pip install -r requirements.txt
```

5. Define las variables de entorno de la base de datos en la terminal de VS Code y prueba la conexión:

**PowerShell:**
```bash
$env:DB_USER="postgres"
$env:DB_PASSWORD="TU_CONTRASEÑA"
$env:DB_NAME="uao_db"
python -c "import os; from sqlalchemy import create_engine; import pandas as pd; e=create_engine(f\"postgresql://{os.getenv('DB_USER','postgres')}:{os.getenv('DB_PASSWORD','postgres')}@{os.getenv('DB_HOST','localhost')}:{os.getenv('DB_PORT',5432)}/{os.getenv('DB_NAME','uao_db')}\"); print(pd.read_sql('SELECT COUNT(*) FROM enrolled_uao', e)); print('CONEXIÓN OK')"
```

**CMD:**
```bash
set DB_USER=postgres
set DB_PASSWORD=TU_CONTRASEÑA
set DB_NAME=uao_db
python index_h.py
```

6. O bien crea un script de prueba, por ejemplo `test_db_connection.py` en la raíz del proyecto:

```python
import os
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine(
    f"postgresql://{os.getenv('DB_USER', 'postgres')}:{os.getenv('DB_PASSWORD', 'postgres')}"
    f"@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', 5432)}/{os.getenv('DB_NAME', 'uao_db')}"
)

with engine.connect() as conn:
    df = pd.read_sql("SELECT COUNT(*) FROM enrolled_uao", conn)
    print(df)
```

7. Ejecuta el script desde la terminal de VS Code: `python test_db_connection.py` → debe imprimir el DataFrame sin errores.

### Opción B — Conexión desde VS Code usando la extensión **PostgreSQL**

1. En VS Code, instala la extensión **PostgreSQL** (Microsoft).
2. Abre la Command Palette (`Ctrl+Shift+P`) → **PostgreSQL: Connect** (o *Connect to Server*).
3. Ingresa los datos del servidor local:
   - **Host:** `localhost`
   - **Port:** `5432`
   - **Database:** `uao_db`
   - **User:** tu usuario de PostgreSQL
   - **Password:** tu contraseña
4. Conecta. Ahora podrás ver los esquemas/tabs de la base de datos y ejecutar queries desde la UI de VS Code.

### Conexión final del dashboard

Cuando el dashboard (`python index_h.py`) se ejecuta desde VS Code (o desde cualquier terminal), internamente usa:

```python
create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')
```

es decir: `postgresql://usuario:contraseña@localhost:5432/uao_db`, y esto es **exactamente** el mismo servidor que pgAdmin4 está administrando localmente.

---

## 📁 Estructura del proyecto

```
C:\Users\x360\Desktop\uao_stats\
├── app/
│   ├── app.py                  # Definición del Dash app
│   ├── index_h.py              # Entry point local (debug, puerto 8050)
│   ├── index_h_ec2.py          # Entry point para AWS EC2
│   ├── requirements.txt        # Dependencias
│   ├── lib/                    # Módulos de contenido / callbacks
│   ├── assets/                 # Imágenes, CSS, HTML (mapa, logos, etc.)
│   └── data/                   # CSVs, modelos, archivos de datos auxiliares
├── README.md
├── LICENSE
└── Team18_Folio.pdf
```

---

## 🌐 Puertos y URLs

| Servicio | Valor |
|---|---|
| Dashboard (local) | `http://localhost:8050` |
| PostgreSQL (local / pgAdmin4) | `localhost:5432` |
| Base de datos | `uao_db` |

---

## 🧯 Solución de problemas

- **Error de conexión a PostgreSQL** (`could not connect`, `Connection refused`): el servidor PostgreSQL no está corriendo → iniciar en pgAdmin4 (*Servers* → *PostgreSQL* → *Start*) o iniciar el servicio de PostgreSQL.
- **Error de base de datos** (`database "uao_db" does not exist`): crear la base `uao_db` en pgAdmin4.
- **Error de tabla**: crear las tablas requeridas (`enrolled_uao`, `registered_uao`, `deserters_uao`, `cities`, `rules`).
- **Error con el driver / SQLAlchemy**: instalar dependencias con `python -m pip install -r app/requirements.txt`.
- **Error con Dash**: usar las versiones del `app/requirements.txt` (Dash 2.18 / Plotly 5.24), ya que el dashboard usa la API de Dash instalada allí.

---

## 🔗 Links del proyecto original

- GitHub: https://github.com/felipeescallon/Data-Science-Project
- App publicada (AWS EC2): http://18.217.133.231:8050/

---

*Fin de la guía local.*
