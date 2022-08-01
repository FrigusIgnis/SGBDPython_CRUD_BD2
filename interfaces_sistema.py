import os
import time

from datetime import date
from datetime import datetime
from gerenciamento_caixa import * #Gerenciamento de caixa
from gerenciamento_estoque import * #Gerenciamento de estoque
from gerenciamento_funcionario import * #Gerenciamento de funcionários(Administração)

def caixaMenu():
    listaProdutos = []
    valorTotal = 0.0
    resumoCompra = ""

    while True:
        os.system("clear")
        caixaRelatorio = open("Caixa.txt", 'a')
        resumoCompra = atualizarResumoCompra(resumoCompra, listaProdutos)
        valorTotal = atualizarValorTotal(valorTotal, listaProdutos)
        caixaOp = int(input("""CAIXA HortiLife\n\nCarrinho de compras atual\n%s
        \n
        --> Valor Total: %.2f
        \n

        1. Adicionar itens
        2. Retirar item
        3. Fechar compra
        4. Sair
        
        COMANDO: """ % (resumoCompra, valorTotal)))

        if caixaOp == 1:
            os.system("clear")
            while True:
                itemCompra = {"Nome": "", "Quantidade": 0,
                              "Preco": 0.0, "Codigo": 0}
                item = input("Insira o código e a quantidade: ").split(" ")
                if item[0] != "0":
                    check = False
                    itemDados = procurarProduto(int(item[0]))
                    if itemDados != None:
                        itemCompra = {"Nome": itemDados["Nome"], "Quantidade": int(
                            item[1]), "Preco": itemDados["Preco"], "Codigo": itemDados["Codigo"], "Marca": itemDados["Marca"]}
                        for produtoCheck in listaProdutos:
                            if itemCompra["Codigo"] == produtoCheck["Codigo"]:
                                listaProdutos[listaProdutos.index(
                                    produtoCheck)]["Quantidade"] += itemCompra["Quantidade"]
                                check = True
                                break
                        if check == False:
                            listaProdutos.append(itemCompra)
                    else:
                        print("Código inválido! Tente novamente\n")
                else:
                    break

        elif caixaOp == 2:
            print()
            retirarID = int(input("Código do produto: "))
            listaProdutos = retirarProduto(listaProdutos, retirarID)

        elif caixaOp == 3:
            for item in listaProdutos:
                atualizarEstoque((item["Quantidade"] * -1), item["Codigo"])
            confirmacao = int(
                input("\n\n1. Confirmar operação\n2. Abortar operação\n\nCOMANDO: "))
            while True:
                if confirmacao == 1:
                    caixaRelatorio.write(date.today().strftime(
                        "%d/%m/%Y") + " " + datetime.now().strftime("%H:%M:%S") + "\n\n")
                    openRelat = open("Caixa.txt", 'r').readlines()
                    print(
                        "\nCompra efetuada com sucesso! Retornando ao menu anterior...\n")
                    for item in listaProdutos:
                        caixaRelatorio.write("Código do item: %s || Quantidade vendida: %s\n" % (
                            str(item["Codigo"]), str(item["Quantidade"])))

                    caixaRelatorio.write("\n")

                    resumoCompra = ""
                    valorTotal = 0.0
                    listaProdutos = []
                    caixaRelatorio.close()
                    time.sleep(3)
                    break
                if confirmacao == 2:
                    for item in listaProdutos:
                        if type(item) != float:
                            atualizarEstoque(
                                item["Quantidade"], item["Codigo"])
                    print("\nOperação abortada! Retornando para o menu anterior...\n")
                    resumoCompra = ""
                    valorTotal = 0.0
                    listaProdutos = []
                    time.sleep(3)
                    break
                else:
                    print("Comando inválido! Tente novamente.\n")

        elif caixaOp == 4:
            print("\nRetornando ao menu anterior...\n")
            break

