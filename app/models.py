"""Modelos de dados da aplicação (tabelas do banco)."""
import enum

from sqlalchemy import (
    Column,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import relationship

from .database import Base


class TipoMovimentacao(str, enum.Enum):
    """Tipos possíveis de movimentação de estoque."""

    entrada = "entrada"
    saida = "saida"


class Produto(Base):
    """Produto controlado no estoque do trailer."""

    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(120), nullable=False)
    categoria = Column(String(60), nullable=False, default="Geral")
    quantidade = Column(Integer, nullable=False, default=0)
    validade = Column(Date, nullable=True)

    movimentacoes = relationship(
        "Movimentacao",
        back_populates="produto",
        cascade="all, delete-orphan",
        order_by="Movimentacao.criado_em.desc()",
    )


class Movimentacao(Base):
    """Registro de entrada ou saída de um produto."""

    __tablename__ = "movimentacoes"

    id = Column(Integer, primary_key=True, index=True)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    tipo = Column(Enum(TipoMovimentacao), nullable=False)
    quantidade = Column(Integer, nullable=False)
    observacao = Column(String(200), default="")
    criado_em = Column(DateTime, server_default=func.now())

    produto = relationship("Produto", back_populates="movimentacoes")
