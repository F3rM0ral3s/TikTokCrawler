from selenium.webdriver.common.by import By
from openpyxl import Workbook
from openpyxl import load_workbook
from time import sleep
import winsound
import re
import datetime


def createExcel():
    excel = Workbook()
    hoja = excel.active

    # Headers de columna
    headers = ["Descripción","URL","Fecha Publicación","Comentario","Likes"]

    # Imprimimos en el excel
    for col,head in enumerate(headers):
         hoja.cell(row=1,column=col+1,value=head)

    # Fecha de analisis
    hoja.cell(row=1,column=7,value='Fecha de analisis:')
    hoja.cell(row=1,column=8,value=datetime.date.today())

    excel.save("videos_comments.xlsx")

def getComments(driver,url,desc,other_info):

    #Inicializamos lista de comentarios
    coms = []

    # Accedemos al excel
    excel = load_workbook("videos_comments.xlsx")
    hoja = excel.active
    curr = hoja.max_row + 1

    try:
        # Escribimos la descripcion, la url y tratamos la fecha
        hoja.cell(row=curr,column=1,value=desc)
        hoja.cell(row=curr,column=2,value=url)
        hoja.cell(row=curr,column=3,value=re.split('\n',other_info)[2])
        
        # Encuentra la ventan de comentarios
        comment_section = driver.find_element(By.CSS_SELECTOR,'div.css-1qp5gj2-DivCommentListContainer.ekjxngi3')
        
        # Variables auxiliares
        start = 0
        i=1

        # Encuentra todos los comentarios visibles
        coms = driver.find_elements(By.CSS_SELECTOR,'div.css-ulyotp-DivCommentContentContainer.e1g2efjf0')
        while(start!=len(coms)):
            # Acotamos los comments a guardar
            if(len(coms)>=500):
                 break
            
            # Acotamos la lista de comentarios
            coms = coms[start:]

            # Escribimos los comments
            for com in coms:
                # Tenemos que hacerlo ligado para estar seguro que la cantidad
                # de likes y el texto corresponden al mismo comentario

                # Obtenemos el texto
                texto = com.find_element(By.CSS_SELECTOR,'div.css-1mf23fd-DivContentContainer.e1g2efjf1')
                texto = texto.find_element(By.CSS_SELECTOR,'p.css-xm2h10-PCommentText.e1g2efjf6')
                
                # Obtenemos numero de likes
                likes = com.find_element(By.CSS_SELECTOR,'div.css-1swe2yf-DivActionContainer.esns4rh0')
                likes = likes.find_element(By.CSS_SELECTOR,'div.css-114tc9h-DivLikeWrapper.ezxoskx0')
                likes = likes.get_attribute('aria-label')
            
                # Escribimos el texto y likes
                hoja.cell(row=curr,column=4,value=texto.text)
                hoja.cell(row=curr,column=5,value=re.findall('\d+',likes)[0])
                curr+=1
                start+=1

            # Hacemos scroll down
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollTop + {}".format(2500*i), comment_section)
            i+=1
            sleep(1)

            #Buscamos si apareció un captcha
            try:
                driver.find_element(By.CSS_SELECTOR,"div.captcha_verify_container.style__CaptchaWrapper-sc-1gpeoge-0.zGYIR") 
                
                # Esperamos respuesta del usuario
                winsound.Beep(440,2500)
                response = input('[COMMENTS] Resolviste el captcha [y/n]: ')
                if(response not in ['y','Y']):
                    driver.quit()

            except Exception as e:
                 pass

            # Buscamos nuevos comments
            coms = driver.find_elements(By.CSS_SELECTOR,'div.css-ulyotp-DivCommentContentContainer.e1g2efjf0')
            
        # Guardamos
        excel.save("videos_comments.xlsx")   

    except Exception as e:
        print('[ Error en comments ]')
        print('[ Se salvaron %d comentarios ]' % len(coms))
        print(e)
        for com in coms:
                # Tenemos que hacerlo ligado para estar seguro que la cantidad
                # de likes y el texto corresponden al mismo comentario

                # Obtenemos el texto
                texto = com.find_element(By.CSS_SELECTOR,'div.css-1mf23fd-DivContentContainer.e1g2efjf1')
                texto = texto.find_element(By.CSS_SELECTOR,'p.css-xm2h10-PCommentText.e1g2efjf6')
                
                # Obtenemos numero de likes
                likes = com.find_element(By.CSS_SELECTOR,'div.css-1swe2yf-DivActionContainer.esns4rh0')
                likes = likes.find_element(By.CSS_SELECTOR,'div.css-114tc9h-DivLikeWrapper.ezxoskx0')
                likes = likes.get_attribute('aria-label')
            
                # Escribimos el texto y likes
                hoja.cell(row=curr,column=4,value=texto.text)
                hoja.cell(row=curr,column=5,value=re.findall('\d+',likes)[0])
                curr+=1
                start+=1  
        excel.save("videos_comments.xlsx")          