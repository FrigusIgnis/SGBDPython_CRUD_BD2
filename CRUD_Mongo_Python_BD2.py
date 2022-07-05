import pymongo
from random import randint


client = pymongo.MongoClient("mongodb+srv://NicolasSilva:nsda1205@sgdbpython-crud-nsda-bd.p1kei.mongodb.net/?retryWrites=true&w=majority")

myDB = client["myDatabase"]

collAlunos = myDB["Alunos"]


def matricular_aluno():
    nome = input("Insira o nome do aluno(a): ")
    cpf = input("Insira o CPF do aluno(a): ")
    matr = randint(10000,50000)
    while matr in collAlunos.find():
        matr = randint(10000, 50000)
    
    matricular = {"Nome":nome, "CPF":cpf, "Matricula":matr}
    collAlunos.insert_one(matricular)

    print("Um novo aluno foi adicionado com sucesso!\n\n")



matricular_aluno()
