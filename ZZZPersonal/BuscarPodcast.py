from bs4 import BeautifulSoup
import requests
from DescargarPodcast import *

URL = "https://www.ivoox.com/podcast-voz-horus-warhammer-40k_sq_f1394221_1.html"

# Realizamos la petición a la web
req = requests.get(URL)
status_code = req.status_code

if status_code == 200:

    # Pasamos el contenido HTML de la web a un objeto BeautifulSoup()
    html = BeautifulSoup(req.text, "html.parser")

    # Obtenemos todos los divs donde están las entradas
    entradas = html.find('p',{'class': 'title-wrapper text-ellipsis-multiple'})

    # Recorremos todas las entradas para extraer el título y el link

    for row in entradas.find_all('a'):
        link = row.get('href')
        titulo = row.get('title')
        print("%s \n\t %s" % (titulo, link))

    f = open('links.txt', 'r')
    mensaje = f.read()
    f.close()

    if mensaje == link:
        print("Mismo link")
    else:
        f = open('links.txt', 'w')
        f.write(link)
        f.close()
        descargar()

else:
    print ("Status Code %d" % status_code)








