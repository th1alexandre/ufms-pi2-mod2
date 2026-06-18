# Controle de Estoque — Trailer de Lanches

Aplicação web para controle de estoque de um trailer de lanches do bairro Pioneiros
(Campo Grande/MS). Desenvolvida para o **Projeto Integrador de Tecnologia da
Informação II — Módulo 2 (Desenvolvimento Web com frameworks e HTML/CSS)**, do
curso de Tecnologia da Informação da UFMS (Programa de Extensão UFMS Digital).

O sistema substitui o controle de estoque feito em papel, permitindo cadastrar
produtos, registrar entradas e saídas e acompanhar, em um painel, os itens
vencidos, próximos do vencimento e com estoque baixo.

## Funcionalidades

- **CRUD de produtos** — cadastrar, listar, editar e excluir produtos (nome,
  categoria, quantidade e data de validade).
- **Movimentações de entrada e saída** — registram o histórico e atualizam
  automaticamente a quantidade em estoque (saída maior que o estoque é bloqueada).
- **Painel de alertas** — destaca produtos vencidos, que vencem em até 7 dias e
  com estoque baixo.

## Tecnologias

- **Python 3.10+** com o framework **FastAPI**
- **SQLAlchemy** + **MySQL** (via PyMySQL) para persistência de dados
- **Jinja2**, **HTML5** semântico e **CSS** responsivo (mobile-first)
- **Uvicorn** como servidor ASGI
- **pytest** para os testes automatizados

## Estrutura do projeto

```
ufms-pi2-mod2/
├── app/
│   ├── main.py            # rotas e regras da aplicação
│   ├── database.py        # conexão com o banco (SQLAlchemy)
│   ├── models.py          # modelos Produto e Movimentacao
│   ├── templates/         # páginas HTML (Jinja2)
│   └── static/css/        # estilos responsivos
├── tests/                 # testes automatizados (pytest)
├── schema.sql             # esquema de referência do MySQL
├── seed.py                # dados de exemplo
├── requirements.txt
└── README.md
```

## Como executar

### 1. Pré-requisitos

- Python 3.10 ou superior
- MySQL em execução (ou usar SQLite, veja abaixo)

### 2. Instalar as dependências

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configurar o banco de dados

Copie `.env.example` para `.env` e ajuste a conexão:

```bash
cp .env.example .env
```

Para **MySQL**, crie o banco (opcionalmente usando o `schema.sql`) e use:

```
DATABASE_URL=mysql+pymysql://usuario:senha@localhost:3306/estoque_trailer
```

Para rodar rapidamente **sem instalar o MySQL**, use SQLite no `.env`:

```
DATABASE_URL=sqlite:///./estoque.db
```

As tabelas são criadas automaticamente na primeira execução.

### 4. (Opcional) Inserir dados de exemplo

```bash
python seed.py
```

### 5. Iniciar a aplicação

```bash
uvicorn app.main:app --reload
```

Acesse `http://localhost:8000`.

## Testes

```bash
pytest
```

Os testes usam um banco SQLite temporário e cobrem o cadastro de produtos, as
movimentações de entrada/saída, o bloqueio de saída acima do estoque e a exibição
de produtos vencidos no painel.

## Decisões de projeto

- **FastAPI** foi escolhido pela simplicidade, boa documentação e validação de
  dados integrada, adequando-se a uma aplicação pequena mantida por uma só pessoa.
- **SQLAlchemy** com `DATABASE_URL` configurável permite usar MySQL no uso real e
  SQLite nos testes, sem alterar o código.
- A interface usa **HTML semântico** e **CSS mobile-first**, já que o proprietário
  acessa o sistema principalmente pelo celular.
- A **quantidade em estoque é derivada das movimentações**: toda entrada/saída
  ajusta o total do produto, mantendo o painel de alertas sempre coerente.
