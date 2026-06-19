-- =============================================================================
-- Projeto Integrador de TI II - Módulo 3 (Banco de Dados e Controle de versão)
-- Esquema do banco de dados (DDL) - MySQL 8
--
-- Sistema de controle de estoque de um trailer de lanches (bairro Pioneiros,
-- Campo Grande/MS). Modelo relacional com duas entidades e um relacionamento
-- 1:N entre PRODUTO e MOVIMENTAÇÃO.
-- =============================================================================

CREATE DATABASE IF NOT EXISTS estoque_trailer
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE estoque_trailer;

-- Remove as tabelas em ordem segura (respeitando a chave estrangeira).
DROP TABLE IF EXISTS movimentacoes;
DROP TABLE IF EXISTS produtos;

-- -----------------------------------------------------------------------------
-- Entidade: PRODUTO
-- Item controlado no estoque do trailer.
-- Restrições: PK; nome obrigatório; quantidade não negativa (CHECK);
-- categoria com valor padrão.
-- -----------------------------------------------------------------------------
CREATE TABLE produtos (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  nome        VARCHAR(120) NOT NULL,
  categoria   VARCHAR(60)  NOT NULL DEFAULT 'Geral',
  quantidade  INT          NOT NULL DEFAULT 0,
  validade    DATE         NULL,
  CONSTRAINT chk_produto_quantidade CHECK (quantidade >= 0)
) ENGINE=InnoDB;

-- Índices para acelerar buscas frequentes (por nome e por validade).
CREATE INDEX idx_produtos_nome     ON produtos (nome);
CREATE INDEX idx_produtos_validade ON produtos (validade);

-- -----------------------------------------------------------------------------
-- Entidade: MOVIMENTAÇÃO
-- Registro de entrada ou saída de um produto (histórico de estoque).
-- Relacionamento: cada movimentação pertence a um produto (N:1).
-- Restrições: PK; FK para produtos com ON DELETE CASCADE; tipo restrito a
-- 'entrada'/'saida' (ENUM); quantidade positiva (CHECK).
-- -----------------------------------------------------------------------------
CREATE TABLE movimentacoes (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  produto_id  INT NOT NULL,
  tipo        ENUM('entrada', 'saida') NOT NULL,
  quantidade  INT NOT NULL,
  observacao  VARCHAR(200) DEFAULT '',
  criado_em   DATETIME DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_movimentacao_produto
    FOREIGN KEY (produto_id) REFERENCES produtos (id)
    ON DELETE CASCADE,
  CONSTRAINT chk_movimentacao_quantidade CHECK (quantidade > 0)
) ENGINE=InnoDB;

CREATE INDEX idx_movimentacoes_produto ON movimentacoes (produto_id);

-- -----------------------------------------------------------------------------
-- VISÃO (VIEW): alertas de validade
-- Classifica cada produto como 'vencido', 'proximo' (vence em até 7 dias),
-- 'sem_validade' ou 'em_dia'. Facilita a consulta usada no painel da aplicação.
-- -----------------------------------------------------------------------------
CREATE OR REPLACE VIEW vw_alertas_validade AS
SELECT
  p.id,
  p.nome,
  p.categoria,
  p.quantidade,
  p.validade,
  CASE
    WHEN p.validade IS NULL THEN 'sem_validade'
    WHEN p.validade < CURDATE() THEN 'vencido'
    WHEN p.validade <= CURDATE() + INTERVAL 7 DAY THEN 'proximo'
    ELSE 'em_dia'
  END AS situacao
FROM produtos p;
