# Laborator: Elementele de bază ale răspunsului
# Student: <Roșca Emilia>

BASE_URL = "https://cybercor.org"

ECHO_URL = "https://httpbin.org"

TIMEOUT = 10 # secunde

print("Ex9")
import requests
response = requests.get(BASE_URL, timeout=TIMEOUT)
print("status_code:", response.status_code)
print("ok:", response.ok) #atribut
print("url:", response.url ) #atribut
print("encoding:", response.encoding) #atribut

# Laborator: Tratarea erorilor cu o metodă 
# Student: <Roșca Emilia>

print("Ex10")
try:
    response = requests.get(BASE_URL, timeout=TIMEOUT)
    response.raise_for_status()
    print("Pagina principală OK.")
except requests.HTTPError as e:
    print("Eroare HTTP:", e)

try:
    response = requests.get(BASE_URL + "/this-page-does-not-exist", timeout=TIMEOUT)
    response.raise_for_status()
except requests.HTTPError:
    print("Pagina căutată nu există.")

# Laborator: Toate antetele
# Student: <Roșca Emilia>

print("Ex11")
response = requests.get(BASE_URL, timeout=TIMEOUT)
response.headers.items() 
for Nume, value in response.headers.items():
    print(f"{Nume}: {value}")

# Laborator: Metode de dicționar
# Student: <Roșca Emilia>

print("Ex12")
response = requests.get(BASE_URL, timeout=TIMEOUT)
print(f"Server:", response.headers.get("Server", "lipsește"))
print(f"Content-Type:",response.headers.get("Content-Type", "lipsește") )
print(f"server:", response.headers.get("server", "lipsește"))
print(f"content-type:",response.headers.get("content-type", "lipsește") )
#Observație: antetele HTTP sunt caseinsensitive, deci se afișează același lucru, indiferent dacă îi scrsi cu majusculă sau minusculă

# Laborator: Înlănțuirea metodelor de șir
# Student: <Roșca Emilia>

print("Ex13")
import requests
response = requests.get(BASE_URL, timeout=TIMEOUT)
count = response.text.lower().count("cyber")
print("Apariții cuvântului 'cyber':", count)
#Putem înlănțui .lower() și .count() deoarece atributul response.text este un șir de caractere (string).
#Când aplicăm .lower(), aceasta returnează la rândul ei tot un obiect de tip șir de caractere (string).
#Pentru că rezultatul este un string valid, putem apela imediat pe el o altă metodă specifică string-urilor, cum este .count().                                                           

# Laborator: Găsirea titlului
# Student: <Roșca Emilia>

print("Ex14")
import requests
response = requests.get(BASE_URL, timeout=TIMEOUT)
#Căutăm poziția de început și sfârșit a etichetei <title>
start = response.text.find("<title>") + len("<title>") 
end = response.text.find("</title>") 
title = response.text[start:end].strip()
print("Titlul paginii:", title)

# Laborator: Numărarea liniilor
# Student: <Roșca Emilia>

print("Ex15")
import requests
response = requests.get(BASE_URL, timeout=TIMEOUT)
lines = response.text.splitlines()
longest_line = max(lines, key=len) 
print(f"Număr linii: {len(lines)}, Lungimea celei mai lungi linii: {len(longest_line)}")

# Laborator: Verificarea HTTPS
# Student: <Roșca Emilia>

print("Ex16")
import requests
response = requests.get(BASE_URL, timeout=TIMEOUT)
if response.url.startswith("https://"): print("Conexiune securizată") 
else: print("Conexiune nesecurizată")

# Laborator: Urmărirea redirecționărilor
# Student: <Roșca Emilia>

print("Ex17")
import requests
response = requests.get(BASE_URL, timeout=TIMEOUT)
http_response = requests.get("http://cybercor.org", timeout=TIMEOUT) 
print("Istoric redirecționări:") 
for resp in http_response.history: print(f"  {resp.status_code} -> {resp.url}") 
print(f"URL final: {http_response.url}")

# Laborator: HEAD versus GET
# Student: <Roșca Emilia>

print("Ex18")
import requests
response = requests.get(BASE_URL, timeout=TIMEOUT)
head_resp = requests.head(BASE_URL, timeout=TIMEOUT) 
get_resp = requests.get(BASE_URL, timeout=TIMEOUT) 
print(f"Lungime HEAD: {len(head_resp.content)}, Lungime GET: {len(get_resp.content)}")
#Cererea HEAD returnează doar antetele (fără corp/conținut), deci len(content) este 0.
#Cererea GET descarcă întregul conținut HTML al paginii.

# Laborator: Cookie-uri
# Student: <Roșca Emilia>

print("Ex19")
import requests
response = requests.get(BASE_URL, timeout=TIMEOUT)
if response.cookies: 
    for cookie in response.cookies: print(f"Cookie: {cookie.name}, Secure: {cookie.secure}") 
else: print("Niciun cookie setat")

# Laborator: Sesiuni
# Student: <Roșca Emilia>

print("Ex20")
import requests
response = requests.get(BASE_URL, timeout=TIMEOUT)
session = requests.Session() 
session.headers.update({"User-Agent": "WebLab-Student"}) 
echo_response = session.get(ECHO_URL + "/headers", timeout=TIMEOUT) 
print("Exercițiul 20 - Antete trimise către server:") 
print(echo_response.json().get("headers", {}).get("User-Agent"))

