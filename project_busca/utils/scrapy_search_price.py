from datetime import datetime

import psycopg2
from selenium import webdriver
from selenium.common.exceptions import (ElementNotSelectableException,
                                        ElementNotVisibleException,
                                        NoSuchElementException)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as condicao_esperada
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


conexao = psycopg2.connect(
    database='railway',
    user='postgres',
    password='LYzhwFvVJH2zg31TdHjR',
    host='containers-us-west-46.railway.app',
    port='7327'
)


sql = conexao.cursor()


def new_product(sql, conexao, name, price, site, link_image, quote_date):
    query = "SELECT * FROM app_price_search_product WHERE name=%s and price=%s and site=%s"
    values = (name, price, site)
    result = sql.execute(query, values)
    dados = sql.fetchall()
    
    if len(dados) == 0:
        query = 'INSERT INTO app_price_search_product(name, price, site, quote_date, link_image) VALUES( %s, %s, %s, %s, %s)'
        values = (name, price, site, quote_date, link_image)
        sql.execute(query, values)
    else:
        print('Dados já cadastrados')
        

    conexao.commit()    


def start_driver():
    chrome_options = Options()
     #--headless    
    arguments = ['--lang=en-US', '--window-size=1920,1080',
                 '--incognito',] 
        
    for argument in arguments:
        chrome_options.add_argument(argument)     
        
    chrome_options.add_experimental_option('prefs', {
        'download.prompt_for_download': False, 
        'profile.default_content_setting_values.notifications': 2,
        'profile.default_content_settings_values.automatic_downloads': 1
    })
    
    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager().install()), options=chrome_options)
    wait = WebDriverWait(
        driver,
        15,
        poll_frequency=1,
        ignored_exceptions=[NoSuchElementException, ElementNotVisibleException, ElementNotSelectableException])
    return driver, wait



def scan_site_1(item):
    #casas bahia
    produto = item.replace(' ', '-')
    driver, wait = start_driver()
    driver.get('https://www.casasbahia.com.br/'+produto+'/b')
    names = wait.until(condicao_esperada.visibility_of_all_elements_located((By.XPATH, '//div[@class="sc-2b5b888e-0 jEybNn"]/h3')))
    prices = wait.until(condicao_esperada.visibility_of_all_elements_located((By.XPATH, '//div[@class="sc-c0914aad-2 hdvMuk"]/span[@class="sc-c0914aad-9 hTVULn"]' )))
    site = driver.current_url                                                                  
    link_image = wait.until(condicao_esperada.visibility_of_all_elements_located((By.XPATH, '//div[@class="sc-b78556c4-5 jkQmcY"]/span/img'))) 
    #limpa os dados para entrar somente o necessario no banco de dados
    name = names[0].text
    price1 = prices[0].text.split(' ')[2].replace('.','')
    price = price1.replace(',', '.')
    image = link_image[0].get_attribute('src')
    
    new_product(sql, conexao, name, price, site, image, datetime.now())
    print("ok1")
    
def scan_site_2(item):
    #magazine luiza
    produto = item.replace(' ', '+')
    driver, wait = start_driver()
    driver.get('https://www.magazineluiza.com.br/busca/'+produto+'/')
    names = wait.until(condicao_esperada.visibility_of_all_elements_located((By.XPATH, '//div[@class="sc-cnOiCc kMzkrA"]/h2')))
    prices = wait.until(condicao_esperada.visibility_of_all_elements_located((By.XPATH, '//div[@class="sc-hLBbgP blWoJz sc-gGfaQS dhvIhC"]/p[@class="sc-kDvujY jDmBNY sc-hGglLj bQqJoc"]' )))
    site = driver.current_url                                                                  
    link_image = wait.until(condicao_esperada.visibility_of_all_elements_located((By.XPATH, '//div[@class="sc-eQVdPn clJokE"]/img'))) 
    #limpa os dados para entrar somente o necessario no banco de dados
    name = names[0].text.split("”")[0]
    price1 = prices[0].text.split(' ')[1].replace('.', '')
    price = price1.replace(',', '.')
    image = link_image[0].get_attribute('src')
    #cadastra novo produto no banco de dados
    new_product(sql, conexao, name, price, site, image, datetime.now())
    print("ok2")
    
def scan_site_3(item):
    #mercado livre
    produto = item.replace(' ', '-')
    driver, wait = start_driver()
    driver.get('https://lista.mercadolivre.com.br/' + produto)
    names = wait.until(condicao_esperada.visibility_of_all_elements_located((By.XPATH, '//div[@class="ui-search-item__group ui-search-item__group--title shops__items-group"]/a[@class="ui-search-item__group__element shops__items-group-details ui-search-link"]/h2')))
    prices = wait.until(condicao_esperada.visibility_of_all_elements_located((By.XPATH, '//div[@class="ui-search-price__second-line shops__price-second-line"]/span[@class="price-tag ui-search-price__part shops__price-part"]/span[@class="price-tag-text-sr-only"]')))
    site = driver.current_url
    link_image = wait.until(condicao_esperada.visibility_of_all_elements_located((By.XPATH, '//div[@class="slick-slide slick-active"]/img')))
    #limpa os dados para entrar somente o necessario no banco de dados
    name = names[0].text.split('-')[0]
    price = prices[0].text.split(' ')[0]
    image = link_image[0].get_attribute('src')
    
    new_product(sql, conexao, name, price, site, image, datetime.now())
    print("ok3")

