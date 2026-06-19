-- =============================================================================
-- Módulo 3 - Carga inicial de dados (DML: INSERT)
-- Popula o banco com produtos e movimentações de exemplo do trailer de lanches.
-- =============================================================================

USE estoque_trailer;

-- ---- Produtos --------------------------------------------------------------
INSERT INTO produtos (nome, categoria, quantidade, validade) VALUES
  ('Pão de hot dog (pacote)',  'Pães',          12, CURDATE() + INTERVAL 3  DAY),
  ('Salsicha (kg)',            'Frios',          8, CURDATE() + INTERVAL 10 DAY),
  ('Refrigerante lata 350ml',  'Bebidas',       40, CURDATE() + INTERVAL 120 DAY),
  ('Maionese (sachê)',         'Molhos',         3, CURDATE() - INTERVAL 2  DAY),
  ('Batata palha',             'Complementos',   5, CURDATE() + INTERVAL 45 DAY),
  ('Queijo cheddar fatiado',   'Frios',          2, CURDATE() + INTERVAL 5  DAY),
  ('Guardanapo (pacote)',      'Descartáveis',  20, NULL);

-- ---- Movimentações ---------------------------------------------------------
-- (referenciam os produtos pelo nome para não depender dos ids gerados)
INSERT INTO movimentacoes (produto_id, tipo, quantidade, observacao)
SELECT id, 'entrada', 12, 'Compra semanal'        FROM produtos WHERE nome = 'Pão de hot dog (pacote)';
INSERT INTO movimentacoes (produto_id, tipo, quantidade, observacao)
SELECT id, 'entrada', 24, 'Reposição de bebidas'  FROM produtos WHERE nome = 'Refrigerante lata 350ml';
INSERT INTO movimentacoes (produto_id, tipo, quantidade, observacao)
SELECT id, 'saida',    6, 'Vendas do dia'         FROM produtos WHERE nome = 'Refrigerante lata 350ml';
INSERT INTO movimentacoes (produto_id, tipo, quantidade, observacao)
SELECT id, 'entrada',  8, 'Compra no atacado'     FROM produtos WHERE nome = 'Salsicha (kg)';
INSERT INTO movimentacoes (produto_id, tipo, quantidade, observacao)
SELECT id, 'saida',    2, 'Uso na produção'       FROM produtos WHERE nome = 'Maionese (sachê)';
