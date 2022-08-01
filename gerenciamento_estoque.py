import pymongo
import os
import time

client = pymongo.MongoClient(
    "mongodb+srv://NicolasSilva:nsda1205@sgdbpython-crud-nsda-bd.p1kei.mongodb.net/?retryWrites=true&w=majority")

myDB = client["myDatabase"]
collPatrocinadores = myDB["Patrocinadores"]
collEstoque = myDB["Estoque"]

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

def attPatrocinadorAdd(produto):
    for patrocinador in collPatrocinadores.find():
        if produto["Marca"] == patrocinador["Marca"]:
            produtosRegistrados = patrocinador["Produtos"]
            produtosRegistrados.append(produto["Nome"])
            updateProdutosPatro = {"$set": {"Produtos": produtosRegistrados}}
            collPatrocinadores.update_one(
                {"Marca": produto["Marca"]}, updateProdutosPatro)
            break

def attPatrocinadorRem(produto):
    for patrocinador in collPatrocinadores.find():
        if produto["Marca"] == patrocinador["Marca"] and produto["Nome"] in patrocinador["Produtos"]:
            produtosRegistrados = patrocinador["Produtos"]
            produtosRegistrados.remove(produto["Nome"])
            updateProdutosPatro = {"$set": {"Produtos": produtosRegistrados}}
            collPatrocinadores.update_one(
                {"Marca": produto["Marca"]}, updateProdutosPatro)
            break

def cadastrarProduto(nome, preco, qtd, cod, marca):
    os.system("clear")
    cadastroProduto = {"Nome": nome, "Preco": preco, "Quantidade": qtd, "Codigo": cod, "Marca": marca}
    collEstoque.insert_one(cadastroProduto)
    
    print("\nUm novo produto foi adicionado com sucesso!\nNome: %s\nPreço: %.2f\nQuantidade: %d\nCódigo do produto: %d\nMarca: %s\n\n" % (
        nome, preco, qtd, cod, marca))

    checkMarca = False
    for patrocinador in collPatrocinadores.find():
        if marca in patrocinador["Marca"]:
            attPatrocinadorAdd(cadastroProduto)
            checkMarca = True

    if checkMarca == False:
        cadastroPatrocinador = {"Marca": marca, "Produtos": [nome]}
        collPatrocinadores.insert_one(cadastroPatrocinador)

    input()

def consultarProduto():
    os.system("clear")
    busca = input("Campo de busca: ")
    totalProdutosBusca = 0
    listaResultado = []
    for produtos in collEstoque.find({"Nome": {"$regex": "^%s" % busca}}):
        listaResultado.append(produtos)
        totalProdutosBusca += 1
    if(len(listaResultado) == 0):
        print("Nenhum produto foi encontrado com este nome.")
    else:
        print("\nOs dados de %d produtos foram carregados.\n" %
              totalProdutosBusca)

        print(
            f'{"PRODUTO":^25}||{"CÓDIGO":^10}||{"QUANTIDADE":^12}||{"PREÇO/KG":^12}||{"MARCA":^15}')
        print(f'{"":^25}||{"":^10}||{"":^12}||{"":^12}||{"":^15}')
        for item in listaResultado:
            print(
                f'{item["Nome"]:^25}||{item["Codigo"]:^10}||{item["Quantidade"]:^12}||{item["Preco"]:^12}||{item["Marca"]:^15}')
        print("\n")
        input()

def listarProdutos():
    os.system("clear")
    joinPatrocinadores = collPatrocinadores.aggregate([
        {
            '$lookup': {
                'from': "Estoque",
                'localField': "Marca",
                'foreignField': "Marca",
                'as': 'produtoPatrocinador'
            }
        }
    ])

    for marca in joinPatrocinadores:
        id = 1
        print(f'{marca["Marca"]:<15}')
        print("________________________________________________\n")
        for produto in marca["produtoPatrocinador"]:
            print(
                f'{id:<2} | Nome: {produto["Nome"]:<20} || Código do produto: {produto["Codigo"]:<6} || Preço: {produto["Preco"]:<10}')
            id += 1

        print("________________________________________________\n")

    input()

def excluirProduto():
    os.system("clear")
    cod = int(input("Código do produto: "))
    queryProduto = procurarProduto(cod)
    relatProduto = queryProduto

    if queryProduto != None:
        attPatrocinadorRem(queryProduto)
        collEstoque.delete_one(queryProduto)
        print("Produto excluído do sistema com sucesso.")
        time.sleep(3)

    return relatProduto

def atualizarDadosProduto():
    os.system("clear")
    estoqueAtt = []
    cod = int(input("Código do produto: "))
    produto = procurarProduto(cod)
    os.system("clear")
    dadosParaAtt = int(
        input("Selecione a opção a ser atualizada:\n1. Nome\n2. Preço\n3. Quantidade\n\nCOMANDO: "))
    if dadosParaAtt == 1:
        os.system("clear")
        nomeProduto = input("Novo nome do produto: ")
        updateDados = {"$set": {"Nome": nomeProduto}}
        collEstoque.update_one({"Nome": produto["Nome"]}, updateDados)
    elif dadosParaAtt == 2:
        os.system("clear")
        precoProduto = float(input("Novo preço(Formato:0.00): "))
        updateDados = {"$set": {"Preco": precoProduto}}
        collEstoque.update_one({"Preco": produto["Preco"]}, updateDados)
    elif dadosParaAtt == 3:
        os.system("clear")
        opcaoQtd = int(
            input("Selecione a opção de atualização:\n1. Reabastecimento\n2. Retirada\n\n COMANDO: "))
        qtdProduto = int(input("Quantidade: "))
        if opcaoQtd == 1:
            atualizarEstoque(qtdProduto, produto["Codigo"])
            estoqueAtt = [cod, qtdProduto]
            return estoqueAtt
        elif opcaoQtd == 2:
            atualizarEstoque((qtdProduto*-1), produto["Codigo"])
            estoqueAtt = [cod, (qtdProduto*-1)]
            return estoqueAtt
        else:
            print("Comando não reconhecido.")

    else:
        print("Comando não reconhecido. Tente novamente.")

    return estoqueAtt