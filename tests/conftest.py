"""Configuração dos testes.

Define um banco SQLite temporário ANTES de importar a aplicação, de modo que os
testes não dependam de um servidor MySQL.
"""
import os
import tempfile

# Usa um arquivo SQLite em diretório temporário do sistema para não depender de
# MySQL nem do diretório do projeto (que pode estar em um volume sem suporte a
# lock de arquivo do SQLite).
_db_path = os.path.join(tempfile.gettempdir(), "ufms_pi2_test_estoque.db")
os.environ.setdefault("DATABASE_URL", f"sqlite:///{_db_path}")

import pytest
from fastapi.testclient import TestClient

from app.database import Base, engine
from app.main import app


@pytest.fixture()
def client():
    # Recria o banco a cada teste para garantir isolamento.
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)
