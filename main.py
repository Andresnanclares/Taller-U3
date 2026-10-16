import os
from pathlib import Path

from dotenv import load_dotenv
from faker import Faker
from sqlalchemy import Column, Date, Integer, String, create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

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

TOTAL_REGISTROS = 100_000

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


def crear_base_y_tabla():
    engine_root = create_engine(BASE_URL, pool_pre_ping=True, future=True)
    with engine_root.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"))

    # Borra la tabla para reiniciar los datos cada vez que se ejecuta el script.
    engine = create_engine(DATABASE_URL, pool_pre_ping=True, future=True)
    with engine.connect() as conn:
        conn.execute(text(f"DROP TABLE IF EXISTS `{TABLA}`;"))

    Base.metadata.create_all(bind=engine)
    return engine


def crear_persona(fake):
    return Persona(
        nombre=fake.first_name(),
        apellido=fake.last_name(),
        correo=fake.unique.email(),
        fecha_nacimiento=fake.date_of_birth(minimum_age=18, maximum_age=80),
        ciudad=fake.city(),
        direccion=fake.address(),
        telefono=fake.phone_number(),
        empresa=fake.company(),
        profesion=fake.job(),
    )


def main():
    fake = Faker("es_ES")
    engine = crear_base_y_tabla()
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        for inicio in range(0, TOTAL_REGISTROS, 1000):
            lote = []
            for _ in range(min(1000, TOTAL_REGISTROS - inicio)):
                lote.append(crear_persona(fake))
            session.add_all(lote)
            session.commit()
            print(f"Lote insertado: {inicio + len(lote)} / {TOTAL_REGISTROS}")
    finally:
        session.close()

    print(f"Se insertaron {TOTAL_REGISTROS} registros en la tabla {TABLA}.")


if __name__ == "__main__":
    main()
