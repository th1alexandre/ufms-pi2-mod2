# Banco de Dados — Módulo 3

Scripts de modelagem e manipulação do banco de dados do sistema de controle de
estoque do trailer de lanches, referentes ao **Módulo 3 (Banco de Dados e
Controle de versão)** do Projeto Integrador de TI II.

## Modelo de dados

O banco possui duas entidades e um relacionamento:

- **produtos** — itens do estoque (nome, categoria, quantidade, validade).
- **movimentacoes** — entradas e saídas de cada produto (tipo, quantidade,
  observação, data).

Relacionamento: **um produto possui muitas movimentações** (1:N). A coluna
`movimentacoes.produto_id` é chave estrangeira para `produtos.id`, com
`ON DELETE CASCADE` (ao excluir um produto, seu histórico é removido junto),
garantindo a integridade referencial.

### Restrições aplicadas

- Chaves primárias (`id`) em ambas as tabelas.
- Chave estrangeira `fk_movimentacao_produto`.
- `NOT NULL` nos campos obrigatórios e `DEFAULT` para categoria/quantidade.
- `CHECK (quantidade >= 0)` em produtos e `CHECK (quantidade > 0)` em movimentações.
- `ENUM('entrada','saida')` restringe os tipos de movimentação.
- Índices em `nome`, `validade` e `produto_id` para acelerar as consultas.

### Normalização

O modelo está na **3ª forma normal (3NF)**: cada tabela trata de uma única
entidade, não há grupos repetidos e todos os atributos dependem apenas da chave
primária. A `view` **vw_alertas_validade** encapsula a regra de classificação de
validade (vencido / próximo / em dia), evitando repetir essa lógica nas consultas.

## Arquivos

| Arquivo | Conteúdo |
|---------|----------|
| `01_schema.sql` | DDL: criação do banco, tabelas, restrições, índices e a view. |
| `02_carga_inicial.sql` | DML: inserção de produtos e movimentações de exemplo. |
| `03_manipulacao.sql` | DML: exemplos de `UPDATE` e `DELETE`. |
| `04_consultas.sql` | DML: consultas `SELECT` (filtros, agregações e `JOIN`). |

## Como executar (MySQL)

```bash
mysql -u usuario -p < 01_schema.sql
mysql -u usuario -p estoque_trailer < 02_carga_inicial.sql
mysql -u usuario -p estoque_trailer < 03_manipulacao.sql
mysql -u usuario -p estoque_trailer < 04_consultas.sql
```

> Observação: este é o mesmo banco usado pela aplicação web (FastAPI), definido
> via `DATABASE_URL`. Os scripts documentam o esquema e demonstram as operações
> de manipulação exigidas no módulo.
