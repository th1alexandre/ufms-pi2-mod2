"""Popula o banco com alguns produtos de exemplo para demonstração.

Uso:
    python seed.py
"""
from datetime import date, timedelta

from app.database import Base, SessionLocal, engine
from app.models import Movimentacao, Produto, TipoMovimentacao

Base.metadata.create_all(bind=engine)

hoje = date.today()

produtos_exemplo = [
    Produto(nome="Pão de hot dog (pacote)", categoria="Pães", quantidade=12, validade=hoje + timedelta(days=3)),
    Produto(nome="Salsicha (kg)", categoria="Frios", quantidade=8, validade=hoje + timedelta(days=10)),
    Produto(nome="Refrigerante lata", categoria="Bebidas", quantidade=40, validade=hoje + timedelta(days=120)),
    Produto(nome="Maionese (sachê)", categoria="Molhos", quantidade=3, validade=hoje - timedelta(days=2)),
    Produto(nome="Batata palha", categoria="Complementos", quantidade=5, validade=hoje + timedelta(days=45)),
]


def main():
    db = SessionLocal()
    try:
        if db.query(Produto).count() > 0:
            print("O banco já possui produtos. Nada foi inserido.")
            return
        db.add_all(produtos_exemplo)
        db.commit()
        primeiro = db.query(Produto).first()
        db.add(
            Movimentacao(
                produto_id=primeiro.id,
                tipo=TipoMovimentacao.entrada,
                quantidade=12,
                observacao="Carga inicial de exemplo",
            )
        )
        db.commit()
        print(f"{len(produtos_exemplo)} produtos de exemplo inseridos com sucesso.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
