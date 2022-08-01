import os
import time

from datetime import date
from datetime import datetime
from interfaces_sistema import * #Interfaces do sistema
from gerimento_Reletorios import * #Gerimento de relatórios

def adminMenu(nomeUsuario):
    nomeRelatorio = nomeUsuario + "_" + date.today().strftime("%d_%m_%Y") + "_" + datetime.now().strftime("%H.%M.%S")
    relatorioArq = open(nomeRelatorio, 'a')
    relatorioArq.write(nomeUsuario + "\nHorário de abertura: " + date.today().strftime("%d/%m/%Y") + " " + datetime.now().strftime("%H:%M:%S") + "\n\n")
    while True:
        os.system("clear")
        admin = int(input("""ADMINISTRAÇÃO HortiLife

        1. Gerenciar funcionários
        2. Gerenciar logística
        3. Gerenciar caixa
        4. Sair
    
        COMANDO: """))

        if admin == 1:
            funcionariosMenu()

        elif admin == 2:
            logisticaMenu()

        elif admin == 3:
            caixaMenu()

        elif admin == 4:
            checkCaixa = open("Caixa.txt", 'a')
            checkLogistica = open("Logistica.txt", 'a')
            checkFunc = open("Administracao.txt", 'a')
            relatorioFinal = gerarRelatorioAdmin("Caixa.txt", "Logistica.txt", "Administracao.txt")

            relatorioArq.write("\n" + relatorioFinal + "\n")
            
            relatorioArq.write("\nHorário de fechamento: " + date.today().strftime(
                    "%d/%m/%Y") + " " + datetime.now().strftime("%H:%M:%S") + "\n\n")
            relatorioArq.close()

            if os.path.exists("Caixa.txt") == True:
                os.remove("Caixa.txt")

            if os.path.exists("Logistica.txt") == True:
                os.remove("Logistica.txt")
                
            if os.path.exists("Administracao.txt") == True:
                os.remove("Administracao.txt")

            break

        else:
            os.system("clear")
            print("Comando inválido! Tente novamente")
            time.sleep(1)

def sistemaMenu(nomeUsuario):
    nomeRelatorio = nomeUsuario + "_" + date.today().strftime("%d_%m_%Y") + "_" + datetime.now().strftime("%H.%M.%S")
    relatorioArq = open(nomeRelatorio, 'a')
    relatorioArq.write(nomeUsuario + "\nHorário de abertura: " + date.today(
      ).strftime("%d/%m/%Y") + " " + datetime.now().strftime("%H:%M:%S") + "\n\n")
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
            checkCaixa = open("Caixa.txt", 'a')
            checkLogistica = open("Logistica.txt", 'a')
            relatorioFinal = gerarRelatorio("Caixa.txt", "Logistica.txt")

            relatorioArq.write("\n" + relatorioFinal + "\n")

            relatorioArq.write("\nHorário de fechamento: " + date.today().strftime(
                "%d/%m/%Y") + " " + datetime.now().strftime("%H:%M:%S") + "\n")
            relatorioArq.close()
            checkCaixa.close()
            checkLogistica.close()

            print("O relatório foi gerado com sucesso! Desativando sistema...")

            if os.path.exists("Caixa.txt") == True:
                os.remove("Caixa.txt")

            if os.path.exists("Logistica.txt") == True:
                os.remove("Logistica.txt")

            break

        else:
            print("Comando inválido! Tente novamente!")
