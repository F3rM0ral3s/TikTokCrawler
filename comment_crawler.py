from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

def getComments(driver):
    try:
        coms = []
        # Encuentra todos los comentarios en ventana
        comment_section = driver.find_element(By.CSS_SELECTOR,'div.css-1qp5gj2-DivCommentListContainer.ekjxngi3')
        ant = 0
        cont=0 
        for i in range(1,15):
            coms = driver.find_elements(By.XPATH,"//span[@dir]")
            tam = len(coms)
            if(ant==tam):
                cont+=1
            else:
                cont=0
            ant=tam
            if(cont==3):
                break
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollTop + {}".format(5000*i), comment_section)
            time.sleep(0.4)

        with open('comments.txt','a', encoding='utf-8') as archivo:
            for com in coms:
                archivo.write(com.text+'\n')

    except Exception as e:
        print('[ Error en comments ]')
        with open('comments.txt','a', encoding='utf-8') as archivo:
            for com in coms:
                archivo.write(com.text+'\n')
                

        

    