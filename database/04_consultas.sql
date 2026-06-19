-- =============================================================================
-- Módulo 3 - Consultas (DML: SELECT)
-- Consultas que respondem às necessidades do controle de estoque.
-- =============================================================================

USE estoque_trailer;

-- C1) Lista geral de produtos, em ordem alfabética.
SELECT id, nome, categoria, quantidade, validade
FROM produtos
ORDER BY nome;

-- C2) Produtos com estoque baixo (5 unidades ou menos).
SELECT nome, categoria, quantidade
FROM produtos
WHERE quantidade <= 5
ORDER BY quantidade;

-- C3) Produtos vencidos ou que vencem em até 7 dias (usando a VIEW).
SELECT nome, categoria, quantidade, validade, situacao
FROM vw_alertas_validade
WHERE situacao IN ('vencido', 'proximo')
ORDER BY validade;

-- C4) Quantidade total de itens em estoque por categoria (agregação).
SELECT categoria,
       COUNT(*)        AS qtd_produtos,
       SUM(quantidade) AS total_em_estoque
FROM produtos
GROUP BY categoria
ORDER BY total_em_estoque DESC;

-- C5) Histórico de movimentações com o nome do produto (JOIN).
SELECT m.criado_em,
       p.nome AS produto,
       m.tipo,
       m.quantidade,
       m.observacao
FROM movimentacoes m
JOIN produtos p ON p.id = m.produto_id
ORDER BY m.criado_em DESC;

-- C6) Total de entradas e saídas por produto (agregação condicional + JOIN).
SELECT p.nome AS produto,
       SUM(CASE WHEN m.tipo = 'entrada' THEN m.quantidade ELSE 0 END) AS total_entradas,
       SUM(CASE WHEN m.tipo = 'saida'   THEN m.quantidade ELSE 0 END) AS total_saidas
FROM produtos p
LEFT JOIN movimentacoes m ON m.produto_id = p.id
GROUP BY p.id, p.nome
ORDER BY p.nome;
