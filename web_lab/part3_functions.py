# Laborator: Prima funcție
# Student: <Roșca Emilia>

BASE_URL = "https://cybercor.org"

ECHO_URL = "https://httpbin.org"

TIMEOUT = 10 # secunde

print("Ex21")
import requests
response = requests.get(BASE_URL, timeout=TIMEOUT)
def fetch(url):
    return requests.get(url, timeout=TIMEOUT)
print("Status fetch:", fetch(BASE_URL).status_code)

# Laborator: Returnarea unei singure valori
# Student: <Roșca Emilia>

print("Ex22")
import time
def get_status(url):
    response = requests.get(url, timeout=TIMEOUT)
    return response.status_code
paths = ["/", "/robots.txt", "/sitemap.xml"]
print("Verificarea căilor:")
for p in paths:
    code = get_status(BASE_URL + p)
    print(f"{p}:{code}")
    time.sleep(1)

# Laborator: Parametri impliciți
# Student: <Roșca Emilia>

print("Ex23")
def fetch_with_timeout(url, timeout=10):
    return requests.get(url, timeout=TIMEOUT)
print("Cu timeout implicit:", fetch_with_timeout(BASE_URL).status_code)
print("Cu timeout personalizat:",fetch_with_timeout(BASE_URL, timeout=3).status_code)

# Laborator: O singură sarcină pe funcție
# Student: <Roșca Emilia>

print("Ex24")
def get_title(html):
#Găsim punctul de start (imediat după eticheta <title>) 
 start = html.find("<title>") + len("<title>")
#Găsim punctul de final (începutul etichetei </title>)
 end = html.find("<title>")
#Extragem porțiunea de text și o curățăm cu .strip()
 titlu = html[start:end].strip()
#Returnăm rezultatul
 return titlu


# Laborator: Docstring-uri
# Student: <Roșca Emilia>    

print("Ex25")
def get_title(html):
   start = html.find("<title>") + len("<title>")
   end = html.find("</title>")
   return html[start:end].strip()

# Laborator: Adnotări de tip
# Student: <Roșca Emilia>    

print("Ex26")
TIMEOUT = 10
# Am adăugat adnotările de tip: url trebuie să fie 'str' (string), iar funcția returnează 'int' (întreg)
def get_status(url: str) -> int:
    """Returnează codul de stare HTTP pentru adresa url."""
    response = requests.get(url, timeout=TIMEOUT)
    return response.status_code

# Laborator: Fără opriri neașteptate
# Student: <Roșca Emilia>    

print("Ex27")
def page_exists(url):
    # Următoarele rânduri sunt împinse la dreapta cu Tab
    try:
        # Încercăm să accesăm URL-ul primit ca parametru
        requests.get(url, timeout=10)
        # Dacă reușește, returnăm True
        return True
    except requests.RequestException:
        # Dacă dă eroare, returnăm False
        return False
rezultat = page_exists("https://this-domain-does-not-exist.invalid")
print(f"Pagina există? {rezultat}")

# Laborator: Returnarea unui dicționar
# Student: <Roșca Emilia> 

print("Ex28")
def check_paths(base, paths):
    dictionar_status = {} # }n primul rând,este necesar de a crea un dicționar gol pentru a stoca rezultatele
    for path in paths: # Parcurgem fiecare cale din lista primită
        url_complet = base + path # Creăm o adresă
        response = requests.get(url_complet, timeout=10) # Creăm cererea web
# Adăugăm o intrare nouă în dicționar
# Cheia va fi calea: path, iar valoarea va fi statusul: status_code
    dictionar_status[path] = response.status_code
    return dictionar_status
cai_de_verificat = ["/", "/robots.txt", "/sitemap.xml"]
# Definim funcția și salvăm dicționarul returnat
rezultate = check_paths(BASE_URL, cai_de_verificat)
print(rezultate)

# Laborator: Argumente cu nume
# Student: <Roșca Emilia> 

print("Ex29")
#Definim funcția
def get_header(url, name, default="lipsește"):
    response = requests.get(url, timeout=10) #facem cererea către pagina web
    valoare_antet = response.headers.get(name, default) #extragem antetul cu ajutorul instrucțiunii .get a dicționarului de antete
    return valoare_antet
