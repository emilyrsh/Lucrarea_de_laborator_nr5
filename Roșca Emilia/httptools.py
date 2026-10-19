import requests

BASE = "https://httpbin.org"
PATHS = ["/get", "/redirect/2", "/delay/1", "/status/404", "/delay/5"]
TIMEOUT = 10  # secunde

# Partea 1: parametri în URL
def search(params):
    try:
        r = requests.get(BASE + "/get", params=params, timeout=TIMEOUT)
        return r.json()["args"]
    except requests.RequestException:
        return None

def search_url(params):
    try:
        r = requests.get(BASE + "/get", params=params, timeout=TIMEOUT)
        return r.url
    except requests.RequestException:
        return None

# Partea 2: anteturi
def fetch_with_agent(agent):
    try:
        headers = {"User-Agent": agent}
        r = requests.get(BASE + "/headers", headers=headers, timeout=TIMEOUT)
        return r.json()["headers"]["User-Agent"]
    except requests.RequestException:
        return None

def default_agent():
    try:
        r = requests.get(BASE + "/headers", timeout=TIMEOUT)
        return r.json()["headers"]["User-Agent"]
    except requests.RequestException:
        return None

# Partea 3: trimiterea datelor
def post_json(data):
    try:
        r = requests.post(BASE + "/post", json=data, timeout=TIMEOUT)
        return r.json()["json"]
    except requests.RequestException:
        return None

def post_form(data):
    try:
        r = requests.post(BASE + "/post", data=data, timeout=TIMEOUT)
        return r.json()["form"]
    except requests.RequestException:
        return None

# Partea 4: coduri de stare
def describe_status(code):
    try:
        r = requests.get(f"{BASE}/status/{code}", allow_redirects=False,timeout=TIMEOUT)
    except requests.RequestException:
        return "eroare de rețea"
    if 200 <= r.status_code < 300:
        return "succes"
    if 400 <= r.status_code < 500:
        return "eroare client"
    if 500 <= r.status_code < 600:
        return "eroare server"
    return "alt cod"

def is_ok(code):
    try:
        r = requests.get(f"{BASE}/status/{code}", timeout=TIMEOUT)
        r.raise_for_status()  # ridică HTTPError pentru 4xx și 5xx
        return True
    except requests.RequestException:
        return False

# Partea 5: redirecționări
def count_redirects(n):
    try:
        r = requests.get(f"{BASE}/redirect/{n}", timeout=TIMEOUT)
        return len(r.history)
    except requests.RequestException:
        return None

def final_url(n):
    try:
        r = requests.get(f"{BASE}/redirect/{n}", timeout=TIMEOUT)
        return r.url
    except requests.RequestException:
        return None


def first_hop(n):
    try:
        # allow_redirects=False: ne oprim la primul răspuns
        r = requests.get(f"{BASE}/redirect/{n}", allow_redirects=False, timeout=TIMEOUT)
        return r.headers.get("Location")
    except requests.RequestException:
        return None


# Partea 6: sesiuni și cookie-uri
def cookie_demo(name, value):
    try:
        with requests.Session() as s:
            s.get(BASE + "/cookies/set", params={name: value}, timeout=TIMEOUT)
            r = s.get(BASE + "/cookies", timeout=TIMEOUT)
            return r.json()["cookies"]
    except requests.RequestException:
        return None

def no_session_demo(name, value):
    try:
        requests.get(BASE + "/cookies/set", params={name: value}, timeout=TIMEOUT)
        r = requests.get(BASE + "/cookies", timeout=TIMEOUT)
        return r.json()["cookies"]  
    except requests.RequestException:
        return None

# Partea 7: raportul final
def report(path):
    try:
        r = requests.get(BASE + path, timeout=3)
        return {
            "status": r.status_code,
            "final_URL": r.url,
            "redirects": len(r.history),
            "seconds": round(r.elapsed.total_seconds(), 2),
            "content_Type": r.headers.get("Content-Type"),
        }
    except requests.Timeout:
        return {"status": None, "error": "timeout"}
    except requests.ConnectionError:
        return {"status": None, "error": "fără conexiune"}
    except requests.RequestException as e:
        return {"status": None, "error": type(e).__name__}

# Bonus: autentificare
def check_login(user, password):
    try:
        r = requests.get(BASE + "/basic-auth/admin/secret", auth=(user, password), timeout=TIMEOUT)
        return r.status_code == 200  
    except requests.RequestException:
        return False
