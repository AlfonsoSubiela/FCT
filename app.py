#***********************************************************************************
#*                    Script de Web Scraping para obtener las noticias de El Mundo   *
#***********************************************************************************
# import de librerias
import requests
from bs4 import BeautifulSoup
import re
import sqlite3
from flask import Flask, render_template


# --- Flask app para mostrar las noticias guardadas ---
app = Flask(__name__)



def scrapear_y_guardar():
    conn = sqlite3.connect("noticias.db")
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS noticias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT,
            enlace TEXT,
            fecha TEXT,
            autor TEXT,
            seccion TEXT,
            contiene_ayuntamiento INTEGER
        )
    ''')
    conn.commit()
    cur.execute("SELECT COUNT(*) FROM noticias")
    if cur.fetchone()[0] == 0:
        url = "https://www.elmundo.es/"
        resp = requests.get(url, timeout=15)
        soup = BeautifulSoup(resp.text, "lxml")
        articles = soup.find_all("article", limit=10)
        for art in articles:
            text = art.get_text(separator=" ", strip=True)[:150] or "Sin texto"
            a = art.find("a")
            href = a["href"] if a and a.has_attr("href") else "No disponible"
            fecha_regex = r"(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}-\d{2}-\d{2})"
            fechas = re.findall(fecha_regex, text)
            fecha = fechas[0] if fechas else "No encontrada"
            contiene_ayuntamiento = bool(re.search(r"ayuntamiento", text, re.IGNORECASE))
            autor = "No encontrado"
            seccion = "No encontrada"
            for tag in art.find_all(["span", "div", "p"]):
                if tag.has_attr("class"):
                    clase = " ".join(tag["class"]).lower()
                    if "autor" in clase or "firma" in clase:
                        autor = tag.get_text(strip=True)
                    if "seccion" in clase or "section" in clase:
                        seccion = tag.get_text(strip=True)
            cur.execute('''
                INSERT INTO noticias (titulo, enlace, fecha, autor, seccion, contiene_ayuntamiento)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (text[:100], href, fecha, autor, seccion, int(contiene_ayuntamiento)))
            conn.commit()
    conn.close()

@app.route("/")
def mostrar_noticias():
    scrapear_y_guardar()
    conn = sqlite3.connect("noticias.db")
    cur = conn.cursor()
    cur.execute("SELECT titulo, enlace, fecha, autor, seccion, contiene_ayuntamiento FROM noticias")
    noticias = cur.fetchall()
    conn.close()
    return render_template('index.html', noticias=noticias)

if __name__ == "__main__":
    app.run(debug=True)

    