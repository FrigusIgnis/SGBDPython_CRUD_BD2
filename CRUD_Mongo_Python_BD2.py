import pymongo
import string, random
from random import randint
from datetime import date
from datetime import datetime


client = pymongo.MongoClient(
    "mongodb+srv://NicolasSilva:nsda1205@sgdbpython-crud-nsda-bd.p1kei.mongodb.net/?retryWrites=true&w=majority")

myDB = client["myDatabase"]

collEstoque = myDB["Estoque"]
collFuncionarios = myDB["Funcionarios"]
collRelatorios = myDB["Relatorios"]

# Gerimento de relatórios

def gerarRelatorio(arq1, arq2):
    caixa = open(arq1,'r')
    logistica = open(arq2, 'r')
    relatorio = ""

    relatorio += "OPERAÇÕES DE CAIXA\n"
    for linha in caixa.readlines():
        relatorio += linha

    relatorio += "OPERAÇÕES DE LOGÍSTICA\n"
    for linha in logistica.readlines():
        relatorio += linha

    return relatorio

# __________________________________________________________________________
# Gerenciamento de usuário/funcionário

def procurarFunc(codFunc):
    queryFunc = None
    for funcionario in collFuncionarios.find({"CodFunc": codFunc}):
        queryFunc = funcionario

    if queryFunc != None:
        return queryFunc
    else:
        print("Funcionário não encontrado! Tente novamente!")

def validarUsuario(usuario, senha):
    queryUsuario = None
    for usuario in collFuncionarios.find({usuario:senha}):
        queryUsuario = usuario

    if(queryUsuario != None):
        return queryUsuario
    else:
        print("Usuário e/ou senha incorretos! Tente novamente.")

def cadastrarFuncionario(nome, cpf, codFunc, isAdmin):
    cadastroFunc = {"Nome":nome, "CPF":cpf, "CodFunc":codFunc, codFunc:random.randint(100000, 999999), "Admin?":isAdmin}
    collFuncionarios.insert_one(cadastroFunc)
    print(f'Funcionário adicionado com sucesso!\nNome: {nome}\n{("Usuário: "+ codFunc)}\n{("Senha: %d" % cadastroFunc[codFunc])}\n')

def consultarFuncionario():
    busca = input("Campo de busca: ")
    totalFuncBusca = 0
    listaResultado = []
    for funcionario in collFuncionarios.find({"Nome": {"$regex": "^%s" % busca}}):
        listaResultado.append(funcionario)
        totalFuncBusca += 1
    if(len(listaResultado) == 0):
        print("Nenhum funcionário foi encontrado com este nome.")
    else:
        print("\nOs dados de %d funcionários foram carregados.\n" % totalFuncBusca)

        print(f'{"NOME":^50}||{"CÓDIGO":^15}||')
        print(f'{"":^50}||{"":^15}||')
        for item in listaResultado:
            print(f'{item["Nome"]:^50}||{item["CodFunc"]:^15}||')

def listarFuncionario():
    totalFuncionarios = 0
    for funcionario in collFuncionarios.find().sort("Nome"):
        print("\nNome: %s\nCódigo de funcionário: %s" % (funcionario["Nome"], funcionario["CodFunc"]))
        print("__________________________________________________")
        totalFuncionarios += 1
    print("Os dados de %d funcionários foram carregados.\n" % totalFuncionarios)

def excluirFuncionario():
    cod = input("Código de funcionário: ")
    queryFunc = procurarFunc(cod)

    if queryFunc != None:
        collFuncionarios.delete_one(queryFunc)
        print("Funcionário excluído do sistema com sucesso.")

def atualizarDadosFuncionario():
    cod = input("Código de funcionário: ")
    funcionario = procurarFunc(cod)
    dadosParaAtt = int(
        input("Selecione a opção a ser atualizada:\n1. Nome\n2. Senha\n\nCOMANDO: "))
    if dadosParaAtt == 1:
        nomeFunc = input("Nome: ")
        updateDados = {"$set": {"Nome": nomeFunc}}
        collFuncionarios.update_one({"Nome": funcionario["Nome"]}, updateDados)
    elif dadosParaAtt == 2:
        print("Gerando nova senha...\n")
        novaSenha = random.randint(100000, 999999)
        updateDados = {"$set": {cod:novaSenha}}
        collFuncionarios.update_one({cod:funcionario[cod]}, updateDados)
        print("\nNova senha para o usuário %s: %d\n" % (cod,novaSenha))

