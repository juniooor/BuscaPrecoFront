from django.shortcuts import render


def pesquisar(requests):
    return render(requests,'produtos/pesquisa.html')

def exibir_resultados(requests):
    pass
