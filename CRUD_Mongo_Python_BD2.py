import pymongo
from random import randint


client = pymongo.MongoClient(
    "mongodb+srv://NicolasSilva:nsda1205@sgdbpython-crud-nsda-bd.p1kei.mongodb.net/?retryWrites=true&w=majority")

myDB = client["myDatabase"]

collEstoque = myDB["Estoque"]
collFuncionarios = myDB["Funcionarios"]

# Funções genéricas para CRUD de logística


def atualizarEstoque(qtd, codigo):
    produto = None
    for prod in collEstoque.find({"Codigo": codigo}):
        produto = prod

    updateQtd = {"$set": {"Quantidade": (produto["Quantidade"] + qtd)}}
    collEstoque.update_one({"Quantidade": produto["Quantidade"]}, updateQtd)
    print("Estoque do produto Nº %d atualizado com sucesso." %
          produto["Codigo"])

#def 

def procurarProduto(codProduto):
    queryProduto = None
    for produto in collEstoque.find({"Codigo": codProduto}):
        queryProduto = produto

    if queryProduto != None:
        return queryProduto
    else:
        print("Produto não encontrado! Tente novamente!")

def gerarCodigo():
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

# __________________________________________________________________________

# Gerenciamento de caixa/funcionário

def validarUsuario(usuario, senha):
    queryUsuario = None
    for usuario in collFuncionarios.find({usuario: senha}):
        queryUsuario = usuario

    if(queryUsuario != None):
        return queryUsuario
    else:
        print("Usuário e/ou senha incorretos! Tente novamente.")

def atualizarResumoCompra(resumoCompra, listaProdutos):
    resumoCompra = ""
    for item in listaProdutos:
        resumoCompra += "\n%s     Código: %s\n%d x %.2f = %.2f\n" % (
                        item["Nome"], item["Codigo"], item["Quantidade"], item["Preco"], (item["Quantidade"] * item["Preco"]))
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

# Gerencimaneto de estoque

def cadastrarProduto(nome, preco, qtd, cod):
    cadastro = {"Nome": nome, "Preco": preco, "Quantidade": qtd, "Codigo": cod}
    collEstoque.insert_one(cadastro)
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
    else:
        print("Produto não encontrado.")

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

#Interfaces do sistema

def caixaMenu():
    listaProdutos = []
    valorTotal = 0.0
    resumoCompra = ""

    while True:
        resumoCompra = atualizarResumoCompra(resumoCompra, listaProdutos)
        valorTotal = atualizarValorTotal(valorTotal, listaProdutos)
        caixaOp = int(input("""CAIXA MongoDB\n\nCarrinho de compras atual\n%s
        \n
        Valor Total: %.2f
        \n

        1. Adicionar itens
        2. Retirar item
        3. Fechar compra
        4. Cancelar operação
        
        COMANDO: """ % (resumoCompra, valorTotal)))

        if caixaOp == 1:
            while True:
                itemCompra = {"Nome": "", "Quantidade": 0, "Preco": 0.0, "Codigo": 0}
                item = input("Insira o código e a quantidade: ").split(" ")
                if item[0] != "0":
                    itemDados = procurarProduto(int(item[0]))
                    if itemDados != None:
                        itemCompra = {"Nome": itemDados["Nome"], "Quantidade": int(
                            item[1]), "Preco": itemDados["Preco"], "Codigo": itemDados["Codigo"]}
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
                    print("\nCompra efetuada com sucesso! Retornando ao menu anterior...\n")
                    resumoCompra = ""
                    valorTotal = 0.0
                    listaProdutos = []
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
    while True:
        logistica = int(input("""LOGÍSTICA MongoDB\n\n
        1. Cadastrar produto
        2. Pesquisar produto
        3. Listar estoque
        4. Excluir produto
        5. Atualizar estoque
        6. Sair"""))

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

