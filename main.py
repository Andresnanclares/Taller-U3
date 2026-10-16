import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base

load_dotenv()

Base = declarative_base()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

BASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/"
DATABASE_URL = f"{BASE_URL}{DB_NAME}"

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
