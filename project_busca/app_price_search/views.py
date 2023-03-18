# from pprint import pprint
from django.shortcuts import render
from utils.scrapy_search_price import scan_site_1, scan_site_2, scan_site_3

from .models import Product


def pesquisar(request):
    return render(request, 'project/pesquisa.html')


def exibir_resultados(requests):
    name_produto = requests.POST.get('produto')
    produto = Product.objects.filter(name__icontains=name_produto)  
    if not name_produto.isdigit() and name_produto != '':
        for prod in produto:
            if name_produto not in prod.name: 
                scan_site_1(name_produto)
                scan_site_2(name_produto)
                scan_site_3(name_produto)
                break
    dados = {
        'dados': Product.objects.filter(
            name__icontains=name_produto).order_by('price')
    }
        
    return render(requests, 'project/resultados.html', dados)



