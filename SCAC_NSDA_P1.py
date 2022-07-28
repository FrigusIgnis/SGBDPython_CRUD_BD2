import os

"""
cadastrarProduto("Banana Prata", 3.09, 200, 1000, "Filomena")
cadastrarProduto("Banana Prata", 2.99, 150, gerarCodigoProduto(), "Filó")
cadastrarProduto("Banana Prata", 3.04, 175, gerarCodigoProduto(), "AgroFruti")
cadastrarProduto("Morango", 19.99, 200, gerarCodigoProduto(), "Filomena")
cadastrarProduto("Morango", 20.09, 200, gerarCodigoProduto(), "Hortal")
cadastrarProduto("Maçã verde", 14.99, 200, gerarCodigoProduto(), "Hortal")
cadastrarProduto("Maçã verde", 14.79, 200, gerarCodigoProduto(), "Pomária")
cadastrarProduto("Maçã vermelha", 5.99, 200, gerarCodigoProduto(), "Hortal")
cadastrarProduto("Maçã vermelha", 5.79, 200, gerarCodigoProduto(), "Pomária")
cadastrarProduto("Uva verde", 10.99, 200, gerarCodigoProduto(), "Filomena")
cadastrarProduto("Uva verde", 10.99, 200, gerarCodigoProduto(), "Filó")
cadastrarProduto("Uva verde", 10.96, 200, gerarCodigoProduto(), "Hortal")
cadastrarProduto("Uva verde", 10.94, 200, gerarCodigoProduto(), "AgroFruti")
cadastrarProduto("Uva verde", 10.89, 200, gerarCodigoProduto(), "Pomária")
cadastrarProduto("Uva roxa", 6.89, 200, gerarCodigoProduto(), "Hortal")
cadastrarProduto("Uva roxa", 6.89, 200, gerarCodigoProduto(), "Filomena")
cadastrarProduto("Melão verde", 4.99, 200, gerarCodigoProduto(), "Filomena")
cadastrarProduto("Melão verde", 4.99, 200, gerarCodigoProduto(), "Filó")
cadastrarProduto("Melão verde", 4.89, 200, gerarCodigoProduto(), "Pomária")
cadastrarProduto("Melância vermelha", 4.59, 150, gerarCodigoProduto(), "Pomária")
cadastrarProduto("Melância vermelha", 4.79, 150, gerarCodigoProduto(), "AgroFruti")
cadastrarProduto("Melância amarela", 3.59, 150, gerarCodigoProduto(), "Pomária")
cadastrarProduto("Melância amarela", 3.69, 150, gerarCodigoProduto(), "Hortal")
cadastrarProduto("Kiwi", 19.89, 200, gerarCodigoProduto(), "Filomena")
cadastrarProduto("Kiwi", 19.79, 200, gerarCodigoProduto(), "Filó")
cadastrarProduto("Mamão Papaya", 6.49, 200, gerarCodigoProduto(), "Filomena")
cadastrarProduto("Mamão Papaya", 6.49, 200, gerarCodigoProduto(), "Filó")
cadastrarProduto("Quiabo", 5.69, 200, gerarCodigoProduto(), "Hortal")
cadastrarProduto("Coentro", 4.89, 200, gerarCodigoProduto(), "Hortal")
cadastrarProduto("Salsa", 3.39, 200, gerarCodigoProduto(), "Hortal")
cadastrarProduto("Salsa", 3.39, 200, gerarCodigoProduto(), "Filomena")
cadastrarProduto("Abóbora", 2.29, 200, gerarCodigoProduto(), "Filó")
cadastrarProduto("Abóbora", 2.19, 200, gerarCodigoProduto(), "Pomária")
cadastrarProduto("Tomate", 3.59, 200, gerarCodigoProduto(), "Hortal")
cadastrarProduto("Tomate", 3.59, 200, gerarCodigoProduto(), "AgroFruti")
cadastrarProduto("Cebola", 2.49, 200, gerarCodigoProduto(), "Filó")
cadastrarProduto("Cebola", 2.49, 200, gerarCodigoProduto(), "AgroFruti")
cadastrarProduto("Alho", 17.19, 200, gerarCodigoProduto(), "Filó")
cadastrarProduto("Alho", 17.19, 200, gerarCodigoProduto(), "AgroFruti")
cadastrarProduto("Couve", 6.99, 200, gerarCodigoProduto(), "Pomária")
cadastrarProduto("Couve-flor", 5.19, 200, gerarCodigoProduto(), "Filomena")
cadastrarProduto("Couve-flor", 5.19, 200, gerarCodigoProduto(), "Filó")
cadastrarProduto("Couve-flor", 5.19, 200, gerarCodigoProduto(), "Hortal")
cadastrarProduto("Couve-flor", 5.19, 200, gerarCodigoProduto(), "AgroFruti")
cadastrarProduto("Couve-flor", 5.19, 200, gerarCodigoProduto(), "Pomária")
cadastrarProduto("Beterraba", 2.29, 200, gerarCodigoProduto(), "AgroFruti")
cadastrarProduto("Cogumelo shitake", 48.59, 100, gerarCodigoProduto(), "Hortal")
cadastrarProduto("Cogumelo champignon", 46.09, 100, gerarCodigoProduto(), "Filó")
cadastrarProduto("Cogumento shimeji", 13.89, 200, gerarCodigoProduto(), "AgroFruti")
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

aluno = []
prof = []
disc = []
tur = []
nome_ar = ''

#A função clear() limpa tudo o que estiver no
# console enquanto o script é executado.
def clear():
    os.system('cls')#Esta função é responsável pela limpeza da janela de comando.

#A função rel_aluno() gera uma relação de alunos
#a partir dos dados que foram carregados do arquivo.
def rel_aluno():
    global aluno
    count = 0
    clear()
    print("<=======================================>")
    for x in aluno:
        print("""Nome: %s
