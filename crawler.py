from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import winsound

import comment_crawler

# Inicializamos driver 
options = Options()
options.add_argument("--disable-notifications") 
driver = webdriver.Chrome(options=options)

# Palabras clave a buscar
keywords = ['Elecciones 2024 Mexico','Sheinbaum','Xochitl Galvez','Morena amlo']

# Se escribe la cabecera de la busqueda en el txt
with open('urls.txt','w') as archivo:
   archivo.write(keywords[0]+'\n')

# Iniciamos txt de comments
with open('comments.txt','w') as archivo:
   archivo.write('-----------------COMMENTS------------------\n')   

actions = ActionChains(driver)
sum=0
for key in keywords:
  # Lanzamos el navegador
  driver.get('https://www.tiktok.com')
  time.sleep(3)

  # Iniciar sesión como invitado
  try:
    login_scren = driver.find_element(By.XPATH,"//div[text()='Continuar como invitado']")
    login_scren.click()
  except:
    print('[[No se encontó login screen]]')


  time.sleep(1)
  # Se busca videos relacionados con las elecciones de 2024
  search =  driver.find_element(By.CSS_SELECTOR,'input.css-1yf5w3n-InputElement.e14ntknm3')
  
  search.send_keys(key)
  search.submit()
  time.sleep(4)

  # Videos
  video = driver.find_element(By.CSS_SELECTOR,'div.css-1soki6-DivItemContainerForSearch.e19c29qe10')
  video.click()

  '''
    SI TODO SALIO BIEN EN ESTE MOMENTO TENDRAS QUE RESOLVER UN CAPTCHA
  '''
  # Esperamos respuesta del usuario
  response = input('Resolviste el captcha [y/n]: ')
  if(response not in ['y','Y']):
    driver.quit()

  # Inicializamos lista de urls
  urls = []
  ########################
  time.sleep(1)
  aux=driver
  comment_crawler.getComments(driver)
  driver=aux
  ########################
  urls.append(driver.current_url)
  sum+=1
  driver.back()

  try:
    start = 1
    # Encuentra todos los placeholder de los videos en ventana
    videos = driver.find_elements(By.CSS_SELECTOR,'div.css-1soki6-DivItemContainerForSearch.e19c29qe10')
    for i in range(100):
      videos = videos[start:]
      for vid in videos:
          print('- Links obtenidos %d' % sum)
          time.sleep(1.5)
          vid.click()
          time.sleep(1)
          ########################
          aux=driver
          comment_crawler.getComments(driver)
          driver=aux
          ########################
          urls.append(driver.current_url)
          sum+=1
          time.sleep(0.5)
          driver.back()
          start+=1
      # Busca mas placeholder dando scrolldown
      actions.scroll_by_amount(0, 4000).perform()
      time.sleep(1.5)
      videos = driver.find_elements(By.CSS_SELECTOR,'div.css-1soki6-DivItemContainerForSearch.e19c29qe10')
  except Exception as e:
    print(e)

    # Guardamos las URLs obtenidas
    with open('urls.txt', 'a') as archivo:
        archivo.write('Buscando '+key+'\n')
        for url in urls:
            archivo.write(url+ "\n")
    
    # Nos encontramos con un Captcha, recargamos la página
    winsound.Beep(1800,2500)
    

# Total de links obtenidos
print('[Links obtenidos %d]' % sum)

# Cerramos navegador
driver.quit()

print('''
  ////////////////////
  FINALIZO EL PROGRAMA
  ////////////////////
''')  
