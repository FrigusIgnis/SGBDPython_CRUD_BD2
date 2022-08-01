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