# Definim funcția, utilizând argumente cu nume
rezultat = get_header(url=BASE_URL, name="Server")
print(f"Antetul Server este: {rezultat}")

# Laborator: Antete de securitate 
# Student: <Roșca Emilia> 

print("Ex30")
def security_headers(url):
    # Lista cu antetele pe care le vom căuta
    antete_căutare = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy"
    ]
    rezultate = {}
    try:
    # Facem cererea către URL
     response = requests.get(url, timeout=10)
    # Parcurgem lista de antete
     for antet in antete_căutare:
    # Verificăm dacă antetul există în răspunsul primit de la server
    # 'antet in response.headers' va returna automat True sau False
       rezultate[antet] = antet in response.headers 
    except requests.RequestException:
    # Dacă site-ul nu funcționează, setăm automat False 
     for antet in antete_căutare:
      rezultate[antet] = False
    return rezultate

# Laborator: Funcții care apelează funcții
# Student: <Roșca Emilia>

print("Ex31")
def security_headers(url):
    antete_de_cautat = [
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "Referrer-Policy"
    ]
    rezultate = {}
    try:
        response = requests.get(url, timeout=10)
        for antet in antete_de_cautat:
            rezultate[antet] = antet in response.headers
    except requests.RequestException:
        for antet in antete_de_cautat:
            rezultate[antet] = False
    return rezultate
def score_headers(results):
    # Calculăm lungimea dicționarului
    total = len(results)
    # În Python, True are valoarea 1, iar False - 0.
    # Putem utiliza instrucțiunea sum() pe valorile dicționarului pentru a aduna toți True.
    scor = sum(results.values())
    # Returnăm rezultatul formatat ca 'string'
    return f"{scor}/{total}"

# Definim funcția score_headers și îi atribuim ca argument direct rezultatul funcției security_headers
rezultat_final = score_headers(security_headers(BASE_URL))
print(f"Scorul antetelor de securitate este: {rezultat_final}")

# Laborator: Două funcții, o sarcină
# Student: <Roșca Emilia>

print("Ex32")
def fetch_robots(base):
    url = base + "/robots.txt"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except requests.RequestException:
        return None

def disallowed_paths(robots_text):
    if robots_text is None:
        return []
    cai_interzise = []
    for line in robots_text.splitlines():
        if line.strip().startswith("Disallow:"):
            cale = line.split("Disallow:")[1].strip()
            cai_interzise.append(cale)
    return cai_interzise

text_robots = fetch_robots(BASE_URL)
lista_disallow = disallowed_paths(text_robots)
print(f"Am găsit {len(lista_disallow)} căi interzise:")
print(lista_disallow)

# Laborator: Oricâte argumente
# Student: <Roșca Emilia>

print("Ex33")
import requests
def response_times(*urls):
    timp_raspuns = {}
    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            # '.elapsed' este un obiect care măsoară timpul trecut.
            timp = response.elapsed.total_seconds()
            # Adăugăm în dicționar
            timp_raspuns[url] = timp
        except requests.RequestException:
            # Dacă site-ul nu funcționează, punem valoarea None ca măsură de siguranță
            timp_raspuns[url] = None
    return timp_raspuns
rezultate = response_times("http://cybercor.org", "https://google.com")
print(rezultate)

# Laborator: Argumente cu nume colectate
# Student: <Roșca Emilia>

print("Ex34")
def log(message, **details):
    # Transformăm mesajul principal într-o listă care conține doar acest mesaj
    elemente = [str(message)]
    # Parcurgem dicționarul generat de 'details'
    for cheie, valoare in details.items():
    # Adăugăm fiecare pereche formatată în lista 
        elemente.append(f"{cheie}={valoare}")
    # Unim toate elementele din listă 
    rezultat_final = " | ".join(elemente)
    print(rezultat_final)
# Definim funcția exact ca în exemplu
log("verificat", url=BASE_URL, status=200)
#Print este pentru persoana care citește codul. Are functia de a afișa un text care nu afectează programul cu nimic. 
#Return este pentru program și indică ce valoare trebuie să iasă din îndeplinirea unei condiții/funcții