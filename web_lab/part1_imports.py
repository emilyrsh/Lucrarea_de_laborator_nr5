# Laborator: Primul import
# Student: <Roșca Emilia>

BASE_URL = "https://cybercor.org"

ECHO_URL = "https://httpbin.org"

TIMEOUT = 10 # secunde
print("Ex1")
import requests
import urllib.request
print ("Versiunea requests:", requests.__version__)
# requests este o bibliotecă externă, de aceea a avut nevoie de ”pip install”.
# urlib face parte din biblioteca standard Python, deci nu necesită instalare.

# Laborator: Două stiluri de import
# Student: <Roșca Emilia>

print("Ex2")
import requests
requests.get(BASE_URL, timeout=TIMEOUT)

# Laborator: Alias-uri
# Student: <Roșca Emilia>

print("Ex3")
import requests as rq
response = rq.get(BASE_URL, timeout=TIMEOUT)
print ("Status cu alias:", response.status_code)
# Aliasul face codul mai ușor de citit când numele modulului este foarte lung
# Aliasul face codul mai greu de citit când porecla nu are legătură cu modulul

# Laborator: Doar biblioteca standard
# Student: <Roșca Emilia>

print("Ex4")
import urllib.request
#Definim un User-Agent de browser pentru a nu fi blocați cu eroarea 403
headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
#Creăm un request care va include adresa și heads de browser
req = urllib.request.Request(BASE_URL, headers=headers)
#Trimitem cererea folosind Request configurat
with urllib.request.urlopen(req) as response:
 status_code = response.status
 raw_body = response.read()
 text_body = raw_body.decode("utf-8")
 print(f"Status: {status_code}")
 print(text_body[:200])

 #Laborator: Privirea în interiorul unui modul
 #Student: Roșca Emilia

print("Ex5")
import requests
# Afișăm toate numele disponibile în modulul requests
print(dir(requests))
# Verificăm tipul a trei nume alese din rezultat
print(type(requests.get)) #requests.get arată dacă este o funcție
print(type(requests.Session)) #requests.Session arată dacă este o clasă
print(type(requests.exceptions)) #requests.exceptions arată dacă este un modul

#Laborator: Citirea documentației
#Student: Roșca Emilia

print("Ex6")
help(requests.get)
# Trimitem o cerere GET folosind parametrul timeout setat la 10 secunde
response = requests.get(BASE_URL, timeout=10)
# Afișăm codul de stare HTTP al răspunsului
print(f"Status: {response.status_code}")
# Afișăm primele 200 de caractere din corpul răspunsului folosind felierea (slicing)
print(response.text[:200])

# Laborator: Cronometrarea unei cereri
# Student: <Roșca Emilia>

print("Ex7")
import time
# Salvăm momentul de timp exact înainte de lansarea cererii folosind time.perf_counter()
start_time = time.perf_counter()
# Trimitem cererea GET către pagina principală
response = requests.get(BASE_URL, timeout=10)
# Salvăm momentul de timp imediat după ce am primit răspunsul complet
end_time = time.perf_counter()
# Calculăm durata totală scursă măsurată manual cu modulul time
durata_time = end_time - start_time
# Afișăm rezultatul măsurat manual și cel oferit nativ de obiectul response
print(f"Timp măsurat cu time.perf_counter(): {durata_time:.6f} secunde")
print(f"Timp măsurat de biblioteca requests (response.elapsed): {response.elapsed.total_seconds()} secunde")

# Laborator: Importul eșuează
#Student: <Roșca Emilia>

print("Ex8")
requests.get(timeout = TIMEOUT)
try:
    import bs4
except ImportError:
    print("Instalați modulul cu: pip install beautifulsoup4")
# Modul: Un singur fișier Python (.py).
# Pachet: Un folder care conține mai multe module.
# Bibliotecă: O colecție amplă de pachete și module gata de folosit (ex: requests, urllib)