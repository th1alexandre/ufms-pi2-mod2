"""Testes unitários da regra de classificação de validade.

Verificam, de forma isolada (sem banco de dados), a função que classifica um
produto como vencido, próximo do vencimento, em dia ou sem validade.
"""
from datetime import date, timedelta

from app.main import DIAS_ALERTA_VALIDADE, classificar_validade
from app.models import Produto

HOJE = date(2026, 6, 19)


def produto(validade):
    return Produto(nome="Teste", categoria="Geral", quantidade=1, validade=validade)


def test_sem_validade():
    assert classificar_validade(produto(None), HOJE) == "sem_validade"


def test_vencido():
    assert classificar_validade(produto(HOJE - timedelta(days=1)), HOJE) == "vencido"


def test_proximo_no_limite_de_7_dias():
    validade = HOJE + timedelta(days=DIAS_ALERTA_VALIDADE)
    assert classificar_validade(produto(validade), HOJE) == "proximo"


def test_proximo_quando_vence_hoje():
    assert classificar_validade(produto(HOJE), HOJE) == "proximo"


def test_em_dia_quando_validade_distante():
    assert classificar_validade(produto(HOJE + timedelta(days=30)), HOJE) == "ok"
