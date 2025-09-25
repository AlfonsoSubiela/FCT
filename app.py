#***********************************************************************************
#*                    Script de Web Scraping para obtener las noticias de El Mundo   *
#***********************************************************************************
# import de librerias
import requests
from bs4 import BeautifulSoup

# URL de la pagina a descargar/scrapear

url = "https://www.elmundo.es/"

# Petición HTTP con timeout de 15 segundos
resp = requests.get(url, timeout=15)


# Parseo del HTML con BeautifulSoup usando el parser "lxml"
soup = BeautifulSoup(resp.text, "lxml")

# Selecciona los primeros 5 elementos <article> de la página
articles = soup.find_all("article", limit=5)

    
# Hace un for empezando en el articulo 1
for i, art in enumerate(articles, 1):

    # Extrae texto visible del artículo, limpia espacios y recorta a 100
    title = art.get_text(strip=True)[:100] or "Sin título"

    # Busca la primera etiqueta <a>
    a = art.find("a")

    # Obtiene el href del enlace si existe; si no, marca como no disponible
    href = a["href"] if a and a.has_attr("href") else "No disponible"

    # Muestra el número de la noticia
    print(f"Noticia {i}")

    # Muestra el título
    print("Título:", title)

    # Muestra el enlace
    print("Enlace:", href)


    # Línea separadora
    print("-"*80)

# Muestra si la pagina esta descargada correctamente o no
if resp.status_code == 200:
    print("Pagina descargada correctamente")
else:
    print("Error al descargar la pagina")

    