CPF: %s
<=======================================>"""%(x[0],x[1]))
        count += 1
    print("\nOs dados de %d aluno(s) foram carregados!\n" % count)

#Todas as funções [leitor_arq_] buscam o arquivo
# pelo nome através da variável 'nome_arq' e, utilizando
# o método readlines(), guarda todos os dados que estiver no arquivo dentro
# de sua respectiva lista.
def leitor_arq_aluno(nome_arq):
    global aluno
    reader = open(nome_arq,'r')
    aluno = []
    for x in reader.readlines():
        nome,cpf = x.strip().split("-")
        aluno.append([nome,cpf])
    reader.close()
    clear()
    print("%s foi carregado!\n\n" % nome_arq)

def leitor_arq_prof(nome_arq):
    global prof
    reader = open(nome_arq,'r')
    prof = []
    for x in reader.readlines():
        nome,cpf, dept = x.strip().split("-")
        prof.append([nome,cpf,dept])
    reader.close()
    clear()
    print("%s foi carregado!\n\n" % nome_arq)

def leitor_arq_disc(nome_arq):
    global disc
    reader = open(nome_arq,'r')
    disc = []
    for x in reader.readlines():
        code_disc,disci = x.strip().split("-")
        disc.append([disci,code_disc])
    reader.close()
    clear()
    print("%s foi carregado!" % nome_arq)

def leitor_arq_turma(nome_arq):
    global tur
    reader = open(nome_arq,'r')
    tur = []
    for x in reader.readlines():
        code_class, period, code_disc, cpf_prof, cpf_aluno = x.strip().split("-")
        tur.append([code_class, period, code_disc, [cpf_prof], [cpf_aluno]])
    reader.close()
    clear()
    print("%s foi carregado" % nome_arq)

#Todas as funções [salvar_] utilizam o método write() para salvar
# novos dados que foram inseridos dentro do arquivo que está
#sendo utilizado.
def salvar_aluno(nome):
        global aluno
        if ".txt" in nome:
            nome.replace(".txt","")
        save = open(nome,'w')
        for x in aluno:
            save.write("%s-%s\n" % (x[0],x[1]))
        save.close()
        print("Dados salvos!\n\n")

def salvar_prof(nome):
    global prof
    if ".txt" in nome:
            nome.replace(".txt","")
    save = open(nome,'w')
    for x in prof:
        save.write("%s-%s-%s\n" % (x[0],x[1],x[2]))
    save.close()
    print("Dados salvos!\n\n")
        
def salvar_disc(nome):
    global disc
    if ".txt" in nome:
            nome.replace(".txt","")
    save = open(nome,'w')
    for x in disc:
        save.write("%s-%s\n" % (x[0],x[1]))
    save.close()
    print("Dados salvos!\n\n")
        
def salvar_turma(nome):
    global tur
    if ".txt" in nome:
            nome.replace(".txt","")
    save = open(nome,'w')
    for x in tur:
        save.write("%s-%s-%s-%s-%s\n" % (x[0],x[1],x[2],x[3],x[4]))
    save.close()
    clear()
    print("Dados salvos!\n\n")

#Todas as funções [criador_] são utilizadas para a entrada de
# novos dados, armazenando-os dentro de sua respectiva lista
#para então ser armazenado no arquivo utilizado.
def criador_professor():
    global prof
    nome = input("Nome: ")
    cpf = input("CPF: ")
    dept = input("Departamento: ")
    prof.append([nome,cpf,dept])
    clear()
    print("Um novo professor foi adicionado com sucesso!\n\n")

def criador_disciplina():
    global disc
    disci = input("Nome: ")
    code_disc = input("Código: ")
    disc.append([code_disc,disci])
    clear()
    print("Uma nova disciplina foi adicionada com sucesso\n\n")


def criador_aluno():
    global aluno
    nome = input("Insira o nome do aluno(a): ")
    cpf = input("Insira o CPF do aluno(a): ")
    aluno.append([nome, cpf])
    clear()
    print("Um novo aluno foi adicionado com sucesso!\n\n")
                
def criador_turma():
    global tur
    code_class = input("Código da turma: ")
    period = input("Período: ")
    code_disc = input("Código da disciplina: ")
    cpf_prof = []
    cpf_alunos = []
    while True:
      menu = int(input("Insira o CPF dos alunos de um por um(Digite 0 para finalizar): "))
      if menu != 0:
        cpf_alunos.append(menu)
      else:
        break
    while True:
      menu = int(input("Insira o CPF do(s) professor(es) de um por um (Digite 0 para finalizar): "))
      if menu != 0:
        cpf_prof.append(menu)
      else:
        break
    clear()
    tur.append([code_class, period, code_disc, cpf_prof, cpf_alunos])

#Todas as funções [leitor_] são utilizadas para carregar algum
#outro arquivo do setor correspondente, para isso, foi utilizado
# o método readlines() para poder ler o que está dentro do arquivo
# e, assim, armazenar os dados dentro da respectiva lista.
def leitor_aluno():
    global aluno
    global nome_ar
    count = 0
    reader = open(nome_ar+".txt",'r')
    aluno = []
    for x in reader.readlines():
        nome,cpf = x.strip().split("-")
        aluno.append([nome,cpf])
    reader.close()
    clear()
    print("Carregando arquivo...\n")
    for x in aluno:
        count += 1
    print("Os dados de %d aluno(s) foram carregados!\n\n" % count)

def leitor_prof():
    global prof
    global nome_ar
    count = 0
    reader = open(nome_ar+".txt",'r')
    prof = []
    for x in reader.readlines():
        nome,cpf, dept = x.strip().split("-")
        aluno.append([nome,cpf,dept])
    reader.close()
    clear()
    print("Carregando arquivo...\n")
    for x in prof:
        count += 1
    print("Os dados de %d professor(es) foram carregados!\n\n" % count)
    
def leitor_disc():
    global disc
    global nome_ar
    count = 0
    reader = open(nome_ar+".txt",'r')
    disc = []
    for x in reader.readlines():
        code_disc,disci = x.strip().split("-")
        disc.append([disci,code_disc])
    reader.close()
    clear()
    print("Carregando arquivo...\n")
    for x in disc:
        count += 1
    print("Os dados de %d disciplina(s) foram carregados!\n\n" % count)

def leitor_turma():
    global tur
    global nome_ar
    count = 0
    reader = open(nome_ar,'r')
    tur = []
    for x in reader.readlines():
        code_class, period, code_disc, cpf_prof, cpf_aluno = x.strip().split("-")
        tur.append([code_class, period, code_disc, [cpf_prof], [cpf_aluno]])
    reader.close()
    clear()
    print("Carregando arquivo...\n")
    for x in tur:
        count += 1
    print("Os dados de %d turma(s) foram carregados!\n\n" % count)
    reader.close()

#As funções [pesq_] executam uma busca pelos dados do arquivo que foi
# carregado, para isso é utilizado um input() para facilitar o trabalho.
def pesq_aluno():
    nome_pesq = input("Insira o nome do aluno: ")
    clear()
    check = False
    for x,y in enumerate(aluno):
        if nome_pesq.lower() in y[0].lower():
            check = True
            print("""Nome: %s
