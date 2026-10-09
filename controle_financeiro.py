def mostrar_menu():
    print("\n=== CONTROLE FINANCEIRO ===")
    print("1 - Adicionar receita")
    print("2 - Adicionar despesa")
    print("3 - Ver receitas")
    print("4 - Ver despesas")
    print("5 - Ver saldo")
    print("6 - Ver resumo financeiro")
    print("7 - Sair")


def adicionar_despesa(despesas, saldo):
    try:
        descricao_despesa = input("Descrição da despesa: ")
        valor_despesa = float(input("Valor da despesa: R$ "))

        if valor_despesa <= 0:
            print("O valor da despesa deve ser maior que zero.")
            return saldo

        despesas.append({
            "descricao": descricao_despesa,
            "valor": valor_despesa
        })

        saldo = saldo - valor_despesa

        print(f"Despesa adicionada: R$ {valor_despesa:.2f}")
        print(f"Saldo atual: R$ {saldo:.2f}")

        return saldo

    except ValueError:
        print("Valor inválido. Digite apenas números.")
        return saldo


def adicionar_receita(receitas, saldo):
    try:
        descricao_receita = input("Descrição da receita: ")
        valor_receita = float(input("Valor da receita: R$ "))

        if valor_receita <= 0:
            print("O valor da receita deve ser maior que zero.")
            return saldo

        receitas.append({
            "descricao": descricao_receita,
            "valor": valor_receita
        })

        saldo = saldo + valor_receita

        print(f"Receita adicionada: R$ {valor_receita:.2f}")
        print(f"Saldo atual: R$ {saldo:.2f}")

        return saldo

    except ValueError:
        print("Valor inválido. Digite apenas números.")
        return saldo


def mostrar_receitas(receitas):
    if len(receitas) == 0:
        print("Nenhuma receita registrada")
    else:
        print("=== RECEITAS ===")

        for item in receitas:
            print(f'{item["descricao"]} - R$ {item["valor"]:.2f}')


def mostrar_despesas(despesas):
    if len(despesas) == 0:
        print("Nenhuma despesa registrada")
    else:
        print("=== DESPESAS ===")

        for item in despesas:
            print(f'{item["descricao"]} - R$ {item["valor"]:.2f}')


def mostrar_saldo(saldo):
    print(f"Saldo atual = R$ {saldo:.2f}")


def mostrar_resumo(receitas, despesas, saldo):
    total_receitas = sum(item["valor"] for item in receitas)
    total_despesas = sum(item["valor"] for item in despesas)

    print("=== RESUMO FINANCEIRO ===")
    print(f"Total de receitas = R$ {total_receitas:.2f}")
    print(f"Total de despesas = R$ {total_despesas:.2f}")
    print(f"Saldo atual = R$ {saldo:.2f}")


saldo = 0
receitas = []
despesas = []

while True:
    mostrar_menu()

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        saldo = adicionar_receita(receitas, saldo)

    elif opcao == "2":
        saldo = adicionar_despesa(despesas, saldo)

    elif opcao == "3":
        mostrar_receitas(receitas)

    elif opcao == "4":
        mostrar_despesas(despesas)

    elif opcao == "5":
        mostrar_saldo(saldo)

    elif opcao == "6":
        mostrar_resumo(receitas, despesas, saldo)

    elif opcao == "7":
        print("Programa encerrado")
        break

    else:
        print("Opção inválida. Tente novamente.")
