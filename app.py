import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

CAMINHO_BANCO = Path(__file__).with_name("financeiro.db")


def conectar_banco():
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.row_factory = sqlite3.Row
    return conexao


def criar_banco():
    with conectar_banco() as conexao:
        conexao.execute(
            """
            CREATE TABLE IF NOT EXISTS movimentacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT NOT NULL CHECK (tipo IN ('receita', 'despesa')),
                descricao TEXT NOT NULL,
                valor REAL NOT NULL CHECK (valor > 0),
                criado_em DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def listar_movimentacoes():
    with conectar_banco() as conexao:
        return conexao.execute(
            """
            SELECT id, tipo, descricao, valor, criado_em
            FROM movimentacoes
            ORDER BY id DESC
            """
        ).fetchall()


def calcular_resumo():
    with conectar_banco() as conexao:
        resumo = conexao.execute(
            """
            SELECT
                COALESCE(SUM(CASE WHEN tipo = 'receita' THEN valor ELSE 0 END), 0)
                    AS total_receitas,
                COALESCE(SUM(CASE WHEN tipo = 'despesa' THEN valor ELSE 0 END), 0)
                    AS total_despesas,
                COUNT(*) AS quantidade
            FROM movimentacoes
            """
        ).fetchone()

    total_receitas = resumo["total_receitas"]
    total_despesas = resumo["total_despesas"]
    saldo = total_receitas - total_despesas

    if total_receitas > 0:
        percentual_disponivel = (saldo / total_receitas) * 100
    else:
        percentual_disponivel = 0

    return {
        "saldo": saldo,
        "total_receitas": total_receitas,
        "total_despesas": total_despesas,
        "quantidade": resumo["quantidade"],
        "percentual_disponivel": percentual_disponivel,
    }


def converter_valor(valor_texto):
    valor_limpo = valor_texto.strip().replace("R$", "").replace(" ", "")

    if "," in valor_limpo:
        valor_limpo = valor_limpo.replace(".", "").replace(",", ".")

    return float(valor_limpo)


def salvar_movimentacao(tipo, descricao, valor):
    with conectar_banco() as conexao:
        conexao.execute(
            """
            INSERT INTO movimentacoes (tipo, descricao, valor)
            VALUES (?, ?, ?)
            """,
            (tipo, descricao, valor),
        )


def validar_movimentacao(descricao, valor_texto, tipo):
    nome_tipo = "receita" if tipo == "receita" else "despesa"

    if not descricao:
        return None, f"Digite uma descrição para a {nome_tipo}."

    if len(descricao) > 60:
        return None, "A descrição deve ter no máximo 60 caracteres."

    try:
        valor = converter_valor(valor_texto)
    except ValueError:
        return None, f"Digite um valor numérico válido para a {nome_tipo}."

    if valor <= 0:
        return None, f"O valor da {nome_tipo} deve ser maior que zero."

    return valor, None


@app.template_filter("brl")
def formatar_brl(valor):
    numero = f"{float(valor):,.2f}"
    numero = numero.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {numero}"


@app.template_filter("data_br")
def formatar_data_br(valor):
    if not valor:
        return ""

    try:
        data_utc = datetime.strptime(valor, "%Y-%m-%d %H:%M:%S").replace(
            tzinfo=timezone.utc
        )
        horario_brasilia = data_utc.astimezone(timezone(timedelta(hours=-3)))
        return horario_brasilia.strftime("%d/%m/%Y • %H:%M")
    except ValueError:
        return valor


@app.route("/")
def inicio():
    return render_template(
        "index.html",
        resumo=calcular_resumo(),
        movimentacoes=listar_movimentacoes(),
        erro=request.args.get("erro"),
        sucesso=request.args.get("sucesso"),
    )


@app.route("/receitas", methods=["POST"])
def adicionar_receita_web():
    descricao = request.form.get("descricao", "").strip()
    valor_texto = request.form.get("valor", "").strip()

    valor, erro = validar_movimentacao(descricao, valor_texto, "receita")

    if erro:
        return redirect(url_for("inicio", erro=erro))

    salvar_movimentacao("receita", descricao, valor)
    return redirect(url_for("inicio", sucesso="Receita adicionada com sucesso."))


@app.route("/despesas", methods=["POST"])
def adicionar_despesa_web():
    descricao = request.form.get("descricao", "").strip()
    valor_texto = request.form.get("valor", "").strip()

    valor, erro = validar_movimentacao(descricao, valor_texto, "despesa")

    if erro:
        return redirect(url_for("inicio", erro=erro))

    salvar_movimentacao("despesa", descricao, valor)
    return redirect(url_for("inicio", sucesso="Despesa adicionada com sucesso."))


@app.route("/movimentacoes/<int:movimentacao_id>/excluir", methods=["POST"])
def excluir_movimentacao(movimentacao_id):
    with conectar_banco() as conexao:
        movimentacao = conexao.execute(
            "SELECT id FROM movimentacoes WHERE id = ?",
            (movimentacao_id,),
        ).fetchone()

        if movimentacao is None:
            return redirect(
                url_for("inicio", erro="Essa movimentação não foi encontrada.")
            )

        conexao.execute(
            "DELETE FROM movimentacoes WHERE id = ?",
            (movimentacao_id,),
        )

    return redirect(url_for("inicio", sucesso="Movimentação excluída."))


criar_banco()


if __name__ == "__main__":
    app.run(debug=True)