>>>>CPF: %s""" % (y[0],y[1]))
    if check == False:
        print("Aluno não encontrado!\n")

def pesq_prof():
    nome_pesq = input("Insira o nome do professor(a): ")
    clear()
    check = False
    for x,y in enumerate(prof):
        if nome_pesq.lower() in y[0].lower():
            check = True
            print("""Nome: %s
>>>>CPF: %s
>>>>Departamento: %s""" % (y[0],y[1],y[2]))
    if check == False and count < 1:
        print("Professor não encontrado!")

def pesq_disc():
    nome_pesq = input("Insira o nome da disciplina: ")
    clear()
    check = False
    for x,y in enumerate(disc):
        if nome_pesq.lower() in y[0].lower():
            check = True
            print("""Disciplina: %s
>>>>Código: %s""" % (y[0],y[1]))
    if check == False:
        print("Disciplina não encontrada!")

def pesq_turma():
    nome_pesq = input("Insira a turma: ")
    period_pesq = input("Insira o período: ")
    code_disc_pesq = input("Insira o código da disciplina: ")
    clear()
    check = False
    for x,y in enumerate(tur):
        if nome_pesq.lower() in y[0].lower() and period_pesq in y[1].lower() and code_disc_pesq in y[2].lower():
            check = True
            print(""">>Código da turma: %s
