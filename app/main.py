"""Aplicação web de controle de estoque para um trailer de lanches.

Projeto Integrador de Tecnologia da Informação II - Módulo 2 (UFMS).
Framework: FastAPI. Banco de dados: MySQL (SQLAlchemy). Interface: HTML + CSS.
"""
from datetime import date, timedelta
from pathlib import Path

from fastapi import Depends, FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import Movimentacao, Produto, TipoMovimentacao

# Quantos dias antes da validade um produto entra na lista de "próximos do vencimento".
DIAS_ALERTA_VALIDADE = 7
# Abaixo (ou igual) desta quantidade o produto é considerado com estoque baixo.
LIMITE_ESTOQUE_BAIXO = 5

BASE_DIR = Path(__file__).resolve().parent

# Cria as tabelas no banco caso ainda não existam.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Controle de Estoque - Trailer de Lanches")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


def classificar_validade(produto: Produto, hoje: date) -> str:
    """Retorna 'vencido', 'proximo', 'ok' ou 'sem_validade' para um produto."""
    if produto.validade is None:
        return "sem_validade"
    if produto.validade < hoje:
        return "vencido"
    if produto.validade <= hoje + timedelta(days=DIAS_ALERTA_VALIDADE):
        return "proximo"
    return "ok"


@app.get("/", response_class=HTMLResponse)
def painel(request: Request, db: Session = Depends(get_db)):
    """Painel inicial com os alertas de validade e de estoque baixo."""
    hoje = date.today()
    produtos = db.query(Produto).all()

    vencidos = [p for p in produtos if classificar_validade(p, hoje) == "vencido"]
    proximos = [p for p in produtos if classificar_validade(p, hoje) == "proximo"]
    estoque_baixo = [p for p in produtos if p.quantidade <= LIMITE_ESTOQUE_BAIXO]

    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "request": request,
            "total_produtos": len(produtos),
            "vencidos": vencidos,
            "proximos": proximos,
            "estoque_baixo": estoque_baixo,
            "dias_alerta": DIAS_ALERTA_VALIDADE,
            "hoje": hoje,
        },
    )


@app.get("/produtos", response_class=HTMLResponse)
def listar_produtos(request: Request, db: Session = Depends(get_db)):
    hoje = date.today()
    produtos = db.query(Produto).order_by(Produto.nome).all()
    situacoes = {p.id: classificar_validade(p, hoje) for p in produtos}
    return templates.TemplateResponse(
        request,
        "produtos.html",
        {"request": request, "produtos": produtos, "situacoes": situacoes},
    )


@app.get("/produtos/novo", response_class=HTMLResponse)
def novo_produto(request: Request):
    return templates.TemplateResponse(
        request,
        "produto_form.html",
        {"request": request, "produto": None, "acao": "/produtos/novo"},
    )


@app.post("/produtos/novo")
def criar_produto(
    nome: str = Form(...),
    categoria: str = Form("Geral"),
    quantidade: int = Form(0),
    validade: str = Form(""),
    db: Session = Depends(get_db),
):
    produto = Produto(
        nome=nome.strip(),
        categoria=categoria.strip() or "Geral",
        quantidade=max(quantidade, 0),
        validade=date.fromisoformat(validade) if validade else None,
    )
    db.add(produto)
    db.commit()
    return RedirectResponse("/produtos", status_code=303)


@app.get("/produtos/{produto_id}/editar", response_class=HTMLResponse)
def editar_produto(produto_id: int, request: Request, db: Session = Depends(get_db)):
    produto = db.get(Produto, produto_id)
    if produto is None:
        return RedirectResponse("/produtos", status_code=303)
    return templates.TemplateResponse(
        request,
        "produto_form.html",
        {
            "request": request,
            "produto": produto,
            "acao": f"/produtos/{produto_id}/editar",
        },
    )


@app.post("/produtos/{produto_id}/editar")
def atualizar_produto(
    produto_id: int,
    nome: str = Form(...),
    categoria: str = Form("Geral"),
    quantidade: int = Form(0),
    validade: str = Form(""),
    db: Session = Depends(get_db),
):
    produto = db.get(Produto, produto_id)
    if produto is not None:
        produto.nome = nome.strip()
        produto.categoria = categoria.strip() or "Geral"
        produto.quantidade = max(quantidade, 0)
        produto.validade = date.fromisoformat(validade) if validade else None
        db.commit()
    return RedirectResponse("/produtos", status_code=303)


@app.post("/produtos/{produto_id}/excluir")
def excluir_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.get(Produto, produto_id)
    if produto is not None:
        db.delete(produto)
        db.commit()
    return RedirectResponse("/produtos", status_code=303)


@app.get("/movimentacoes", response_class=HTMLResponse)
def listar_movimentacoes(request: Request, db: Session = Depends(get_db)):
    movimentacoes = (
        db.query(Movimentacao).order_by(Movimentacao.criado_em.desc()).all()
    )
    return templates.TemplateResponse(
        request,
        "movimentacoes.html",
        {"request": request, "movimentacoes": movimentacoes},
    )


@app.get("/movimentacoes/nova", response_class=HTMLResponse)
def nova_movimentacao(request: Request, db: Session = Depends(get_db)):
    produtos = db.query(Produto).order_by(Produto.nome).all()
    return templates.TemplateResponse(
        request,
        "movimentacao_form.html",
        {"request": request, "produtos": produtos, "erro": None},
    )


@app.post("/movimentacoes/nova")
def criar_movimentacao(
    request: Request,
    produto_id: int = Form(...),
    tipo: str = Form(...),
    quantidade: int = Form(...),
    observacao: str = Form(""),
    db: Session = Depends(get_db),
):
    produto = db.get(Produto, produto_id)
    quantidade = max(quantidade, 1)

    erro = None
    if produto is None:
        erro = "Produto não encontrado."
    elif tipo == TipoMovimentacao.saida.value and quantidade > produto.quantidade:
        erro = (
            f"Não é possível dar saída de {quantidade} unidade(s): "
            f"o estoque atual de '{produto.nome}' é {produto.quantidade}."
        )

    if erro:
        produtos = db.query(Produto).order_by(Produto.nome).all()
        return templates.TemplateResponse(
            request,
            "movimentacao_form.html",
            {"request": request, "produtos": produtos, "erro": erro},
            status_code=400,
        )

    movimentacao = Movimentacao(
        produto_id=produto.id,
        tipo=TipoMovimentacao(tipo),
        quantidade=quantidade,
        observacao=observacao.strip(),
    )
    if movimentacao.tipo == TipoMovimentacao.entrada:
        produto.quantidade += quantidade
    else:
        produto.quantidade -= quantidade

    db.add(movimentacao)
    db.commit()
    return RedirectResponse("/movimentacoes", status_code=303)
