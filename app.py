import sqlite3
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


def listar_movimentacoes(tipo):
    with conectar_banco() as conexao:
        registros = conexao.execute(
            """
            SELECT id, descricao, valor, criado_em
            FROM movimentacoes
            WHERE tipo = ?
            ORDER BY id DESC
            """,
            (tipo,)
        ).fetchall()

    return registros


def calcular_totais():
    with conectar_banco() as conexao:
        totais = conexao.execute(
            """
            SELECT
                COALESCE(
                    SUM(CASE WHEN tipo = 'receita' THEN valor ELSE 0 END),
                    0
                ) AS total_receitas,
                COALESCE(
                    SUM(CASE WHEN tipo = 'despesa' THEN valor ELSE 0 END),
                    0
                ) AS total_despesas
            FROM movimentacoes
            """
        ).fetchone()

    total_receitas = totais["total_receitas"]
    total_despesas = totais["total_despesas"]
    saldo = total_receitas - total_despesas

    return total_receitas, total_despesas, saldo


def converter_valor(valor_texto):
    return float(valor_texto.replace(",", "."))


def salvar_movimentacao(tipo, descricao, valor):
    with conectar_banco() as conexao:
        conexao.execute(
            """
            INSERT INTO movimentacoes (tipo, descricao, valor)
            VALUES (?, ?, ?)
            """,
            (tipo, descricao, valor)
        )


@app.route("/")
def inicio():
    total_receitas, total_despesas, saldo = calcular_totais()

    return render_template(
        "index.html",
        saldo=saldo,
        total_receitas=total_receitas,
        total_despesas=total_despesas,
        receitas=listar_movimentacoes("receita"),
        despesas=listar_movimentacoes("despesa"),
        erro=request.args.get("erro")
    )


@app.route("/receitas", methods=["POST"])
def adicionar_receita_web():
    descricao = request.form.get("descricao", "").strip()
    valor_texto = request.form.get("valor", "").strip()

    try:
        valor = converter_valor(valor_texto)

        if not descricao:
            return redirect(
                url_for("inicio", erro="Digite uma descrição para a receita.")
            )

        if valor <= 0:
            return redirect(
                url_for(
                    "inicio",
                    erro="O valor da receita deve ser maior que zero."
                )
            )

        salvar_movimentacao("receita", descricao, valor)

    except ValueError:
        return redirect(
            url_for(
                "inicio",
                erro="Digite um valor numérico válido para a receita."
            )
        )

    return redirect(url_for("inicio"))


@app.route("/despesas", methods=["POST"])
def adicionar_despesa_web():
    descricao = request.form.get("descricao", "").strip()
    valor_texto = request.form.get("valor", "").strip()

    try:
        valor = converter_valor(valor_texto)

        if not descricao:
            return redirect(
                url_for("inicio", erro="Digite uma descrição para a despesa.")
            )

        if valor <= 0:
            return redirect(
                url_for(
                    "inicio",
                    erro="O valor da despesa deve ser maior que zero."
                )
            )

        salvar_movimentacao("despesa", descricao, valor)

    except ValueError:
        return redirect(
            url_for(
                "inicio",
                erro="Digite um valor numérico válido para a despesa."
            )
        )

    return redirect(url_for("inicio"))


criar_banco()


if __name__ == "__main__":
    app.run(debug=True)