>>>>Período: %s
>>>>Código da disciplina: %s
>>>>CPF dos professores:""" % (y[0],y[1],y[2]))
            for x in y[3]:
                print(">>>>>>%s"%(x))
            print(">>>>CPF dos alunos:")
            for x in y[4]:
                print(">>>>>>%s" % x)
    print("\n")
    if check == False:
        print("Turma não encontrada!") 

#As funções [att_] são utilizadas para atualizar algum dado já existente no
# arquivo(Utiliza quase o mesmo sistema das funções [pesq_] onde a diferença
# está no fato de quê ele requer outro input() para poder modificar algo.
def att_aluno():
    global aluno
    nome = input("Insira o nome do aluno para executar a busca: ")
    for x in aluno:
        if nome.lower() in x[0].lower():
            print("Aluno encontrado!")
            j = input("""O que deseja mudar? (Nome ou CPF)
R: """)
            if j.lower() == "nome":
                new_name = input("Insira um novo nome: ")
                x[0] = new_name
                salvar_aluno(nome_ar)
            elif j.lower() == "cpf":
                new_cpf = int(input("Insira o novo CPF: "))
                x[1] = new_cpf

def att_prof():
    global prof
    nome = input("Insira o nome do professor para executar a busca: ")
    for x in prof:
        if x[0] == nome:
            print("Professor encontrado!")
            j = input("""O que deseja mudar? (Nome, CPF ou Departamento)
