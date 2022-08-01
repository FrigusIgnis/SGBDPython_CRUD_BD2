def gerarRelatorio(arq1, arq2):
    caixa = open(arq1, 'r')
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

def gerarRelatorioAdmin(arq1, arq2, arq3):
    caixa = open(arq1, 'r')
    logistica = open(arq2, 'r')
    funcionario = open(arq3, 'r')
    relatorio = ""

    relatorio += "--- OPERAÇÕES DE CAIXA\n"
    for linha in caixa.readlines():
        relatorio += linha

    relatorio += "\n"

    relatorio += "--- OPERAÇÕES DE LOGÍSTICA\n"
    for linha in logistica.readlines():
        relatorio += linha

    relatorio += "\n"

    relatorio += "--- OPERAÇÕES DE ADMINISTRAÇÃO\n"
    for linha in funcionario.readlines():
        relatorio += linha
    
    return relatorio
