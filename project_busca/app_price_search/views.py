from django.shortcuts import render

from .models import Product


def pesquisar(request):
    return render(request, 'project/pesquisa.html')


def exibir_resultados(requests):
    name_produto = requests.POST.get('produto')
    print(name_produto)
    dados = {
        'dados': Product.objects.filter(name__icontains=name_produto).order_by('price')
    }
    return render(requests, 'project/resultados.html', dados)