R: """)
            if j.lower() == "nome":
                new_name = input("Insira o nome: ")
                prof[x][0] = new_name
            elif j.lower() == "cpf":
                new_cpf = int(input("Insira o novo CPF: "))
                prof[x][1] = new_cpf
            elif j.lower() == "departamento":
                new_dept = input("Insira o departamento: ")
                prof[x][2] = new_dept

def att_disc():
    global disc
    nome = input("Insira o nome da disciplina para executar a busca: ")
    for x in disc:
        if x[0] == nome:
            print("Disciplina encontrada!")
            j = input("""O que deseja mudar? (Nome ou Código)
R: """)
            if j.lower() == "nome":
                new_name = input("Insira o novo nome: ")
                disc[x][0] = new_name
            elif j.lower() == "código" or j.lower() == "codigo":
                new_code_disc = int(input("Insira o novo código: "))
                disc[x][1] = new_code_disc

def att_turma():
    global tur
    nome = input("Insira a turma: ")
    period = input("Insira o período da turma: ")
    disc = input("Insira o código da disciplina: ")
    for x in tur:
        if x[0] == nome and x[1] == period and x[2] == disc:
            print("Turma encontrada!")
            j = input("""O que deseja mudar? (Código da turma , período, código da disciplina, CPF dos professores ou CPF dos alunos)
R: """)
            if j.lower() == "código da turma" or j.lower() == "codigo da turma":
                new_code_class = input("Insira o código da turma: ")
                tur[x][0] = new_code_class
            elif j.lower() == "periodo" or j.lower() == "período":
                new_period = int(input("Insira o período: "))
                tur[x][1] = new_period
            elif j.lower() == "código da disciplina" or j.lower() == "codigo da disciplina":
                new_code_disc = input("Insira o código da disciplina: ")
                tur[x][2] = new_code_disc
            elif j.lower() == "cpf dos alunos":
                cpf_prof = input("Insira o CPF para executar a busca: ")
                for y in x[3]:
                    if y == cpf_prof:
                        print("Professor encontrado!")
                        new_cpf_prof = input("Insira o novo CPF: ")
                        tur[x][x[3].index(y)] = new_cpf_prof
                    else:
                        print("Professor não encontrado!\n")
            elif j.lower() == 'cpf dos professores':
                cpf_aluno = input('Insira o CPF para executar a busca: ')
                for y in x[4]:
                    if y == cpf_aluno:
                        print('Aluno econtrado!')
                        new_cpf_aluno = input("Insira o novo CPF: ")
                        tur[x][x[4].index(y)] = new_cpf_aluno
                    

#As funções [del_] são utilizadas para poder apagar dados, utilizando a
# função del foi possível fazer a parte de Delete do projeto.
def del_aluno():
    global aluno
    nome_del = input("Insira o nome do Aluno: ")
    for y,x in enumerate(aluno):
        if x[1].lower() == nome_del.lower():
            del aluno[y]
            clear()
            print("Dados apagados!\n\n")
            break

def del_prof():
    global prof
    nome_del = input("Insira o nome do professor: ")
    for y,x in enumerate(prof):
        if x[1].lower() == nome_del.lower():
            del prof[y]
            clear()
            print("Dados apagados!\n\n")
            break

def del_disc():
    global disc
    nome_del = input("Insira o código da disciplina: ")
    for y,x in enumerate(disc):
        if x[0] == nome_del:
            del disc[y]
            clear()
            print("Dados apagados!\n\n")
            break

def del_turma():
    global tur
    nome_del = input("Insira a turma, o período, e o código da disciplina: ").split()
    for y,x in enumerate(tur):
        if x[0] == nome_del[0] and x[1] == nome_del[1] and x[2] == nome_del[2]:
            del tur[y]
            clear()
            print("Dados apagados!\n\n")
            break

#As funções restantes foram utilizadas para criar o menu de cada setor.
def aluno_menu():
    global nome_ar
    while True:
        menu = int(input("""1 - Adicionar um aluno
2 - Excluir um aluno
3 - Atualizar dados de um aluno já existente
4 - Pesquisar dados de um aluno já existente
5 - Gerar relação de alunos
6 - Salvar dados
7 - Carregar outro arquivo
0 - Voltar ao menu anterior

