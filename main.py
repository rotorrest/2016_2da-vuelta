import time
import re
import lxml
import undetected_chromedriver as uc
import pandas as pd

from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from html_table_extractor.extractor import Extractor

from core import web 

#headless
options = uc.ChromeOptions()
#options.headless=True
#options.add_argument('--headless')
driver = uc.Chrome(options=options)

#head
#driver = uc.Chrome(options=options)

#variables
url_base = 'https://www.web.onpe.gob.pe/modElecciones/elecciones/elecciones2016/PRP2V2016/Actas-por-numero.html#posicion'
text_fake = "EL NÚMERO DE MESA QUE HA INGRESADO NO EXISTE"
j_fake = 0 
restartchrome = 500
j = 0
columns = ['num_mesa', 'num_copia', 'departamento', 'provincia', 'distrito', 'local', 'direccion', 'electores_habiles', 'total_votantes', 'estado_acta', 'ppk', 'fp', 'votos_blanco', 'voto_nulos', 'votos_impugnados', 'votos_emitidos']

#Mesas
x = range(1,1000000)
list_mesas = []
for i in x:
  i = str(i)
  if len(i) == 1:
    i = '00000'+i
    list_mesas.append(i)
  elif len(i) == 2:
    i = '0000'+i
    list_mesas.append(i)
  elif len(i) == 3:
    i = '000'+i
    list_mesas.append(i)
  elif len(i) == 4:
    i = '00'+i
    list_mesas.append(i)
  elif len(i) == 5:
    i = '0'+i
    list_mesas.append(i)
  elif len(i) == 6:
    list_mesas.append(i)

#create csv
df = pd.DataFrame( columns = columns)
df. to_csv("r.csv")

start = int(input('Start: '))
end = int(input('end: '))
for mesa in tqdm(list_mesas[start:end], ncols=50):

    if j % restartchrome == 0 and j != 0:
        driver.close()
        driver = uc.Chrome(options=options)
    
    j = j + 1 
    
    driver.get(url_base)

    input_mesa = driver.find_element_by_id('nroMesa')
    input_mesa.send_keys(mesa)

    button = driver.find_element_by_xpath('/html/body/div/section[2]/div/div[2]/div/div[2]/div[2]/form/div[3]/button')

    button.click()
    
    s = driver.page_source
    s = BeautifulSoup(s, 'lxml')
    
    if re.search(text_fake, s.text): #detecs fake mesas
        print('fake: ' + str(j_fake) )
        j_fake = j_fake + 1
    else:
        results = web.run(s)
        results = list(results)
        
        item = {}
        item['num_mesa'] = results[0]
        item['num_copia'] = results[1]
        item['departamento'] = results[2]
        item['provincia'] = results[3]
        item['distrito'] = results[4]
        item['local'] = results[5]
        item['direccion'] = results[6]
        item['electores_habiles'] = results[7]
        item['total_votantes'] = results[8]
        item['estado_acta'] = results[9]
        item['ppk'] = results[10]
        item['fp'] = results[11]
        item['votos_blanco'] = results[12]
        item['voto_nulos'] = results[13]
        item['votos_impugnados'] = results[14]
        item['votos_emitidos'] = results[15]
        
        
        df = df.append(item, ignore_index=True)
        df. to_csv("r.csv")
