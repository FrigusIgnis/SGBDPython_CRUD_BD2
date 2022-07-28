import pymongo
import os
import string, random
from random import randint
from datetime import date
from datetime import datetime
import time


client = pymongo.MongoClient("mongodb+srv://NicolasSilva:nsda1205@sgdbpython-crud-nsda-bd.p1kei.mongodb.net/?retryWrites=true&w=majority")

myDB = client["myDatabase"]

collEstoque = myDB["Estoque"]
collFuncionarios = myDB["Funcionarios"]
collPatrocinadores = myDB["Patrocinadores"]


# Gerimento de relatórios

def gerarRelatorio(arq1, arq2):
    caixa = open(arq1,'r')
    logistica = open(arq2, 'r')
    relatorio = ""

    relatorio += "--- OPERAÇÕES DE CAIXA\n"
    for linha in caixa.readlines():
        relatorio += linha

    relatorio += "\n"

    relatorio += "--- OPERAÇÕES DE LOGÍSTICA\n"
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
    input()

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
            print(f'{item["Nome"]:<50}||{item["CodFunc"]:<15}||')
        input()

def listarFuncionario():
    totalFuncionarios = 0
    for funcionario in collFuncionarios.find().sort("Nome"):
        print("\nNome: %s\nCódigo de funcionário: %s" % (funcionario["Nome"], funcionario["CodFunc"]))
        print("__________________________________________________")
        totalFuncionarios += 1
    print("Os dados de %d funcionários foram carregados.\n" % totalFuncionarios)
    input()

def excluirFuncionario():
    cod = input("Código de funcionário: ")
    queryFunc = procurarFunc(cod)

    if queryFunc != None:
        collFuncionarios.delete_one(queryFunc)
        print("Funcionário excluído do sistema com sucesso.")
        time.sleep(2)

def atualizarDadosFuncionario():
    os.system("clear")
    cod = input("Código de funcionário: ")
    funcionario = procurarFunc(cod)
    os.system("clear")
    dadosParaAtt = int(
        input("Selecione a opção a ser atualizada:\n1. Nome\n2. Senha\n\nCOMANDO: "))
    if dadosParaAtt == 1:
        os.system("clear")
        nomeFunc = input("Nome: ")
        updateDados = {"$set": {"Nome": nomeFunc}}
        collFuncionarios.update_one({"Nome": funcionario["Nome"]}, updateDados)
    elif dadosParaAtt == 2:
        os.system("clear")
        print("Gerando nova senha...\n")
        novaSenha = random.randint(100000, 999999)
        updateDados = {"$set": {cod:novaSenha}}
        collFuncionarios.update_one({cod:funcionario[cod]}, updateDados)
        print("\nNova senha para o usuário %s: %d\n" % (cod,novaSenha))
        input()

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
    time.sleep(2)

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
            updateProdutosPatro = {"$set":{"Produtos":produtosRegistrados}}
            collPatrocinadores.update_one({"Marca":produto["Marca"]}, updateProdutosPatro)
            break

def attPatrocinadorRem(produto):
    for patrocinador in collPatrocinadores.find():
        if produto["Marca"] == patrocinador["Marca"] and produto["Nome"] in patrocinador["Produtos"]:
            produtosRegistrados = patrocinador["Produtos"]
            produtosRegistrados.remove(produto["Nome"])
            updateProdutosPatro = {"$set":{"Produtos":produtosRegistrados}}
            collPatrocinadores.update_one({"Marca":produto["Marca"]}, updateProdutosPatro)
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
        cadastroPatrocinador = {"Marca":marca, "Produtos":[nome]}
        collPatrocinadores.insert_one(cadastroPatrocinador)
    
    time.sleep(2)

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
        print("\nOs dados de %d produtos foram carregados.\n" % totalProdutosBusca)

        print(f'{"PRODUTO":^25}||{"CÓDIGO":^10}||{"QUANTIDADE":^12}||{"PREÇO/KG":^12}||{"MARCA":^15}')
        print(f'{"":^25}||{"":^10}||{"":^12}||{"":^12}||{"":^15}')
        for item in listaResultado:
            print(f'{item["Nome"]:^25}||{item["Codigo"]:^10}||{item["Quantidade"]:^12}||{item["Preco"]:^12}||{item["Marca"]:^15}')
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
            print(f'{id:<2} | Nome: {produto["Nome"]:<20} || Código do produto: {produto["Codigo"]:<6} || Preço: {produto["Preco"]:<10}')
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
        time.sleep(2)

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
            estoqueAtt = [cod,(qtdProduto*-1)]
            return estoqueAtt
        else:
            print("Comando não reconhecido.")

    else:
        print("Comando não reconhecido. Tente novamente.")

