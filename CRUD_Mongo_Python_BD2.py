import pymongo
from random import randint


client = pymongo.MongoClient("mongodb+srv://NicolasSilva:nsda1205@sgdbpython-crud-nsda-bd.p1kei.mongodb.net/?retryWrites=true&w=majority")

myDB = client["myDatabase"]

collEstoque = myDB["Estoque"]
collFuncionarios = myDB["Funcionarios"]

# Funções genéricas para CRUD

def atualizarEstoque(qtd, codigo):
    produto = None
    for prod in collEstoque.find({"Codigo":codigo}):
        produto = prod
    
    updateQtd = {"$set" : {"Quantidade":(produto["Quantidade"] + qtd)}}
    collEstoque.update_one({"Quantidade":produto["Quantidade"]},updateQtd)
    print("Estoque do produto Nº %d atualizado com sucesso." % produto["Codigo"])

def acharProduto():
    codProduto = int(input("Insira o código do produto: "))

    queryProduto = None
    for produto in collEstoque.find({"Codigo":codProduto}):
        queryProduto = produto

    return queryProduto

def procurarProduto(codProduto):
    queryProduto = None
    for produto in collEstoque.find({"Codigo":codProduto}):
        queryProduto = produto

    if queryProduto != None:
        return queryProduto
    else:
        print("Produto não encontrado! Tente novamente!")

def gerarCodigo():
    cod = 1000
    checarCodigo = None
    while True:
        for codigo in collEstoque.find({"Codigo":cod}):
            checarCodigo = codigo
        if checarCodigo["Codigo"] == cod:
            cod += 1
        else:
            break
    return cod

#__________________________________________________________________________

#Gerenciamento de caixa/funcionário

def validarUsuario(usuario, senha):
    queryUsuario = None
    for usuario in collEstoque.find({usuario:senha}):
        queryUsuario = usuario
    
    if(queryUsuario != None):
        return queryUsuario
    else:
        print("Usuário e/ou senha incorretos! Tente novamente.")

def retirarProduto(carrinhoCompras, id):
    for produto in carrinhoCompras:
        if(id == produto["Codigo"]):
            atualizarEstoque(produto["Quantidade"], produto["Codigo"])
            carrinhoCompras.remove(produto)
    return carrinhoCompras


#__________________________________________________________________________

# Gerencimaneto de estoque

def cadastrarProduto():
    nome = input("Nome do produto: ")
    preco = float(input("Preço: "))
    qtd = int(input("Quantidade: "))
    cod = GerarCodigo()
    
    cadastro = {"Nome":nome, "Preco":preco, "Quantidade":qtd, "Codigo":cod}
    collEstoque.insert_one(cadastro)

    print("\nUm novo produto foi adicionado com sucesso!\nNome: %s\nPreço: %.2f\nQuantidade: %d\nCódigo do produto: %d\n\n" % (nome, preco, qtd, cod))

def consultarProduto():
    totalProdutos = 0
    for produtos in collEstoque.find():
        totalProdutos += 1
    print("Os dados de %d produtos foram carregados.\n" % totalProdutos)

    resConsulta = acharProduto()
    
    if resConsulta != None:
        print("Estes são os dados referentes ao produto:\nNome: %s\nPreço: %.2f\nQuantidade: %d\nCódigo do produto: %d\n" % (resConsulta["Nome"],
            resConsulta["Preco"], resConsulta["Quantidade"], resConsulta["Codigo"]))
    else:
        print("Produto não encontrado")

def listarProdutos():
    totalProdutos = 0
    for produto in collEstoque.find().sort("Codigo"):
        print("\nNome: %s\nPreço: %.2f\nQuantidade: %d\nCódigo do produto: %d" % (produto["Nome"],
         produto["Preco"], produto["Quantidade"], produto["Codigo"]))
        print("__________________________________________________")
        totalProdutos += 1
    print("Os dados de %d alunos foram carregados.\n" % totalProdutos)