def sistemaMenu():
    while True:
        menu = int(input("""SISTEMA MONGO
        1. Operação de caixa
        2. Operação de logística
        3. Sair
        
        COMANDO: """))
        if menu == 1:
            caixaMenu()

        elif menu == 2:
            #logisticaMenu()
            print()
        elif menu == 3:
            #gerarRelatorio()
            print("O relatório foi gerado com sucesso! Desativando sistema...")
            break
        else:
            print("Comando inválido! Tente novamente!")

# ____________________________________________________________________________

# Executável

consultarProduto()
"""
while True:
    print("Bem vindo! Digite seu login e senha para continuar\n")
    login = input("Login: ")
    senha = input("Senha: ")

    checkUsuario = validarUsuario(login, senha)
    if checkUsuario != None:
        sistemaMenu()
    else:
        break

"""
"""
inserirProdutos = [
{"Nome":"Banana prata", "Preco":3.09, "Quantidade": 200, "Codigo":gerarCodigo()},
{"Nome":"Morango", "Preco":19.99, "Quantidade": 200, "Codigo":gerarCodigo()},
{"Nome":"Maçã verde", "Preco":14.99, "Quantidade": 200, "Codigo":gerarCodigo()},
{"Nome":"Maçã vermelha", "Preco":5.99, "Quantidade": 200, "Codigo":gerarCodigo()},
{"Nome":"Uva verde", "Preco":10.99, "Quantidade": 200, "Codigo":gerarCodigo()},
{"Nome":"Uva roxa", "Preco":6.89, "Quantidade": 200, "Codigo":gerarCodigo()},
{"Nome":"Melão verde", "Preco":4.99, "Quantidade": 200, "Codigo":gerarCodigo()},
{"Nome":"Melância vermelha", "Preco":4.59, "Quantidade": 200, "Codigo":gerarCodigo()},
{"Nome":"Melância amarela", "Preco":3.59, "Quantidade": 200, "Codigo":gerarCodigo()},
{"Nome":"Kiwi", "Preco":19.89, "Quantidade": 200, "Codigo":gerarCodigo()},
{"Nome":"Mamão Papaya", "Preco":6.49, "Quantidade": 200, "Codigo":gerarCodigo()},
{"Nome":"Quiabo", "Preco":5.69, "Quantidade": 200, "Codigo":gerarCodigo()},
{"Nome":"Coentro", "Preco":4.89, "Quantidade": 200, "Codigo":gerarCodigo()},
{"Nome":"Salsa", "Preco":3.39, "Quantidade": 200, "Codigo":gerarCodigo()},
{"Nome":"Abóbora", "Preco":2.29, "Quantidade": 200, "Codigo":gerarCodigo()},
{"Nome":"Tomate", "Preco":3.59, "Quantidade": 200, "Codigo":gerarCodigo()},
{"Nome":"Cebola", "Preco":2.49, "Quantidade": 200, "Codigo":gerarCodigo()},
{"Nome":"Alho", "Preco":17.19, "Quantidade": 200, "Codigo":gerarCodigo()},
{"Nome":"Couve", "Preco":6.99, "Quantidade": 200, "Codigo":gerarCodigo()},
{"Nome":"Couve-flor", "Preco":5.19, "Quantidade": 200, "Codigo":gerarCodigo()},
{"Nome":"Beterraba", "Preco":2.29, "Quantidade": 200, "Codigo":gerarCodigo()},
{"Nome":"Cogumelo shitake", "Preco":48.59, "Quantidade": 200, "Codigo":gerarCodigo()},
{"Nome":"Cogumelo champignon", "Preco":46.09, "Quantidade": 200, "Codigo":gerarCodigo()},
{"Nome":"Cogumelo shimeji", "Preco":13.89, "Quantidade": 200, "Codigo":gerarCodigo()}
]

collEstoque.insert_many(inserirProdutos)"""
"""
inserirFuncionarios = [
    {"jks2145":"051220", "Nome":"Morgana Oliveira"},
    {"nsa1205":"120520", "Nome":"Nicolas Silva de Araújo"},
    {"jus2265":"200512", "Nome":"João Carlos Muniz"},
    {"hki1234":"123456", "Nome":"Giovanna Lorezzi"}
]

collFuncionarios.insert_many(inserirFuncionarios)"""