COMANDO: """))
        if menu == 0:
            clear()
            break
        elif menu == 1:
            clear()
            criador_aluno()
        elif menu == 2:
            clear()
            del_aluno()
        elif menu == 3:
            clear()
            att_aluno()
        elif menu == 4:
            clear()
            pesq_aluno()
        elif menu == 5:
            clear()
            rel_aluno()
        elif menu == 6:
            clear()
            salvar_aluno(nome_ar)
        elif menu == 7:
            clear()
            nome_ar = input("Insira o nome do arquivo: ") + '.txt'
            leitor_aluno()
        elif menu < 0 or menu > 8 or menu.isnumeric() == False:
            clear()
            print("Comando inválido! Selecione uma das opções disponivéis!")
    
def prof_menu():
    global nome_ar
    while True:
        menu = int(input("""1 - Adicionar um professor
2 - Excluir dados de um professor já existente
3 - Atualizar dados de um professor já existente
4 - Pesquisar dados de um professor já existente
5 - Gerar ata de frequência
6 - Salvar dados
7 - Carregar outro arquivo
0 - Voltar ao menu anterior

COMANDO: """))
        if menu == 0:
            clear()
            break
        elif menu == 1:
            clear()
            criador_professor()
        elif menu == 2:
            clear()
            del_professor()
        elif menu == 3:
            clear()
            att_disciplina()
        elif menu == 4:
            pesq_prof()
        elif menu == 5:
            clear()
            ata_freq()
        elif menu == 6:
            clear()
            salvar_prof(nome_ar)
        elif menu == 7:
            clear()
            nome_ar = input("Insira o nome do arquivo: ") + '.txt'
            leitor_prof()
        elif menu < 0 or menu > 8 or menu.isnumeric() == False:
            clear()
            print("Comando inválido! Selecione uma das opções disponíveis!")

    
def disc_menu():
    global nome_ar
    while True:
        menu = int(input("""1 - Adicionar uma nova disciplina
2 - Excluir dados de um disciplina já existente
3 - Atualizar dados de uma disciplina já existente
4 - Pesquisar dados de uma disciplina já existente
5 - Gerar ata de exercício
6 - Salvar dados
7 - Carregar outro arquivo
0 - Voltar ao menu anterior

COMANDO: """))
        if menu == 0:
            clear()
            break
        elif menu == 1:
            clear()
            criador_disciplina()
        elif menu == 2:
            clear()
            del_disc()
        elif menu == 3:
            clear()
            att_disc()
        elif menu == 4:
            pesq_disc()
        elif menu == 5:
            clear()
            ata_exer()
        elif menu == 6:
            clear()
            salvar_disc(nome_ar)
        elif menu == 7:
            clear()
            nome_ar = input("Insira o nome do arquivo: ") + '.txt'
            leitor_disc()
        elif menu < 0 or menu > 8 or menu.isnumeric() == False:
            clear()
            print("Comando inválido! Selecione uma das opções disponíveis!")

    
def turm_menu():
    global nome_ar
    while True:
        menu = int(input("""1 - Adicionar uma nova turma
2 - Excluir dados de uma turma já existente
3 - Atualizar dados de uma turma já existente
4 - Pesquisar dados de uma turma já existente
5 - Gerar ata de exercício
6 - Salvar dados
7 - Carregar outro arquivo
0 - Voltar ao menu anterior

COMANDO: """))
        if menu == 0:
            clear()
            break
        elif menu == 1:
            clear()
            criador_turma()
        elif menu == 2:
            clear()
            del_turma()
        elif menu == 3:
            clear()
            att_turma()
        elif menu == 4:
            pesq_turma()
        elif menu == 5:
            clear()
            ata_exer()
        elif menu == 6:
            clear()
            salvar_turma(nome_ar)
        elif menu == 7:
            clear()
            nome_ar = input("Insira o nome do arquivo: ")+'.txt'
            leitor_turma()
        elif menu < 0 or menu > 8 or menu.isnumeric() == False:
            clear()
            print("Comando inválido! Selecione uma das opções disponíveis!")



    
#E, por último, onde tudo acontece, o Menu Principal!
# O while True foi utilizado para que se possa fazer várias alterações
# enquanto a condição de parada não for verdadeira e, dentro de cada opção,
# foi incrementado o método de criar/carregar arquivo para facilitar a
#gerência de arquivos.
while True:
    menu = int(input("""============| SEJA BEM-VINDO AO SISTEMA DE CONTROLE ACADÊMICO |===============\n\n
