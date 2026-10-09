from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def inicio():
    return render_template(
        "index.html",
        saldo=0.0,
        total_receitas=0.0,
        total_despesas=0.0
    )


if __name__ == "__main__":
    app.run(debug=True)
