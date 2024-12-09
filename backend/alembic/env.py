# alembic/env.py

from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from sqlalchemy.engine import URL
from alembic import context
import os
import sys

# Agregar el directorio raíz del proyecto al path de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Cargar variables de entorno
from dotenv import load_dotenv
load_dotenv()

# Leer la URL de la base de datos
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL no está configurada en .env")

# Convertir la URL de la base de datos a su versión síncrona para Alembic
SYNC_DATABASE_URL = DATABASE_URL.replace("+asyncpg", "")

# Configuración de Alembic
config = context.config
config.set_main_option("sqlalchemy.url", SYNC_DATABASE_URL)

# Configuración del logger
if config.config_file_name:
    fileConfig(config.config_file_name)

# Importar modelos para que Alembic detecte las tablas
from app.utils.db import Base
# Importa todos tus modelos aquí
from app.models.comment import Comment
from app.models.prediccion import Prediccion
from app.models.video_model import Video

# Metadata de las tablas
target_metadata = Base.metadata

def run_migrations_offline():
    """Ejecutar migraciones en modo offline."""
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Ejecutar migraciones en modo online."""
    connectable = create_engine(
        config.get_main_option("sqlalchemy.url"),
        poolclass=pool.NullPool,
    )
    
    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )
        
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()