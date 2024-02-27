from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

# Inicializamos driver y lista
options = Options()
options.add_argument("--disable-notifications") 
driver = webdriver.Chrome(options=options)

urls = []

# Lanzamos el navegador
driver.get('https://www.tiktok.com')

time.sleep(3)
# Iniciar sesión como invitado
try:
  login_scren = driver.find_element(By.XPATH,"//div[text()='Continuar como invitado']")
  login_scren.click()
except:
   print('No se encontó login screen')

time.sleep(1)
# Se escribe la cabecera de la busqueda en el txt
print('Buscando ','Elecciones 2024 Mexico')
with open('urls.txt','w') as archivo:
   archivo.write('Buscando Elecciones 2024 Mexico\n')

# Se busca videos relacionados con las elecciones de 2024
search = driver.find_element(By.XPATH,"//input[@name='q'][@placeholder='Buscar']")
search.send_keys('Elecciones 2024 Mexico')
search.submit()

time.sleep(5)
# Videos
video = driver.find_element(By.CSS_SELECTOR,'div.css-1soki6-DivItemContainerForSearch.e19c29qe10')
video.click()

'''
  SI TODO SALIO BIEN EN ESTE MOMENTO TENDRAS QUE RESOLVER UN CAPTCHA
  TIENES 10 SEGUNDOS PARA HACERLO
'''
time.sleep(10)
urls.append(driver.current_url)
driver.back()

time.sleep(5)

actions = ActionChains(driver)
keywords = ['sheinbaum','xochitl','morena amlo']
for key in keywords:
  try:
    start = 1
    videos = driver.find_elements(By.CSS_SELECTOR,'div.css-1soki6-DivItemContainerForSearch.e19c29qe10')
    for i in range(100):
      videos = videos[start:]
      for vid in videos:
          print('Links obtenidos %d' % start)
          time.sleep(1.5)
          vid.click()
          time.sleep(1)
          urls.append(driver.current_url)
          time.sleep(0.5)
          driver.back()
          start+=1
      actions.scroll_by_amount(0, 5000).perform()
      time.sleep(1.5)
      videos = driver.find_elements(By.CSS_SELECTOR,'div.css-1soki6-DivItemContainerForSearch.e19c29qe10')
  except Exception as e:
    print(e)
    # Cerramos navegador
    driver.quit()

    # Guardamos las URLs obtenidas
    with open('urls.txt', 'a') as archivo:
        archivo.write('Buscando '+key+'\n')
        for url in urls:
            archivo.write(url+ "\n")
    
    # Generamos una nueva busqueda
    urls = []
    print('Buscando '+key)
    search.send_keys(key)
    search.submit()
    time.sleep(5)
  


# Total de links obtenidos
print('[Links obtenidos %d]' % len(urls))



print('''
  ////////////////////
  FINALIZO EL PROGRAMA
  ////////////////////
''')  