# ____________________________________________________________________________

# Gerenciamento de caixa

def atualizarResumoCompra(resumoCompra, listaProdutos):
    resumoCompra = ""
    for item in listaProdutos:
        resumoCompra += f'\n{(item["Nome"] + " " + item["Marca"]):<25}{item["Codigo"]:>11}\n{item["Quantidade"]} x {item["Preco"]:<6} = {(item["Quantidade"] * item["Preco"]):>24.2f}\n'
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
        os.system("clear")
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
            os.system("clear")
            while True:
                itemCompra = {"Nome": "", "Quantidade": 0, "Preco": 0.0, "Codigo": 0}
                item = input("Insira o código e a quantidade: ").split(" ")
                if item[0] != "0":
                    check = False
                    itemDados = procurarProduto(int(item[0]))
                    if itemDados != None:
                        itemCompra = {"Nome": itemDados["Nome"], "Quantidade": int(
                            item[1]), "Preco": itemDados["Preco"], "Codigo": itemDados["Codigo"], "Marca":itemDados["Marca"]}
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
    acoesLogistica = {"Cadastro":{}, "Exclusao":{}, "Reabastecimento":{}, "Retirada":{}}
    while True:
        os.system("clear")
        logisticaRelatorio = open("Logistica.txt",'a')
        logistica = int(input("""LOGÍSTICA HortiLife\n\n
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
                acoesLogistica["Exclusao"][produtoRelat["Marca"]].append([produtoRelat["Nome"]])
            else:
                acoesLogistica["Exclusao"][produtoRelat["Marca"]] = [produtoRelat["Nome"]]

        if logistica == 5:
            os.system("clear")
            estoqueLog = atualizarDadosProduto()
            if len(estoqueLog) > 0:
                if estoqueLog[1] < 0:
                    if estoqueLog[0] in acoesLogistica["Retirada"].keys():
                        acoesLogistica["Retirada"][estoqueLog[0]] += estoqueLog[1]
                    else:
                        acoesLogistica["Retirada"][estoqueLog[0]] = estoqueLog[1]
                else:
                    if estoqueLog[0] in acoesLogistica["Reabastecimento"].keys():
                        acoesLogistica["Reabastecimento"][estoqueLog[0]] += estoqueLog[1]
                    else:
                        acoesLogistica["Reabastecimento"][estoqueLog[0]] = estoqueLog[1]
        
        if logistica == 6:
            logisticaRelatorio.write(date.today().strftime("%d/%m/%Y") + " " + datetime.now().strftime("%H:%M:%S") +"\n\n")
            for marca in acoesLogistica["Cadastro"].keys():
                for produto in acoesLogistica["Cadastro"][marca]:
                    logisticaRelatorio.write(f'Nome: {produto[0]:<30} || Código: {produto[1]:<12} || Marca: {marca:<25}\n')
            
            logisticaRelatorio.write("\n\n")

            logisticaRelatorio.write("EXCLUSÃO - OPERAÇÕES\n")
            for marca in acoesLogistica["Exclusao"].keys():
                nomeProduto = str(acoesLogistica["Exclusao"][marca])
                logisticaRelatorio.write(f'Nome: {nomeProduto:<30} || Marca: {marca:<12}\n')
            
            logisticaRelatorio.write("\n\n")

            logisticaRelatorio.write("REABASTECIMENTO - OPERAÇÕES\n")
            for cod in acoesLogistica["Reabastecimento"].keys():
                qtdReabastecida = str(acoesLogistica["Reabastecimento"][cod])
                logisticaRelatorio.write(f'Código do produto: {cod:<30}  || Quantidade: {qtdReabastecida:<12}\n')
            
            logisticaRelatorio.write("\n\n")

            logisticaRelatorio.write("RETIRADA - OPERAÇÕES\n")
            for cod in acoesLogistica["Retirada"].keys():
                qtdRetirada = str(acoesLogistica["Retirada"][cod])
                logisticaRelatorio.write(f'Código do produto: {cod:<30}  || Quantidade: {qtdRetirada:<12}\n')
            
            logisticaRelatorio.write("\n\n")

            print("\nRetornando ao menu anterior...\n")
            break

def funcionariosMenu():
    while True:
        os.system("clear")
        funcionarios = int(input("""GERÊNCIA HortiLife
        1. Cadastrar novo funcionário
        2. Pesquisar funcionário
        3. Alterar dados de funcionário
        4. Excluir funcionário
        5. Voltar ao menu anterior
        
        COMANDO: """))

        if funcionarios == 1:
            os.system("clear")
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
            os.system("clear")
            consultarFuncionario()

        if funcionarios == 3:
            os.system("clear")
            listarFuncionario()

        if funcionarios == 4:
            os.system("clear")
            excluirFuncionario()

        if funcionarios == 5:
            os.system("clear")
            atualizarDadosFuncionario()

        if funcionarios == 6:
            print("\nRetornando ao menu anterior...\n")
            break

def adminMenu(nomeUsuario):
    nomeRelatorio = nomeUsuario + "_" + date.today().strftime("%d/%m/%Y") + "_" + datetime.now().strftime("%H.%M.%S")
    relatorioArq = open(nomeRelatorio, 'w')
    relatorioArq.write(nomeUsuario + "\nHorário de abertura: " + date.today().strftime("%d/%m/%Y") + " " + datetime.now().strftime("%H:%M:%S") +"\n\n")
    while True:
        os.system("clear")
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
            os.remove("Caixa.txt")
            os.remove("Logistica.txt")
            break

        else:
            print("Comando inválido! Tente novamente!")

def sistemaMenu(nomeUsuario):
    nomeRelatorio = nomeUsuario + "_" + date.today().strftime("%d_%m_%Y") + "_" + datetime.now().strftime("%H.%M.%S")
    relatorioArq = open(nomeRelatorio, 'a')
    relatorioArq.write(nomeUsuario + "\nHorário de abertura: " + date.today().strftime("%d/%m/%Y") + " " + datetime.now().strftime("%H:%M:%S") + "\n\n")
    while True:
        os.system("clear")
        menu = int(input("""SISTEMA HortiLife
        1. Operação de caixa
        2. Operação de logística
        3. Sair
        
        COMANDO: """))
        if menu == 1:
            caixaMenu()

        elif menu == 2:
            logisticaMenu()

        elif menu == 3:
            relatorioFinal = gerarRelatorio("Caixa.txt", "Logistica.txt")
            relatorioArq.write(relatorioFinal)
            relatorioArq.write("Horário de fechamento: " + date.today().strftime("%d/%m/%Y") + " " + datetime.now().strftime("%H:%M:%S") +"\n")
            relatorioArq.close()
            print("O relatório foi gerado com sucesso! Desativando sistema...")
            os.remove("Caixa.txt")
            os.remove("Logistica.txt")
            break

        else:
            print("Comando inválido! Tente novamente!")

# ____________________________________________________________________________

# Executável

while True:
    try:
        os.system("clear")
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
    except:
        os.system("clear")
        print("-- Login e/ou senha inválidos --")