Opções:
1 - Gerenciar dados relacionados aos alunos
2 - Gerenciar dados relacionados aos professores
3 - Gerenciar dados relacionados às disciplinas
4 - Gerenciar dados relacionados às turmas
0 - Encerrar programa

COMANDO: """))
    if menu == 0:
        break
    elif menu == 1:
        
        perg_arquivo = input('''Deseja carregar ou criar um arquivo?
R: ''')
        if perg_arquivo.lower() == "carregar" or perg_arquivo.lower() == "carregar arquivo":#Toda a parte de carregamento e criação de arquivos é feita com esta condição.
            nome_ar = input("Insira o nome do arquivo: ") + ".txt"
            leitor_arq_aluno(nome_ar)
            clear()
            aluno_menu()
        elif perg_arquivo.lower() == "criar" or perg_arquivo.lower() == "criar arquivo":
            nome_ar = input("Insira o nome do arquivo: ") + ".txt"
            j = open(nome_ar,'w')
            j.close()
            leitor_arq_aluno(nome_ar)
            clear()
            aluno_menu()
        else:
            clear()
            print("Comando inválido! Retornando para o menu principal...\n\n")
            
    elif menu == 2:
        
        perg_arquivo = input('''Deseja carregar ou criar um arquivo?
R: ''')
        if perg_arquivo.lower() == "carregar" or perg_arquivo.lower() == "carregar arquivo":
            nome_ar = input("Insira o nome do arquivo: ") + ".txt"
            leitor_arq_prof(nome_ar)
            clear()
            prof_menu()
        elif perg_arquivo.lower() == "criar" or perg_arquivo.lower() == "criar arquivo":
            nome_ar = input("Insira o nome do arquivo: ") + ".txt"
            j = open(nome_ar,'w')
            j.close()
            leitor_arq_prof(nome_ar)
            clear()
            prof_menu()
        else:
            clear()
            print("Comando inválido! Retornando para o menu principal...\n\n")
            
    elif menu == 3:
        
        perg_arquivo = input('''Deseja carregar ou criar um arquivo?
R: ''')
        if perg_arquivo.lower() == "carregar" or perg_arquivo.lower() == "carregar arquivo":
            nome_ar = input("Insira o nome do arquivo: ") + ".txt"
            leitor_arq_disc(nome_ar)
            clear()
            disc_menu()
        elif perg_arquivo.lower() == "criar" or perg_arquivo.lower() == "criar arquivo":
            nome_ar = input("Insira o nome do arquivo: ") + ".txt"
            j = open(nome_ar,'w')
            j.close()
            leitor_arq_disc(nome_ar)
            clear()
            disc_menu()
        else:
            clear()
            print("Comando inválido! Retornando para o menu principal...\n\n")
            
    elif menu == 4:
        
        perg_arquivo = input('''Deseja carregar ou criar um arquivo?
R: ''')
        if perg_arquivo.lower() == "carregar" or perg_arquivo.lower() == "carregar arquivo":
            nome_ar = input("Insira o nome do arquivo: ") + ".txt"
            leitor_arq_turma(nome_ar)
            clear()
            turm_menu()
        elif perg_arquivo.lower() == "criar" or perg_arquivo.lower() == "criar arquivo":
            nome_ar = input("Insira o nome do arquivo: ") + ".txt"
            j = open(nome_ar,'w')
            j.close()
            leitor_arq_turma(nome_ar)
            clear()
            turm_menu()
        else:
            clear()
            print("Comando inválido! Retornando para o menu principal...\n\n")
    elif menu < 0 or menu > 5 or menu.isnumeric() == False:
        print("Comando inválido! Selecione uma das opções disponíveis!\n")