def gerarCodigoFuncionario():
    cod = ""
    countLetras = 0
    countNumero = 0
    checarCodigo = None

    while True:
        while countLetras < 3:
            cod += random.choice(string.ascii_lowercase)
            countLetras += 1
        while countNumero < 4:
            cod += str(random.randint(0, 9))
            countNumero += 1
        for codigo in collFuncionarios.find({"CodFunc": cod}):
            checarCodigo = codigo
        if checarCodigo != None:
            cod = ""
        else:
            break
    
    return cod
        
# __________________________________________________________________________

# Gerencimaneto de estoque

def atualizarEstoque(qtd, codigo):
    produto = None
    for prod in collEstoque.find({"Codigo": codigo}):
        produto = prod

    updateQtd = {"$set": {"Quantidade": (produto["Quantidade"] + qtd)}}
    collEstoque.update_one({"Quantidade": produto["Quantidade"]}, updateQtd)
    print("Estoque do produto Nº %d atualizado com sucesso." %
          produto["Codigo"])

def procurarProduto(codProduto):
    queryProduto = None
    for produto in collEstoque.find({"Codigo": codProduto}):
        queryProduto = produto

    if queryProduto != None:
        return queryProduto
    else:
        print("Produto não encontrado! Tente novamente!")

def gerarCodigoProduto():
    cod = 1000
    checarCodigo = None
    while True:
        for codigo in collEstoque.find({"Codigo": cod}):
            checarCodigo = codigo
        if checarCodigo["Codigo"] == cod:
            cod += 1
        else:
            break
    return cod

def cadastrarProduto(nome, preco, qtd, cod):
    cadastroProduto = {"Nome": nome, "Preco": preco, "Quantidade": qtd, "Codigo": cod}
    collEstoque.insert_one(cadastroProduto)
    print("\nUm novo produto foi adicionado com sucesso!\nNome: %s\nPreço: %.2f\nQuantidade: %d\nCódigo do produto: %d\n\n" % (
        nome, preco, qtd, cod))

def consultarProduto():
    busca = input("Campo de busca: ")
    totalProdutosBusca = 0
    listaResultado = []
    for produtos in collEstoque.find({"Nome": {"$regex": "^%s" % busca}}):
        listaResultado.append(produtos)
        totalProdutosBusca += 1
    if(len(listaResultado) == 0):
        print("Nenhum produto foi encontrado com este nome.")
    else:
        print("\nOs dados de %d produtos foram carregados.\n" % totalProdutosBusca)

        print(f'{"PRODUTO":^25}||{"CÓDIGO":^10}||{"QUANTIDADE":^12}||{"PREÇO":^10}')
        print(f'{"":^25}||{"":^10}||{"":^12}||{"":^10}')
        for item in listaResultado:
            print(f'{item["Nome"]:^25}||{item["Codigo"]:^10}||{item["Quantidade"]:^12}||{item["Preco"]:^10}')

def listarProdutos():
    totalProdutos = 0
    for produto in collEstoque.find().sort("Codigo"):
        print("\nNome: %s\nPreço: %.2f\nQuantidade: %d\nCódigo do produto: %d" % (produto["Nome"], produto["Preco"], 
         produto["Quantidade"], produto["Codigo"]))
        print("__________________________________________________")
        totalProdutos += 1
    print("Os dados de %d produtos foram carregados.\n" % totalProdutos)

def excluirProduto():
    cod = int(input("Código do produto: "))
    queryProduto = procurarProduto(cod)

    if queryProduto != None:
        collEstoque.delete_one(queryProduto)
        print("Produto excluído do sistema com sucesso.")

