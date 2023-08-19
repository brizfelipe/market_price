import time
from datetime import datetime
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from ..functions import database
from ..models import Store

def get_produc(driver):
    product = True
    last_product = 0
    caught_products = []
    while product:
        try:
            product_list = driver.find_elements("xpath",'//div[@class="product"]')
            for number_product in range(product_list):
                product_detail = {}
                if not try_click(
                    driver=driver,
                    xpath_click=f'//*[@id="app-container"]/main/div/div/div/div[2]/div[{number_product+1}]',
                    xpath_to_wait_for=f'//*[@id="modal-container"]/div[2]/div/div/div[2]/div/div/div[1]/div/div/div'
                ):
                    continue
                else:
                    url = driver.current_url
                    # img do departamento
                    
                    product_img = driver.find_element("xpath",f'//*[@id="modal-container"]/div[2]/div/div/div[2]/div/div/div[1]/div/div/figure/div/img') 
                    product_detail["img_link"] = product_img.get_attribute('src')

                    product_detail["name"] = driver.find_element("xpath",f'//*[@id="modal-container"]/div[2]/div/div/div[2]/div/div/div[1]/div/div/div/section[1]/h2').text
                    product_detail["price"] = driver.find_element("xpath",f'//*[@id="modal-container"]/div[2]/div/div/div[2]/div/div/div[1]/div/div/div/section[3]/table/tbody/tr[1]/td/span/span').text
                    product_detail['emb'] = driver.find_element("xpath",f'//*[@id="modal-container"]/div[2]/div/div/div[2]/div/div/div[1]/div/div/div/section[3]/table/tbody/tr[2]/td').text
                    product_detail['aisle_id'] = url.split("/")[9]
                    product_detail['product_id'] = url.split("/")[11]
                    product_detail["datetime"] = datetime.now()
                    caught_products.append(product_detail)
                    # voltar
                    driver.find_element("xpath",'//*[@id="modal-container"]/div[2]/div/div/div[1]/div/div[3]/button').click()
            for _ in range(7):
                driver.find_element("xpath",'//body').send_keys(Keys.ARROW_DOWN)
            new_product_list = driver.find_elements("xpath",'//div[@class="product"]')
            if not len(new_product_list) > len(product_list):
                product = False
                

        except Exception as e:
            pass
    


def try_click(driver,xpath_click,xpath_to_wait_for):
    try:
        element_to_click = driver.find_element(By.XPATH, xpath_click)
        element_to_click.click()
        
        wait = WebDriverWait(driver, 10)
        wait.until(EC.visibility_of_element_located((By.XPATH, xpath_to_wait_for)))
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    

    x = 0
    while x < attempt:
        try:
            driver.find_element('xpath',xpath).click()
            time.sleep(1)
            return True
        except Exception as e:
            print(e)
            time.sleep(1)
            x+=1
    
    return False



def init_cornershop(cep):
    print(f'\n\nstart {datetime.now()}')
    driver = create_driver()
    skip_login(driver,cep)
    return driver


def create_driver():
    print('\nAbrindo cornershop')
    try:
        chrome_options = Options()
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://web.cornershopapp.com/")
        time.sleep(5)
        print('--------->Aberto com sucesso!')
        return driver
    except Exception as e:
        print(f'--------->Erro ao abrir: {e}')


def skip_login(driver,cep):
    try:
        print('\nInserir o cep')
        # continuar sem login
        driver.find_element("xpath","//*[@id='modal-container']/div[2]/div/div/div/div[2]/div/button[1]").click() 
        print('--------->continuar sem login')
        time.sleep(1)
        print('\n alterando o local e cep')
        # escolher localização
        driver.find_element("xpath",'//*[@id="app-container"]/header/div[2]/button').click()
        print('--------->Alterar cep')
        time.sleep(1)
        # selecionar brasil
        driver.find_element("xpath",'//*[@id="select-country"]').send_keys('Brasil')
        # alterar o cep
        cep_input = driver.find_element("xpath",'//*[@id="zip-code-input"]')
        cep_input.clear() #limpar campo do cep, pq ja vem u cep padrão
        print('--------->Limpar input do cep atual')
        cep_input.send_keys(cep) # inserir cep novo
        print('--------->Cep alterado')
        # clicar em feito
        driver.find_element("xpath",'//*[@id="modal-container"]/div[2]/div/div[1]/div/div[3]/button').click()
        print('--------->FEITO!')
        time.sleep(2)
        return True
    
    except Exception as e:
        return False


