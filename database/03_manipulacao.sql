-- =============================================================================
-- Módulo 3 - Manipulação de dados (DML: UPDATE e DELETE)
-- Exemplos de operações de atualização e remoção de registros.
-- =============================================================================

USE estoque_trailer;

-- 1) Registrar uma ENTRADA e atualizar o estoque do produto.
--    (a aplicação faz isso em uma transação; aqui demonstramos em SQL puro)
INSERT INTO movimentacoes (produto_id, tipo, quantidade, observacao)
SELECT id, 'entrada', 10, 'Reposição de pães' FROM produtos WHERE nome = 'Pão de hot dog (pacote)';

UPDATE produtos
SET quantidade = quantidade + 10
WHERE nome = 'Pão de hot dog (pacote)';

-- 2) Registrar uma SAÍDA (venda) e abater do estoque.
INSERT INTO movimentacoes (produto_id, tipo, quantidade, observacao)
SELECT id, 'saida', 5, 'Vendas do dia' FROM produtos WHERE nome = 'Refrigerante lata 350ml';

UPDATE produtos
SET quantidade = quantidade - 5
WHERE nome = 'Refrigerante lata 350ml' AND quantidade >= 5;

-- 3) Corrigir a categoria de um produto.
UPDATE produtos
SET categoria = 'Laticínios'
WHERE nome = 'Queijo cheddar fatiado';

-- 4) Remover um produto vencido do cadastro.
--    Por causa do ON DELETE CASCADE, as movimentações ligadas a ele também
--    são removidas automaticamente, preservando a integridade referencial.
DELETE FROM produtos
WHERE nome = 'Maionese (sachê)';