def atualizarDadosProduto():
    cod = int(input("Código do produto: "))
    produto = procurarProduto(cod)
    dadosParaAtt = int(
        input("Selecione a opção a ser atualizada:\n1. Nome\n2. Preço\n3. Quantidade"))
    if dadosParaAtt == 1:
        nomeProduto = input("Novo nome do produto: ")
        updateDados = {"$set": {"Nome": nomeProduto}}
        collEstoque.update_one({"Nome": produto["Nome"]}, updateDados)
    elif dadosParaAtt == 2:
        precoProduto = float(input("Novo preço(Formato:0.00): "))
        updateDados = {"$set": {"Preco": precoProduto}}
        collEstoque.update_one({"Preco": produto["Preco"]}, updateDados)
    elif dadosParaAtt == 3:
        opcaoQtd = int(
            input("Selecione a opção de atualização:\n1. Reabastecimento\n2. Retirada\n"))
        qtdProduto = int(input("Quantidade: "))
        if opcaoQtd == 1:
            atualizarEstoque(qtdProduto, produto["Codigo"])
        elif opcaoQtd == 2:
            atualizarEstoque((qtdProduto*-1), produto["Codigo"])
        else:
            print("Comando não reconhecido.")

    else:
        print("Comando não reconhecido. Tente novamente.")

# ____________________________________________________________________________

# Gerenciamento de caixa

def atualizarResumoCompra(resumoCompra, listaProdutos):
    resumoCompra = ""
    for item in listaProdutos:
        resumoCompra += f'\n{item["Nome"]:<25}{item["Codigo"]:>11}\n{item["Quantidade"]} x {item["Preco"]:<6} = {(item["Quantidade"] * item["Preco"]):>24.2f}\n'
        resumoCompra += "__________________________________________________"
    return resumoCompra

def atualizarValorTotal(valorTotal, listaProdutos):
    valorTotal = 0.0
    for item in listaProdutos:
        valorTotal += item["Preco"] * item["Quantidade"]
    return valorTotal

def retirarProduto(carrinhoCompras, id):
    for produto in carrinhoCompras:
        if(id == produto["Codigo"]):
            carrinhoCompras.remove(produto)
            print("Produto removido com sucesso!\n")
    return carrinhoCompras

# __________________________________________________________________________

#Interfaces do sistema

def caixaMenu():
    listaProdutos = []
    valorTotal = 0.0
    resumoCompra = ""

    while True:
        caixaRelatorio = open("Caixa.txt",'a')
        resumoCompra = atualizarResumoCompra(resumoCompra, listaProdutos)
        valorTotal = atualizarValorTotal(valorTotal, listaProdutos)
        caixaOp = int(input("""CAIXA HortiLife\n\nCarrinho de compras atual\n%s
        \n
        Valor Total: %.2f
        \n

        1. Adicionar itens
        2. Retirar item
        3. Fechar compra
        4. Sair
        
        COMANDO: """ % (resumoCompra, valorTotal)))

        if caixaOp == 1:
            while True:
                itemCompra = {"Nome": "", "Quantidade": 0, "Preco": 0.0, "Codigo": 0}
                item = input("Insira o código e a quantidade: ").split(" ")
                if item[0] != "0":
                    check = False
                    itemDados = procurarProduto(int(item[0]))
                    if itemDados != None:
                        itemCompra = {"Nome": itemDados["Nome"], "Quantidade": int(
                            item[1]), "Preco": itemDados["Preco"], "Codigo": itemDados["Codigo"]}
                        for produtoCheck in listaProdutos:
                            if itemCompra["Codigo"] == produtoCheck["Codigo"]:
                                listaProdutos[listaProdutos.index(produtoCheck)]["Quantidade"] += itemCompra["Quantidade"]
                                check = True
                                break
                        if check == False:
                            listaProdutos.append(itemCompra)
                    else:
                        print("Código inválido! Tente novamente\n")
                else:
                    break

        elif caixaOp == 2:
            retirarID = int(input("Código do produto: "))
            listaProdutos = retirarProduto(listaProdutos, retirarID)
        
        elif caixaOp == 3:
            for item in listaProdutos:
                    atualizarEstoque((item["Quantidade"] * -1), item["Codigo"])
            confirmacao = int(
                input("\n\n1. Confirmar operação\n2. Abortar operação\n\nCOMANDO: "))
            while True:
                if confirmacao == 1:
                    caixaRelatorio.write(date.today().strftime("%d/%m/%Y") + " " + datetime.now().strftime("%H:%M:%S") +"\n\n")
                    openRelat = open("Caixa.txt",'r').readlines()
                    print("\nCompra efetuada com sucesso! Retornando ao menu anterior...\n")
                    for item in listaProdutos:
                        caixaRelatorio.write("Código do item: %s || Quantidade vendida: %s\n" % (str(item["Codigo"]), str(item["Quantidade"])))

                    caixaRelatorio.write("\n")
                    resumoCompra = ""

                    valorTotal = 0.0
                    listaProdutos = []
                    caixaRelatorio.close()
                    break
                if confirmacao == 2:
                    for item in listaProdutos:
                        if type(item) != float:
                            atualizarEstoque(item["Quantidade"], item["Codigo"])
                    print("\nOperação abortada! Retornando para o menu anterior...\n")
                    resumoCompra = ""
                    valorTotal = 0.0
                    listaProdutos = []
                    break
                else:
                    print("Comando inválido! Tente novamente.\n")
        
        elif caixaOp == 4:
            print("\nRetornando ao menu anterior...\n")
            break

