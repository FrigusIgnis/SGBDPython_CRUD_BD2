import pymongo
import time
import os
import string
import random

from random import randint
from validacao_usuario import *

client = pymongo.MongoClient(
    "mongodb+srv://NicolasSilva:nsda1205@sgdbpython-crud-nsda-bd.p1kei.mongodb.net/?retryWrites=true&w=majority")

myDB = client["myDatabase"]
collFuncionarios = myDB["Funcionarios"]

def procurarFunc(codFunc):
    queryFunc = None
    for funcionario in collFuncionarios.find({"CodFunc": codFunc}):
        queryFunc = funcionario

    if queryFunc != None:
        return queryFunc
    else:
        print("Funcionário não encontrado! Tente novamente!")

def cadastrarFuncionario(nome, cpf, codFunc, isAdmin):
    senhaFunc = geradorSenha()
    cadastroFunc = {"Nome": nome, "CPF": cpf, "CodFunc": codFunc,
                    codFunc: senhaFunc[1], "Admin?": isAdmin}
    collFuncionarios.insert_one(cadastroFunc)
    print(
        f'Funcionário adicionado com sucesso!\nNome: {nome}\n{("Usuário: "+ codFunc)}\n{("Senha: %d" % senhaFunc[0])}\n')
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
        print("\nOs dados de %d funcionários foram carregados.\n" %
              totalFuncBusca)

        print(f'{"NOME":^40}||{"CÓDIGO":^12}||')
        print(f'{"":^40}||{"":^12}||')
        for item in listaResultado:
            print(f'{item["Nome"]:^40}||{item["CodFunc"]:^12}||')
        input()

def listarFuncionario():
    totalFuncionarios = 0
    for funcionario in collFuncionarios.find().sort("Nome"):
        print("\nNome: %s\nCódigo de funcionário: %s" %
              (funcionario["Nome"], funcionario["CodFunc"]))
        print("__________________________________________________")
        totalFuncionarios += 1
    print("Os dados de %d funcionários foram carregados.\n" % totalFuncionarios)
    input()

def excluirFuncionario():
    cod = input("Código de funcionário: ")
    queryFunc = procurarFunc(cod)
    relatFunc = queryFunc

    if queryFunc != None:
        collFuncionarios.delete_one(queryFunc)
        print("Funcionário excluído do sistema com sucesso.")
        time.sleep(3)
    
    return relatFunc

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
        novaSenha = geradorSenha()
        updateDados = {"$set": {cod: novaSenha[1]}}
        collFuncionarios.update_one({cod: funcionario[cod]}, updateDados)
        print("\nNova senha para o usuário %s: %d\n" % (cod, novaSenha[0]))
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
