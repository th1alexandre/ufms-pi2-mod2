-- Esquema de referência do banco de dados (MySQL).
-- A aplicação cria as tabelas automaticamente via SQLAlchemy, mas este arquivo
-- documenta a estrutura e permite criar o banco manualmente, se preferir.

CREATE DATABASE IF NOT EXISTS estoque_trailer
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE estoque_trailer;

CREATE TABLE IF NOT EXISTS produtos (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  nome        VARCHAR(120) NOT NULL,
  categoria   VARCHAR(60)  NOT NULL DEFAULT 'Geral',
  quantidade  INT          NOT NULL DEFAULT 0,
  validade    DATE         NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS movimentacoes (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  produto_id  INT NOT NULL,
  tipo        ENUM('entrada', 'saida') NOT NULL,
  quantidade  INT NOT NULL,
  observacao  VARCHAR(200) DEFAULT '',
  criado_em   DATETIME DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_movimentacao_produto
    FOREIGN KEY (produto_id) REFERENCES produtos (id)
    ON DELETE CASCADE
) ENGINE=InnoDB;