def logisticaMenu():
    acoesLogistica = []
    while True:
        logisticaRelatorio = open("Logistica.txt",'a') #Parada
        logistica = int(input("""LOGÍSTICA HortiLife\n\n
        1. Cadastrar produto
        2. Pesquisar produto
        3. Listar estoque
        4. Excluir produto
        5. Atualizar estoque
        6. Voltar ao menu anterior"""))

        if logistica == 1:
            nome = input("Nome do produto: ")
            preco = float(input("Preço: "))
            qtd = int(input("Quantidade: "))
            cod = GerarCodigo()
            cadastrarProduto(nome, preco, qtd, cod)

        if logistica == 2:
            consultarProduto()

        if logistica == 3:
            listarProdutos()

        if logistica == 4:
            excluirProduto()

        if logistica == 5:
            atualizarDadosProduto()

        if logistica == 6:
            print("\nRetornando ao menu anterior...\n")
            break

def funcionariosMenu():
    while True:
        funcionarios = int(input("""GERÊNCIA HortiLife
        1. Cadastrar novo funcionário
        2. Pesquisar funcionário
        3. Alterar dados de funcionário
        4. Excluir funcionário
        5. Voltar ao menu anterior
        
        COMANDO: """))

        if funcionarios == 1:
            nome = input("Nome: ")
            cpf = input("CPF: ")
            isAdmin = False
            while True:
                isAdminInput = int(input("Administrador?\n1. Sim\n2. Não"))
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

        if funcionarios == 2:
            consultarFuncionario()

        if funcionarios == 3:
            listarFuncionario()

        if funcionarios == 4:
            excluirFuncionario()

        if funcionarios == 5:
            atualizarDadosFuncionario()

        if funcionarios == 6:
            print("\nRetornando ao menu anterior...\n")
            break

def adminMenu(nomeUsuario):
    nomeRelatorio = nomeUsuario + "_" + date.today().strftime("%d/%m/%Y") + "_" + datetime.now().strftime("%H.%M.%S") +"\n\n"
    relatorioArq = open(nomeRelatorio, 'w')
    relatorioArq.write("Horário de abertura: " + date.today().strftime("%d/%m/%Y") + " " + datetime.now().strftime("%H:%M:%S") +"\n\n")
    while True:
        admin = int(input("""ADMINISTRAÇÃO HortiLife
    
        1. Gerenciar funcionários
        2. Gerenciar logística
        3. Gerenciar caixa
        4. Carregar relatórios
        5. Sair
    
        COMANDO: """))

        if admin == 1:
            funcionariosMenu()

        elif admin == 2:
            logisticaMenu()

        elif admin == 3:
            caixaMenu()
        
        elif admin == 4:
            carregarRelatorio()

        elif admin == 5:
            relatorioFinal = gerarRelatorio("Caixa.txt", "Logistica.txt")
            relatorioArq.write("\n" + relatorioFinal + "\n")
            relatorioArq.write("Horário de fechamento: " + date.today().strftime("%d/%m/%Y") + " " + datetime.now().strftime("%H:%M:%S") +"\n\n")
            relatorioArq.close()
            break

        else:
            print("Comando inválido! Tente novamente!")

def sistemaMenu(nomeUsuario):
    nomeRelatorio = nomeUsuario + "_" + date.today().strftime("%d/%m/%Y") + "_" + datetime.now().strftime("%H.%M.%S") +"\n\n"
    relatorioArq = open(nomeRelatorio, 'w')
    relatorioArq.write("Horário de abertura: " + date.today().strftime("%d/%m/%Y") + " " + datetime.now().strftime("%H:%M:%S") +"\n\n")
    while True:
        menu = int(input("""SISTEMA HortiLife
        1. Operação de caixa
        2. Operação de logística
        3. Sair
        
        COMANDO: """))
        if menu == 1:
            caixaMenu()

        elif menu == 2:
            logisticaMenu()
            print()
        elif menu == 3:
            relatorioFinal = gerarRelatorio("Caixa.txt", "Logistica.txt")
            relatorioArq.write("\n" + relatorioFinal + "\n")
            relatorioArq.write("Horário de fechamento: " + date.today().strftime("%d/%m/%Y") + " " + datetime.now().strftime("%H:%M:%S") +"\n\n")
            relatorioArq.close()
            print("O relatório foi gerado com sucesso! Desativando sistema...")
            break
        else:
            print("Comando inválido! Tente novamente!")