def excluirProduto():
    queryProduto = acharProduto()
    
    if queryProduto != None:
        collEstoque.delete_one(queryProduto)
        print("Produto excluído do sistema com sucesso.")
    else:
        print("Produto não encontrado.")

def atualizarDadosProduto():
    produto = acharProduto()
    dadosParaAtt = int(input("Selecione a opção a ser atualizada:\n1. Nome\n2. Preço\n3. Quantidade"))
    if dadosParaAtt == 1:
        nomeProduto = input("Novo nome do produto: ")
        updateDados = {"$set" : {"Nome":nomeProduto}}
        collEstoque.update_one({"Nome":produto["Nome"]}, updateDados)
    elif dadosParaAtt == 2:
        precoProduto = float(input("Novo preço(Formato:0.00): "))
        updateDados = {"$set" : {"Preco":precoProduto}}
        collEstoque.update_one({"Preco":produto["Preco"]}, updateDados)
    elif dadosParaAtt == 3:
        opcaoQtd = int(input("Selecione a opção de atualização:\n1. Reabastecimento\n2. Retirada\n"))
        qtdProduto = int(input("Quantidade: "))
        if opcaoQtd == 1:
            atualizarEstoque(qtdProduto, produto["Codigo"])
        elif opcaoQtd == 2:
            atualizarEstoque((qtdProduto*-1), produto["Codigo"])
        else:
            print("Comando não reconhecido.")

    else:
        print("Comando não reconhecido. Tente novamente.")

#____________________________________________________________________________

def caixaMenu():
    listaProdutos = []
    valorTotal = 0.0
    while True:
        itemCompra = {"Nome":"", "Quantidade":0, "Preco":0.0, "Codigo":0}
        item = input("Insira o código e a quantidade: ").split(" ")
        if item[0] != "0":
            itemDados = procurarProduto(int(item[0]))
            if itemDados != None:
                itemCompra = {"Nome":itemDados["Nome"], "Quantidade":int(item[1]), "Preco":itemDados["Preco"], "Codigo":itemDados["Codigo"]}
                listaProdutos.append(itemCompra)
                valorTotal += itemDados["Preco"] * int(item[1])
            else:
                print("Código inválido! Tente novamente")
        else:
            break
    listaProdutos.append(valorTotal)
    return listaProdutos

        

def sistemaMenu():
    while True:
        menu = int(input("""SISTEMA MONGO
        1. Operação de caixa
        2. Operação de logística
        3. Sair
        
        COMANDO: """))
        if menu == 1:
            listaDeCompras = caixaMenu()
            valorTotal = 0
            resumoCompra = ""
            for item in listaDeCompras:
                if type(item) != float:
                    atualizarEstoque((item["Quantidade"] * -1), item["Codigo"])
                    resumoCompra += "\n%s\n%d x %.2f = %.2f\n" % (item["Nome"], item["Quantidade"], item["Preco"], (item["Quantidade"] * item["Preco"]))
                    resumoCompra += "__________________________________________________"
                else:
                    valorTotal = item

            print(resumoCompra)
            print("\n\nValor total: %.2f" % valorTotal)

            confirmacao = int(input("\n\n1. Confirmar operação\n2. Abortar operação\n\nCOMANDO: "))
            while True:
                if confirmacao == 1:
                    print("\nCompra efetuada com sucesso! Retornando ao menu anterior...\n")
                    break
                if confirmacao == 2:
                    for item in listaDeCompras:
                        if type(item) != float:
                            atualizarEstoque(item["Quantidade"], item["Codigo"])
                    print("\nOperação abortada! Retornando para o menu anterior...\n")
                    break

        elif menu == 2:
            #logisticaMenu()
            print()
        elif menu == 3:
            #gerarRelatorio()
            print("O relatório foi gerado com sucesso! Desativando sistema...")
        else:
            print("Comando inválido! Tente novamente!")

#____________________________________________________________________________

#Executável

#cadastrarProduto()
#consultarProduto()
#listarProdutos()
#excluirProduto()
#atualizarDadosProduto()
#sistemaMenu()





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
