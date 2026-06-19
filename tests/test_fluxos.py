"""Testes de integração dos fluxos da aplicação web.

Exercitam as rotas reais (HTTP) sobre um banco SQLite temporário, cobrindo o
cadastro, edição e exclusão de produtos, as movimentações de estoque e os
alertas exibidos no painel.
"""
from datetime import date, timedelta

from app.database import SessionLocal
from app.models import Produto


def criar(client, nome, quantidade=10, categoria="Geral", validade=""):
    return client.post(
        "/produtos/novo",
        data={"nome": nome, "categoria": categoria, "quantidade": quantidade, "validade": validade},
        follow_redirects=False,
    )


def id_de(nome):
    db = SessionLocal()
    pid = db.query(Produto).filter_by(nome=nome).first().id
    db.close()
    return pid


def quantidade_de(pid):
    db = SessionLocal()
    q = db.get(Produto, pid).quantidade
    db.close()
    return q


def test_editar_produto_altera_dados(client):
    criar(client, "Coca", quantidade=5)
    pid = id_de("Coca")
    client.post(
        f"/produtos/{pid}/editar",
        data={"nome": "Coca-Cola", "categoria": "Bebidas", "quantidade": 20, "validade": ""},
        follow_redirects=False,
    )
    assert "Coca-Cola" in client.get("/produtos").text
    assert quantidade_de(pid) == 20


def test_excluir_produto_remove_da_lista(client):
    criar(client, "Item temporário")
    pid = id_de("Item temporário")
    client.post(f"/produtos/{pid}/excluir", follow_redirects=False)
    assert "Item temporário" not in client.get("/produtos").text


def test_entrada_incrementa_estoque(client):
    criar(client, "Água", quantidade=10)
    pid = id_de("Água")
    client.post(
        "/movimentacoes/nova",
        data={"produto_id": pid, "tipo": "entrada", "quantidade": 7, "observacao": ""},
        follow_redirects=False,
    )
    assert quantidade_de(pid) == 17


def test_saida_decrementa_estoque(client):
    criar(client, "Suco", quantidade=10)
    pid = id_de("Suco")
    client.post(
        "/movimentacoes/nova",
        data={"produto_id": pid, "tipo": "saida", "quantidade": 4, "observacao": ""},
        follow_redirects=False,
    )
    assert quantidade_de(pid) == 6


def test_movimentacao_aparece_no_historico(client):
    criar(client, "Pão")
    pid = id_de("Pão")
    client.post(
        "/movimentacoes/nova",
        data={"produto_id": pid, "tipo": "entrada", "quantidade": 3, "observacao": "Compra teste"},
        follow_redirects=False,
    )
    historico = client.get("/movimentacoes").text
    assert "Compra teste" in historico and "Pão" in historico


def test_proximo_vencimento_aparece_no_painel(client):
    validade = (date.today() + timedelta(days=2)).isoformat()
    criar(client, "Iogurte", quantidade=10, validade=validade)
    assert "Iogurte" in client.get("/").text


def test_estoque_baixo_aparece_no_painel(client):
    criar(client, "Sal", quantidade=2)
    assert "Sal" in client.get("/").text


def test_form_nova_movimentacao_lista_produtos(client):
    criar(client, "Mostarda")
    assert "Mostarda" in client.get("/movimentacoes/nova").text
