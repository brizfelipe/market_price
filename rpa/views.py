from django.shortcuts import render
import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
from datetime import datetime
import time 
from selenium.webdriver.common.keys import Keys
from cornershopapp.models import Store,Department
from cornershopapp.functions import database as corneDatabase,selenium
from cornershop import Cornershop


def api(request,cep):
    driver = selenium.init_cornershop(cep)
    # api para pegar as lojas
    cs = Cornershop(
        locality = cep,
        country = 'BR'
    )
    stores = cs.search_branch_groups()[0].items
    stores_json = [store.__dict__ for store in stores]
    stores_fields = [
        {
            'name':store['name'],
            'code':int(store['store_id']),
            'img_url':store['img_url']
        } for store in stores_json
    ]
    print('\nColeta de dados das lojas:')
    for store_field in stores_fields:
        name = store_field['name']
        code = store_field['code']
        store_saved =  corneDatabase.save_store(**store_field)
        if not store_saved:
            print(f'---------> Mercado: {name} | code {code} | Status: False | Detail: Error o salvar mercado')
        elif store_saved is True:
            print(f'---------> Mercado: {name} | code {code} | Statu: True | Detail: Mercado á existente ')
        else:
            print(f'---------> Mercado: {name} | code {code} | Statu: True | Detail: salvo m sucesso!!! ')
    print('\nInicio coleta de dados dos produtos de cada mercado cadastrado.')
   

    # selenium.get_departament(driver)
    
    for store in Store.objects.all(): # for em toda as lojas
        store_code = store.code
        for departament in Department.objects.all():
            departament_code = departament.cod
            link = f'https://web.cornershopapp.com/store/{int(store_code)}/catalog/department/{departament_code}'
            driver.get(link)
            time.sleep(5)
            aisles = driver.find_elements('xpath','//*[@id="app-container"]/main/div/div/div')
            for aisle in range(len(aisles)):
                aisle_name = driver.find_element('xpath',f'//*[@id="app-container"]/main/div/div/div[{aisle+1}]').text.split('\n')[0]
                if aisle_name == 'Em destaque':
                    continue
                pass

            
    pass