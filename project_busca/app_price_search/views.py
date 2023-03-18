# from pprint import pprint
from django.shortcuts import render
from utils.scrapy_search_price import scan_site_1, scan_site_2, scan_site_3

from .models import Product


def pesquisar(request):
    return render(request, 'project/pesquisa.html')


def exibir_resultados(requests):
    name_produto = requests.POST.get('produto')
    produto = Product.objects.filter(name__icontains=name_produto)
    if not produto.exists():
        print(False)
        if not name_produto.isdigit() and name_produto != '':
            print('pass digitoooo')
            scan_site_1(name_produto)
            scan_site_2(name_produto)
            scan_site_3(name_produto)
    else: 
        print(True)
        print('pass else')
        
    dados = {
        'dados': Product.objects.filter(
            name__icontains=name_produto).order_by('price')
    }
        
    return render(requests, 'project/resultados.html', dados)



