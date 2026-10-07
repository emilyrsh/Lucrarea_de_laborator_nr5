#Laborator: Descompunerea unui URL
#Student: <Roșca Emilia>

BASE_URL = "https://cybercor.org" 

ECHO_URL = "https://httpbin.org" 

TIMEOUT = 10  # secunde 

print("Ex35")
import urllib
import requests
 
def descompune_url(url):
    # urlparse primește textul și returnează un obiect special cu atribute
    rezultat = urllib.parse.urlparse(url)
    # Accesăm atributele obiectului și le afișăm
    print(f"Scheme (Protocol): {rezultat.scheme}")
    print(f"Netloc (Domeniu):  {rezultat.netloc}")
    print(f"Path (Cale):       {rezultat.path}")
    print(f"Query (Parametri): {rezultat.query}")
    print(f"Fragment (Ancoră): {rezultat.fragment}")
# Definim funcția cu URL-ul din exercițiu
descompune_url("https://cybercor.org/path?x=1#top")

# Laborator: Compunerea URL-urilor
# Student: <Roșca Emilia> 

print("Ex36")
import urllib.parse
def compune_url(base, cai_relative):
    for cale in cai_relative:
        # urljoin se ocupă automat de toată logica de combinare
        url_complet = urllib.parse.urljoin(base, cale)
        # Le afișăm formatat ca să le comparăm mai ușor
        print(f"Relativ: {cale:<15} -> Complet: {url_complet}")
# Folosim un BASE_URL cu o cale ceva mai adâncă pentru a vedea efectul '../'
BASE_URL = "https://cybercor.org/folder/subfolder/pagina.html"
legaturi_de_testat = ["/about", "contact.html", "../index.html"]
compune_url(BASE_URL, legaturi_de_testat)

# Laborator: Extragerea legăturilor
# Student: <Roșca Emilia> 

print("Ex37")
import re
import requests

def extract_links(html):
    legăturile = re.findall(r'href="([^"]+)"', html) 
    legături_unice = list(set(legăturile))
    return legături_unice
    
# Testăm funcția

BASE_URL = "https://cybercor.org"
try:
        # Descărcăm HTML-ul paginii principale
        response = requests.get(BASE_URL, timeout=10)
        # Definim funcția pe textul paginii
        linkuri = extract_links(response.text)
        print(f"Am găsit {len(linkuri)} legături unice:")
        # Afișăm primele 5 linkuri găsite
        for link in linkuri[:5]:
            print(f"- {link}")
except requests.RequestException:
        print("Nu am putut accesa pagina")

# Laborator: Interne sau externe?
# Student: <Roșca Emilia> 

print("Ex38")
import urllib.parse
def split_links(links, domain):
    interne = []
    externe = []
    # Aflăm domeniul principal (netloc) al site-ului nostru
    domeniu_de_bază = urllib.parse.urlparse(domain).netloc
    for link in links:
        # Transformăm legătura într-un URL complet
        url_complet = urllib.parse.urljoin(domain, link)
        # Extragem domeniul legăturii
        domeniu_link = urllib.parse.urlparse(url_complet).netloc
        # Comparăm domeniile pentru a decide unde o adăugăm
        if domeniu_link == domeniu_de_bază:
            interne.append(url_complet)
        else:
            externe.append(url_complet)
    return interne, externe

# Testăm funcția
BASE_URL = "https://cybercor.org"
lista_de_proba = [
    "/despre", 
    "contact.html", 
    "https://google.com/search?q=python", 
    "https://cybercor.org/noutati",
    "http://github.com"
]

# Definim funcția și despachetăm cele 2 liste returnate
linkuri_interne, linkuri_externe = split_links(lista_de_proba, BASE_URL)
print(f"Legături interne ({len(linkuri_interne)}):")
for link in linkuri_interne:
    print(f" - {link}")
print(f"\nLegături externe ({len(linkuri_externe)}):")
for link in linkuri_externe:
    print(f" - {link}")

# Laborator: Propriile metode
# Student: <Roșca Emilia> 

print("Ex39")
from html.parser import HTMLParser

