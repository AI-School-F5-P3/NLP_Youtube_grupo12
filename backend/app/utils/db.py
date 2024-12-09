# app/utils/db.py

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener la URL de la base de datos desde las variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL no está configurada en el archivo .env")

# Crear el motor asincrónico para la base de datos
async_engine = create_async_engine(
    DATABASE_URL,
    future=True,
    echo=False  # Cambiar a False en producción para reducir ruido en los logs
)

# Declarar la base para definir modelos de SQLAlchemy
Base = declarative_base()

# Configuración de la sesión asincrónica
async_session = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Función para obtener la sesión de la base de datos
async def get_db():
    """
    Generador de sesiones asincrónicas de la base de datos.
    """
    async with async_session() as session:
        yield session

# Función para inicializar la base de datos
async def init_db():
    """
    Inicializa la base de datos creando todas las tablas definidas en los modelos.
    """
    async with async_engine.begin() as conn:
        # Crear las tablas si no existen
        await conn.run_sync(Base.metadata.create_all)