def get_departament(driver):

    for store in Store.objects.all():
            # criar link da loja cadastrada
            print(f'Coleta de departamento da loja: {store.name}' )
            link = f"https://web.cornershopapp.com/store/{store.code}/featured"
            driver.get(link)
            time.sleep(5)
            departamento_list = driver.find_elements("xpath",'//*[@id="app-container"]/main/div/div/section[3]/div/div')
            print('---------> Abrindo pagina do departamento')

            departamento_error = []
            for departamento_number in range(0,len(departamento_list)):
                departamento = departaent(driver,departamento_number,store)
                if not departamento['status']:
                    departamento_error.append(departamento)
            
            if len(departamento_error) > 0:
                try_again = 0
                while try_again < 10 and len(departamento_error) > 0:
                    temp_error_list = []
                    
                    for departament in departamento_error:
                        departamento = departaent(driver, departament['departament_number'], store)
                        if not departamento['status']:
                            time.sleep(1)
                            temp_error_list.append(departament)
                    
                    departamento_error = temp_error_list
                    try_again += 1

    return



def departaent(driver,departamento_number,store)->dict:
    results = {}
    results['Status'] = False
    results['departament_number'] = departamento_number
    results['departament'] = None
    
    try:
        print(f'Pegado departamento da loja: {store.name}')
        # pegar nome do departamento
        departamento_nome = driver.find_element("xpath",f'//*[@id="app-container"]/main/div/div/section[3]/div/div[{departamento_number+1}]/div[1]/h2/span').text
        print(f'---------> Departamento nome: {departamento_nome}')
        # img do departamento
        departamento_img = driver.find_element("xpath",f'//*[@id="app-container"]/main/div/div/section[3]/div/div[{departamento_number+1}]/div[1]/img') 
        departamento_img_link = departamento_img.get_attribute('src')
        print(f'---------> Departamento img ')
        # acessar pagina do departamento para pegar o codigo do departamento
        
        try_access_departaent = 0
        try_back_storePage = 0

        while try_access_departaent < 10:
            try:
                driver.find_element("xpath",f'//*[@id="app-container"]/main/div/div/section[3]/div/div[{departamento_number+1}]/div[1]/button').click()
                time.sleep(5)
                departaento_code = driver.current_url.split('/')[7] # pegar o código na url 
                print(f'---------> Departamento code: {departaento_code} ')
                try_access_departaent = 10
            except Exception:
                time.sleep(1)
                try_access_departaent += 1
        
        while try_back_storePage < 10:
            try:
                driver.find_element('xpath','//*[@id="app-container"]/nav/div[1]/button').click() #voltar para pagina 
                time.sleep(2)
                print(f'---------> Voltando para pagina principal da loja')
                try_back_storePage = 10
            except Exception as e:
                time.sleep(1)
                try_back_storePage +=1

        departament = {
            'store':store,
            'cod' : departaento_code,
            'name' : departamento_nome,
            'image_link' : departamento_img_link
        }

        print(f'--------->Salvando departamento no banco de dados')
        departamento_db = database.save_departament(**departament)
        if not departamento_db:
            print(f'---------> Departamento: {departamento_nome} | code {departaento_code} | Status: False | Detail: Error o salvar departamento')
            return results
        elif departamento_db is True:
            print(f'---------> Departamento: {departamento_nome} | code {departaento_code} | Status: True | Detail: Departaento já salvo')
        else:
            print(f'---------> Departamento: {departamento_nome} | code {departaento_code} | Status: True | Detail: Departaento salvo.')
    
    except Exception as e:
        print(f'--------->Erro em colerar dados do departamento: ERROR: {e}')
        return results
    
    results['status'] = True
    results['departament'] = departament
    return results
