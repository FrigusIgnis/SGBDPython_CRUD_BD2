import os
import time

from gerimento_Reletorios import * #Gerimento de relatórios
from gerenciamento_funcionario import * #Gerenciamento de usuário/funcionário
from gerenciamento_estoque import * #Gerenciamento de estoque
from gerenciamento_caixa import * #Gerenciamento de caixa
from interfaces_sistema import * #Interfaces do sistema
from interfaces_usuario import * #Interfaces para o usuário

# ____________________________________________________________________________

# Executável

while True:
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
        time.sleep(1)