from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

receitas = []
despesas = []


def calcular_totais():
    total_receitas = sum(item["valor"] for item in receitas)
    total_despesas = sum(item["valor"] for item in despesas)
    saldo = total_receitas - total_despesas
    return total_receitas, total_despesas, saldo


def converter_valor(valor_texto):
    return float(valor_texto.replace(",", "."))


@app.route("/")
def inicio():
    total_receitas, total_despesas, saldo = calcular_totais()

    return render_template(
        "index.html",
        saldo=saldo,
        total_receitas=total_receitas,
        total_despesas=total_despesas,
        receitas=receitas,
        despesas=despesas,
        erro=request.args.get("erro")
    )


@app.route("/receitas", methods=["POST"])
def adicionar_receita_web():
    descricao = request.form.get("descricao", "").strip()
    valor_texto = request.form.get("valor", "").strip()

    try:
        valor = converter_valor(valor_texto)

        if not descricao:
            return redirect(url_for("inicio", erro="Digite uma descrição para a receita."))

        if valor <= 0:
            return redirect(url_for("inicio", erro="O valor da receita deve ser maior que zero."))

        receitas.append({
            "descricao": descricao,
            "valor": valor
        })

    except ValueError:
        return redirect(url_for("inicio", erro="Digite um valor numérico válido para a receita."))

    return redirect(url_for("inicio"))


@app.route("/despesas", methods=["POST"])
def adicionar_despesa_web():
    descricao = request.form.get("descricao", "").strip()
    valor_texto = request.form.get("valor", "").strip()

    try:
        valor = converter_valor(valor_texto)

        if not descricao:
            return redirect(url_for("inicio", erro="Digite uma descrição para a despesa."))

        if valor <= 0:
            return redirect(url_for("inicio", erro="O valor da despesa deve ser maior que zero."))

        despesas.append({
            "descricao": descricao,
            "valor": valor
        })

    except ValueError:
        return redirect(url_for("inicio", erro="Digite um valor numérico válido para a despesa."))

    return redirect(url_for("inicio"))


if __name__ == "__main__":
    app.run(debug=True)
