from django.shortcuts import render


def pesquisar(request):
    return render(request, 'project/pesquisa.html')

def exibir_resultados(requests):
    pass
