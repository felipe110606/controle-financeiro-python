# Controle Financeiro em Python

Projeto de estudos e portfólio desenvolvido em Python, evoluindo de uma aplicação de terminal para uma aplicação web com persistência de dados.

## Versões do projeto

### Versão 1 — Terminal

A primeira versão funciona diretamente no terminal e foi criada para praticar lógica de programação, funções, listas, dicionários, validações e tratamento de erros.

Arquivo principal:

```text
controle_financeiro.py
```

### Versão 2 — Web

A versão web usa Flask, HTML, CSS e SQLite.

Ela permite cadastrar receitas e despesas pelo navegador e mantém os dados salvos mesmo depois que o servidor é encerrado.

Arquivo principal:

```text
app.py
```

## Funcionalidades atuais

- Adicionar receitas com descrição e valor
- Adicionar despesas com descrição e valor
- Listar movimentações
- Calcular total de receitas
- Calcular total de despesas
- Calcular saldo atual automaticamente
- Validar valores inválidos, negativos ou iguais a zero
- Interface web responsiva
- Persistência local com SQLite

## Tecnologias

- Python
- Flask
- SQLite
- HTML
- CSS
- Git
- GitHub

## Conceitos praticados

- Variáveis
- `input()` e `print()`
- `if`, `elif` e `else`
- `while` e `break`
- Listas e dicionários
- `append()`
- `for`
- `len()` e `sum()`
- Funções com `def`
- Parâmetros e `return`
- `try` / `except`
- `ValueError`
- F-strings
- Rotas Flask
- Requisições GET e POST
- Formulários HTML
- Templates com Jinja
- SQL básico
- `CREATE TABLE`, `INSERT` e `SELECT`

## Como executar a versão web

1. Tenha o Python instalado.
2. Clone ou baixe este repositório.
3. Abra o terminal na pasta do projeto.
4. Crie um ambiente virtual:

```bash
python -m venv .venv
```

5. Ative o ambiente virtual no Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

6. Instale as dependências:

```bash
pip install -r requirements.txt
```

7. Execute:

```bash
python app.py
```

8. Abra no navegador:

```text
http://127.0.0.1:5000
```

O arquivo `financeiro.db` é criado automaticamente na primeira execução e fica apenas na máquina local.

## Como executar a versão de terminal

```bash
python controle_financeiro.py
```

## Estrutura atual

```text
controle-financeiro-python/
├── app.py
├── controle_financeiro.py
├── requirements.txt
├── README.md
├── .gitignore
├── templates/
│   └── index.html
└── static/
    └── style.css
```

## Próximas evoluções

- Excluir movimentações
- Editar movimentações
- Adicionar categorias
- Exibir datas de forma amigável
- Filtros por período
- Melhorias visuais
- Testes automatizados
- Publicação da aplicação web

---

Projeto desenvolvido como parte dos meus estudos de Python e desenvolvimento de software.