# ____________________________________________________________________________

# Executável

"""
while True:
    print("Bem vindo! Digite seu login e senha para continuar\n")
    login = input("Login: ")
    senha = int(input("Senha: "))

    checkUsuario = validarUsuario(login, senha)
    if checkUsuario != None and checkUsuario["Admin?"] != True:
        sistemaMenu(checkUsuario["Nome"])
    elif checkUsuario != None and checkUsuario["Admin?"] == True:
        adminMenu(checkUsuario["Nome"])
    else:
        break
"""

"""
inserirProdutos = [
{"Nome":"Banana prata", "Preco":3.09, "Quantidade": 200, "Codigo":gerarCodigoProduto()},
{"Nome":"Morango", "Preco":19.99, "Quantidade": 200, "Codigo":gerarCodigoProduto()},
{"Nome":"Maçã verde", "Preco":14.99, "Quantidade": 200, "Codigo":gerarCodigoProduto()},
{"Nome":"Maçã vermelha", "Preco":5.99, "Quantidade": 200, "Codigo":gerarCodigoProduto()},
{"Nome":"Uva verde", "Preco":10.99, "Quantidade": 200, "Codigo":gerarCodigoProduto()},
{"Nome":"Uva roxa", "Preco":6.89, "Quantidade": 200, "Codigo":gerarCodigoProduto()},
{"Nome":"Melão verde", "Preco":4.99, "Quantidade": 200, "Codigo":gerarCodigoProduto()},
{"Nome":"Melância vermelha", "Preco":4.59, "Quantidade": 200, "Codigo":gerarCodigoProduto()},
{"Nome":"Melância amarela", "Preco":3.59, "Quantidade": 200, "Codigo":gerarCodigoProduto()},
{"Nome":"Kiwi", "Preco":19.89, "Quantidade": 200, "Codigo":gerarCodigoProduto()},
{"Nome":"Mamão Papaya", "Preco":6.49, "Quantidade": 200, "Codigo":gerarCodigoProduto()},
{"Nome":"Quiabo", "Preco":5.69, "Quantidade": 200, "Codigo":gerarCodigoProduto()},
{"Nome":"Coentro", "Preco":4.89, "Quantidade": 200, "Codigo":gerarCodigoProduto()},
{"Nome":"Salsa", "Preco":3.39, "Quantidade": 200, "Codigo":gerarCodigoProduto()},
{"Nome":"Abóbora", "Preco":2.29, "Quantidade": 200, "Codigo":gerarCodigoProduto()},
{"Nome":"Tomate", "Preco":3.59, "Quantidade": 200, "Codigo":gerarCodigoProduto()},
{"Nome":"Cebola", "Preco":2.49, "Quantidade": 200, "Codigo":gerarCodigoProduto()},
{"Nome":"Alho", "Preco":17.19, "Quantidade": 200, "Codigo":gerarCodigoProduto()},
{"Nome":"Couve", "Preco":6.99, "Quantidade": 200, "Codigo":gerarCodigoProduto()},
{"Nome":"Couve-flor", "Preco":5.19, "Quantidade": 200, "Codigo":gerarCodigoProduto()},
{"Nome":"Beterraba", "Preco":2.29, "Quantidade": 200, "Codigo":gerarCodigoProduto()},
{"Nome":"Cogumelo shitake", "Preco":48.59, "Quantidade": 200, "Codigo":gerarCodigoProduto()},
{"Nome":"Cogumelo champignon", "Preco":46.09, "Quantidade": 200, "Codigo":gerarCodigoProduto()},
{"Nome":"Cogumelo shimeji", "Preco":13.89, "Quantidade": 200, "Codigo":gerarCodigoProduto()}
]

collEstoque.insert_many(inserirProdutos)"""