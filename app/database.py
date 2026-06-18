"""Configuração da conexão com o banco de dados (SQLAlchemy).

A string de conexão é lida da variável de ambiente DATABASE_URL, o que permite
usar MySQL no uso real e SQLite durante os testes/desenvolvimento sem alterar o
código.
"""
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:root@localhost:3306/estoque_trailer",
)

# SQLite precisa de um argumento extra quando usado com o servidor web.
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


def get_db():
    """Fornece uma sessão de banco por requisição (dependência do FastAPI)."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
