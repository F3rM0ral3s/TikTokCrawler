from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import winsound

import comment_crawler

# Inicializamos driver 
options = Options()
options.add_argument("--disable-notifications") 
driver = webdriver.Chrome(options=options)

# Creamos excel
comment_crawler.createExcel()

# Palabras clave a buscar
keywords = ['Elecciones 2024 Mexico','Sheinbaum','Xochitl Galvez','Morena amlo']

# Inicializamos las acciones del navegador y una variable sumador
actions = ActionChains(driver)
sum=1

for key in keywords:
  # Lanzamos el navegador
  driver.get('https://www.tiktok.com')
  sleep(3)

  # Iniciar sesión como invitado
  try:
    login_scren = driver.find_element(By.XPATH,"//div[text()='Continuar como invitado']")
    login_scren.click()
  except:
    print('[[No se encontó login screen]]')
  sleep(1)


  # Se busca videos relacionados con las elecciones de 2024
  search =  driver.find_element(By.CSS_SELECTOR,'input.css-1yf5w3n-InputElement.e14ntknm3')
  search.send_keys(key)
  search.submit()
  sleep(5)

  print('Buscando %s' % key)

  try:
    start = 0
    # Encuentra todos los placeholder de los videos en ventana
    videos = driver.find_elements(By.CSS_SELECTOR,'div.css-1soki6-DivItemContainerForSearch.e19c29qe10')
    for i in range(100):

      # Esta lista es de los tiktoks en pantalla que no hemos analizado
      videos = videos[start:]

      for vid in videos:
          # Printeamos el num de videos analizados
          # y entramos al tiktok
          print('- Videos analizados %d' % sum)
          sleep(3)
          driver.execute_script("arguments[0].scrollIntoView(true);", vid)
          sleep(1)
          vid.click()
          sleep(2.5)

          # Buscamos captcha
          try:
            driver.find_element(By.CSS_SELECTOR,"div.captcha_verify_container.style__CaptchaWrapper-sc-1gpeoge-0.zGYIR") 
            
            # Esperamos respuesta del usuario
            winsound.Beep(440,2000)
            response = input('[VIDEOS] Resolviste el captcha [y/n]: ')
            if(response not in ['y','Y']):
                driver.quit()

          except Exception as e:
            pass
          
          # Obtenemos batch de comentarios
          aux=driver
          url = driver.current_url
          desc = driver.find_element(By.XPATH,'//div[@data-e2e="browse-video-desc"]')
          other_info = driver.find_element(By.CSS_SELECTOR,'span.css-gg0x0w-SpanOtherInfos.evv7pft3')
          comment_crawler.getComments(driver,url,desc.text,other_info.text)
          driver=aux
          
          sum+=1
          start+=1
          driver.back()

      videos = driver.find_elements(By.CSS_SELECTOR,'div.css-1soki6-DivItemContainerForSearch.e19c29qe10')


  except Exception as e:
    print(e)


# Total de videos y comments
print('[Total de videos analizados %d]' % sum)

# Cerramos navegador
driver.quit()

print('''
  ////////////////////
  FINALIZO EL PROGRAMA
  ////////////////////
''')  