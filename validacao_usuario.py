import pymongo
import time
import os
import string
import random

from random import randint

client = pymongo.MongoClient(
    "mongodb+srv://NicolasSilva:nsda1205@sgdbpython-crud-nsda-bd.p1kei.mongodb.net/?retryWrites=true&w=majority")

myDB = client["myDatabase"]
collFuncionarios = myDB["Funcionarios"]

def validarUsuario(usuario, senha):
    codAcesso = conversorSenha(senha)
    queryUsuario = None
    for usuario in collFuncionarios.find({usuario:codAcesso}):
        queryUsuario = usuario

    if(queryUsuario != None):
        return queryUsuario
    else:
        print("Usuário e/ou senha incorretos! Tente novamente.")

def geradorSenha():
    validacao = []
    codAcesso = random.randint(100000, 999999)
    validacao.append(codAcesso)
    seqAcesso = conversorSenha(codAcesso)
    validacao.append(seqAcesso)

    return validacao


def conversorSenha(senha):
    convCodAcesso = str(senha)
    seqAcesso = str((int(convCodAcesso[0]) % 3)) + str(
        (int(convCodAcesso[1]) % 4)) + str(
        (int(convCodAcesso[2]) % 7)) + str(
        (int(convCodAcesso[3]) % 6)) + str(
        (int(convCodAcesso[4]) % 9)) + str(
        (int(convCodAcesso[5]) % 8))
    seqAcesso = int(seqAcesso)
    return seqAcesso