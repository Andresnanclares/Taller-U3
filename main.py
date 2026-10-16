import os

from dotenv import load_dotenv
from sqlalchemy import Column, Date, Integer, String, create_engine, text
from sqlalchemy.orm import declarative_base

load_dotenv()

Base = declarative_base()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
TABLA = os.getenv("DB_TABLE_NAME")

BASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/"
DATABASE_URL = f"{BASE_URL}{DB_NAME}"

class Persona(Base):
    __tablename__ = TABLA

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    correo = Column(String(255), unique=True, nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    ciudad = Column(String(100), nullable=False)
    direccion = Column(String(255), nullable=False)
    telefono = Column(String(30), nullable=False)
    empresa = Column(String(150), nullable=False)
    profesion = Column(String(100), nullable=False)


def crear_base():
    engine_root = create_engine(BASE_URL, pool_pre_ping=True, future=True)
    with engine_root.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"))

    engine = create_engine(DATABASE_URL, pool_pre_ping=True, future=True)

    Base.metadata.create_all(bind=engine)
    return engine



def main():
    crear_base()


if __name__ == "__main__":
    main()