def logisticaMenu():
    acoesLogistica = {"Cadastro": {}, "Exclusao": {},
                      "Reabastecimento": {}, "Retirada": {}}
    while True:
        os.system("clear")
        logisticaRelatorio = open("Logistica.txt", 'a')

        logistica = int(input("""LOGÍSTICA HortiLife\n
    1. Cadastrar produto
    2. Pesquisar produto
    3. Listar estoque
    4. Excluir produto
    5. Atualizar estoque
    6. Voltar ao menu anterior
        
    COMANDO: """))

        if logistica == 1:
            os.system("clear")
            nome = input("Nome do produto: ")
            preco = float(input("Preço: "))
            qtd = int(input("Quantidade: "))
            cod = gerarCodigoProduto()
            marca = input("Marca: ")
            cadastrarProduto(nome, preco, qtd, cod, marca)

            if marca in acoesLogistica["Cadastro"].keys():
                acoesLogistica["Cadastro"][marca].append([nome, cod])
            else:
                acoesLogistica["Cadastro"][marca] = [[nome, cod]]

        if logistica == 2:
            os.system("clear")
            consultarProduto()

        if logistica == 3:
            os.system("clear")
            listarProdutos()

        if logistica == 4:
            os.system("clear")
            produtoRelat = excluirProduto()
            if produtoRelat["Marca"] in acoesLogistica["Exclusao"].keys():
                acoesLogistica["Exclusao"][produtoRelat["Marca"]].append(
                    [produtoRelat["Nome"]])
            else:
                acoesLogistica["Exclusao"][produtoRelat["Marca"]] = [
                    produtoRelat["Nome"]]

        if logistica == 5:
            os.system("clear")
            estoqueLog = atualizarDadosProduto()
            if len(estoqueLog) > 0:
                if estoqueLog[1] < 0:
                    if estoqueLog[0] in acoesLogistica["Retirada"].keys():
                        acoesLogistica["Retirada"][estoqueLog[0]
                                                   ] += estoqueLog[1]
                    else:
                        acoesLogistica["Retirada"][estoqueLog[0]
                                                   ] = estoqueLog[1]
                else:
                    if estoqueLog[0] in acoesLogistica["Reabastecimento"].keys():
                        acoesLogistica["Reabastecimento"][estoqueLog[0]
                                                          ] += estoqueLog[1]
                    else:
                        acoesLogistica["Reabastecimento"][estoqueLog[0]
                                                          ] = estoqueLog[1]

        if logistica == 6:
            logisticaRelatorio.write(date.today().strftime(
                "%d/%m/%Y") + " " + datetime.now().strftime("%H:%M:%S") + "\n\n")
            
            logisticaRelatorio.write("CADASTRO - OPERAÇÕES\n")

            for marca in acoesLogistica["Cadastro"].keys():
                for produto in acoesLogistica["Cadastro"][marca]:
                    logisticaRelatorio.write(
                        f'Nome: {produto[0]:<30} || Código: {produto[1]:<12} || Marca: {marca:<25}\n')

            logisticaRelatorio.write("\n\n")

            logisticaRelatorio.write("EXCLUSÃO - OPERAÇÕES\n")
            for marca in acoesLogistica["Exclusao"].keys():
                nomeProduto = str(acoesLogistica["Exclusao"][marca])
                logisticaRelatorio.write(
                    f'Nome: {nomeProduto:<30} || Marca: {marca:<12}\n')

            logisticaRelatorio.write("\n\n")

            logisticaRelatorio.write("REABASTECIMENTO - OPERAÇÕES\n")
            for cod in acoesLogistica["Reabastecimento"].keys():
                qtdReabastecida = str(acoesLogistica["Reabastecimento"][cod])
                logisticaRelatorio.write(
                    f'Código do produto: {cod:<30}  || Quantidade: {qtdReabastecida:<12}\n')

            logisticaRelatorio.write("\n\n")

            logisticaRelatorio.write("RETIRADA - OPERAÇÕES\n")
            for cod in acoesLogistica["Retirada"].keys():
                qtdRetirada = str(acoesLogistica["Retirada"][cod])
                logisticaRelatorio.write(
                    f'Código do produto: {cod:<30}  || Quantidade: {qtdRetirada:<12}\n')

            logisticaRelatorio.write("\n\n")

            print("\nRetornando ao menu anterior...\n")
            break
        else:
            print("Comando inválido! Tente novamente.")

def funcionariosMenu():
    acoesAdmin = {"Cadastro": {}, "Exclusao": {}}
    while True:
        os.system("clear")
        funcRelatorio = open("Administracao.txt", 'a')
        funcionarios = int(input("""GERÊNCIA HortiLife

        1. Cadastrar novo funcionário
        2. Pesquisar funcionário
        3. Listar funcionários
        4. Excluir funcionário
        5. Alterar dados de funcionário
        6. Voltar ao menu anterior
            
        COMANDO: """))

        if funcionarios == 1:
            os.system("clear")
            nome = input("Nome: ")
            cpf = input("CPF: ")
            isAdmin = False
            while True:
                isAdminInput = int(input("Administrador?\n1. Sim\n2. Não\n\n COMANDO: "))
                if isAdminInput == 1:
                    isAdmin = True
                    break
                elif isAdminInput == 2:
                    isAdmin = False
                    break
                else:
                    print("Comando inválido! Tente novamente")

            codFunc = gerarCodigoFuncionario()

            cadastrarFuncionario(nome, cpf, codFunc, isAdmin)

            acoesAdmin["Cadastro"][nome] = [[cpf, codFunc]]

        elif funcionarios == 2:
            os.system("clear")
            consultarFuncionario()

        elif funcionarios == 3:
            os.system("clear")
            listarFuncionario()

        elif funcionarios == 4:
            os.system("clear")
            funcExcluido = excluirFuncionario()
            acoesAdmin["Exclusao"][funcExcluido["Nome"]] = funcExcluido["CPF"]

        elif funcionarios == 5:
            os.system("clear")
            atualizarDadosFuncionario()

        elif funcionarios == 6:
            funcRelatorio.write(date.today().strftime(
                "%d/%m/%Y") + " " + datetime.now().strftime("%H:%M:%S") + "\n\n")
            
            funcRelatorio.write("CADASTRO - OPERAÇÕES\n")
            
            for funcionario in acoesAdmin["Cadastro"].keys():
                for dado in acoesAdmin["Cadastro"][funcionario]:
                    funcRelatorio.write(
                        f'Nome: {funcionario:<50} || CPF.: {dado[0]:<12} || Código de func.: {dado[1]:<10}\n')

            funcRelatorio.write("\n\n")

            funcRelatorio.write("EXCLUSÃO - OPERAÇÕES\n")
            for funcionario in acoesAdmin["Exclusao"].keys():
                cpfFunc = str(acoesAdmin["Exclusao"][funcionario])
                funcRelatorio.write(
                    f'Nome: {funcionario:<50} || CPF: {cpfFunc:<12}\n')
            print("\nRetornando ao menu anterior...\n")
            time.sleep(2)
            break

        else:
            os.system("clear")
            print("Comando inválido! Tente novamente!")
            time.sleep(1)