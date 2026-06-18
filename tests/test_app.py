"""Testes básicos dos principais fluxos da aplicação."""
from datetime import date, timedelta

from app.database import SessionLocal
from app.models import Produto


def criar_produto(client, nome="Salsicha", quantidade=10, validade=""):
    return client.post(
        "/produtos/novo",
        data={
            "nome": nome,
            "categoria": "Frios",
            "quantidade": quantidade,
            "validade": validade,
        },
        follow_redirects=False,
    )


def test_painel_carrega(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert "Painel" in resp.text


def test_cadastrar_produto_aparece_na_lista(client):
    resp = criar_produto(client, nome="Pão de hot dog")
    assert resp.status_code == 303
    lista = client.get("/produtos")
    assert "Pão de hot dog" in lista.text


def test_entrada_e_saida_atualizam_estoque(client):
    criar_produto(client, nome="Refrigerante", quantidade=10)
    db = SessionLocal()
    produto_id = db.query(Produto).filter_by(nome="Refrigerante").first().id
    db.close()

    # Entrada de 5 -> estoque 15
    client.post(
        "/movimentacoes/nova",
        data={"produto_id": produto_id, "tipo": "entrada", "quantidade": 5, "observacao": ""},
        follow_redirects=False,
    )
    # Saída de 3 -> estoque 12
    client.post(
        "/movimentacoes/nova",
        data={"produto_id": produto_id, "tipo": "saida", "quantidade": 3, "observacao": ""},
        follow_redirects=False,
    )

    db = SessionLocal()
    atual = db.get(Produto, produto_id).quantidade
    db.close()
    assert atual == 12


def test_saida_maior_que_estoque_e_bloqueada(client):
    criar_produto(client, nome="Maionese", quantidade=2)
    db = SessionLocal()
    produto_id = db.query(Produto).filter_by(nome="Maionese").first().id
    db.close()

    resp = client.post(
        "/movimentacoes/nova",
        data={"produto_id": produto_id, "tipo": "saida", "quantidade": 10, "observacao": ""},
        follow_redirects=False,
    )
    assert resp.status_code == 400

    db = SessionLocal()
    atual = db.get(Produto, produto_id).quantidade
    db.close()
    assert atual == 2  # estoque não foi alterado


def test_produto_vencido_aparece_no_painel(client):
    ontem = (date.today() - timedelta(days=1)).isoformat()
    criar_produto(client, nome="Item vencido", quantidade=4, validade=ontem)
    painel = client.get("/")
    assert "Item vencido" in painel.text