class ImageFinder(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []

    def handle_starttag(self, tag, attrs):
        # Căutăm tag-urile de tip imagine
        if tag == "img":
            # Extragem atributul src
            src = dict(attrs).get("src")
            if src is not None:
                self.images.append(src)

# Testăm funcția
test_html = """ 
<html><body> 
  <img src="/logo.png" alt="Logo"> 
  <IMG SRC="poza.jpg"> 
  <img alt="imagine fără src"> 
  <img src="https://cdn.example.com/banner.webp" /> 
  <a href="/despre">Aceasta nu este o imagine</a> 
</body></html> 
"""

finder = ImageFinder()
finder.feed(test_html)
print("Listă test:", finder.images)
assert finder.images == [
    "/logo.png",                            # imagine obișnuită
    "poza.jpg",                             # tag scris cu majuscule
    "https://cdn.example.com/banner.webp",  # tag care se închide singur
], "Parserul nu a găsit exact imaginile așteptate"
print("Testul a trecut!\n")

# Creăm un obiect NOU ImageFinder pentru pagina reală
try:
    response = requests.get(BASE_URL, timeout=10)
    finder_real = ImageFinder()
    finder_real.feed(response.text)
    print(len(finder_real.images), "imagini găsite pe site.")
    # Afișăm primele 10 imagini
    for src in finder_real.images[:10]:
        print(f" - {src}")
except requests.RequestException:
    print("Eroare la accesarea site-ului real.")

# Laborator: Amprenta paginii
# Student: <Roșca Emilia>  

print("Ex40")
import requests
import hashlib
def page_fingerprint(url):
    try:
        response = requests.get(url, timeout=10)
# hexdigest() transformă rezultatul într-un șir de caractere citibil
        amprenta = hashlib.sha256(response.content).hexdigest()
        return amprenta 
    except requests.RequestException:
     return None

# Testăm funcția
BASE_URL = "https://cybercor.org"
amprenta_1 = page_fingerprint(BASE_URL)
amprenta_2 = page_fingerprint(BASE_URL)
print(f"Prima amprentă:  {amprenta_1}")
print(f"A doua amprentă: {amprenta_2}")
# Comparăm rezultatele
if amprenta_1 == amprenta_2:
    print("\nRezultat: Amprentele sunt IDENTICE.")
else:
    print("\nRezultat: Amprentele sunt DIFERITE.")

# Laborator: Salvarea în JSON
# Student: <Roșca Emilia>  

print("Ex41")
import requests
import json
BASE_URL = "https://cybercor.org"
try:
    response = requests.get(BASE_URL, timeout=10)
    # Transformăm structura de antete a requests într-un dicționar clasic 
    antete_dict = dict(response.headers)
    # Deschidem un fișier numit 'headers.json' în modul scriere
    with open("headers.json", "w") as file:
    # json.dump scrie dicționarul în fișier, iar indent=2 adaugă spații și rânduri noi
     json.dump(antete_dict, file, indent=2)
    print("Antetele au fost cu succes salvate în 'headers.json'.")
    # Deschidem fișierul creat în modul citire
    with open("headers.json", "r") as file:
    # json.load - citește textul din fișier și îl transformă la loc într-un dicționar 
        antete_incarcate = json.load(file)
    # Extragem un antet specific
    antet_cautat = antete_incarcate.get("Content-Type", "Antetul nu a fost găsit")
    print("\nDate încărcate din fișier:")
    print(f"Content-Type: {antet_cautat}")
except requests.RequestException:
    print("Nu am putut accesa site-ul pentru a obține antetele.")

# Laborator: Interogare DNS
# Student: <Roșca Emilia>

print("Ex42")
import socket
def resolve(hostname):
    try:
    # gethostbyname face conversia din nume în IP
        adresa_ip = socket.gethostbyname(hostname)
        return adresa_ip
    except socket.gaierror:
        # gaierror (Get Address Info Error) apare dacă domeniul nu există
        return "Domeniul nu a putut fi găsit"

# Testăm funcția
# Interogarea DNS se face doar pe numele domeniului, deci NU punem "https://" sau "/path" la început.
domeniu = "cybercor.org"
rezultat_ip = resolve(domeniu)
print(f"Adresa IP a domeniului {domeniu} este: {rezultat_ip}")


# Laborator: Expirarea certificatului
# Student: <Roșca Emilia>

print("Ex43")
import socket
import ssl
import time
def cert_days_left(hostname):
# Creăm contextul SSL conform indiciului
 context = ssl.create_default_context()
 try:
    # Creăm conexiunea de rețea de bază
        with socket.create_connection((hostname, 443), timeout=10) as sock:
    # Încapsulăm conexiunea în SSL (tunel criptat)
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
    # Extragem data expirării
                certificat = ssock.getpeercert()
                data_text = certificat["notAfter"]
    # Convertim data expirării în secunde
                expirare_secunde = ssl.cert_time_to_seconds(data_text)
    # Calculăm diferența de timp
                timp_secunde = time.time()
                secunde_rămase = expirare_secunde - timp_secunde
    # Transformăm secundele în zile (24 ore = 3600 secunde)
                zile_rămase = int(secunde_rămase / 86400)
                return zile_rămase
 except Exception as e:
        print(f"A apărut o eroare: {e}")
        return None

# Testăm funcția
domeniu = "cybercor.org"
zile = cert_days_left(domeniu)
if zile is not None:
    print(f"Certificatul pentru {domeniu} mai este valabil {zile} zile.")
    