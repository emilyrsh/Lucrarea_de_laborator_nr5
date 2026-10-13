import sys
import requests

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

SITES = [
    # Pagini obișnuite (Părțile 2, 3 și 4)
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    # Pagini care eșuează
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    # Anteturi de securitate (Partea 5)
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    # Răspunde aleatoriu cu 200 sau 500 (Partea 6)
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]

# Partea 1: Funcții de bază pentru verificarea site-urilor
def build_url(host, path):
    return f"https://{host}/{path}"

def is_https(url):
    if url.startswith("https://"):
        return True
    else:
        return False


# Partea 2: Trimiterea unei cereri GET și afișarea răspunsului
def show_response(url):
    response = requests.get(url)
    print(f"Status: {response.status_code}")
    print(f"Content-Type: {response.headers.get('Content-Type')}")

# Partea 3: Un verificator reutilizabil 
TIMEOUT=5 #secunde
def check_site(url):
    try:
        response = requests.get(url, timeout=TIMEOUT)
        result = {
            "Status": response.status_code,
            "Content-Type": response.headers.get("Content-Type"),
            "Length": len(response.content),
            "Server": response.headers.get("Server"),
        }
    except Exception as e:
        result = {
            "Status": None,
            "Error": str(e)
        }
    if "Server" not in result:
        result["server"] = "unknown"
    if "content" not in result:
        result["content"] = ""
    if "error" not in result:
        result["error"] = ""
    return result


# Partea 4: Verificarea mai multor site-uri
def scan_sites():
    results = []
    for url in SITES:
        result = check_site(url)
        results.append((url, result))
        if result["Status"] == 200:
            print(f"{url}")
    return results

#Partea 5: Audit de securitate
TIMEOUT=5 #secunde
def check_headers(url):
    try:
            response = requests.get(url, timeout=TIMEOUT)
            return {
                "present": [h for h in SECURITY_HEADERS if h in response.headers],
                "missing": [h for h in SECURITY_HEADERS if h not in response.headers],
                "score": len([h for h in SECURITY_HEADERS if h in response.headers]) / len(SECURITY_HEADERS) * 100,
            }
    except Exception as e:
            return {
                "Status": None,
                "Error": str(e)
            }
    
# Partea 6: Încercări repetate 
TIMEOUT=5 #secunde
def retry_check(url, attempts=3):
    for attempt in range(attempts):
        try:
            response = requests.get(url, timeout=TIMEOUT)
        except Exception as e:
            if attempt == attempts - 1:
                return {
                    "Status": None,
                    "Error": str(e),
                    "Attempts": attempts
                }
    return {
        "Status": response.status_code,
        "Attempts": attempt + 1
    }   
if __name__ == "__main__":
    # Exemplu de utilizare a funcțiilor
    print("Scanarea site-urilor...")
    scan_results = scan_sites()
    for url, result in scan_results:
        print(f"{url}: {result}")

    print("\nAudit de securitate...")
    for url in SITES:
        header_result = check_headers(url)
        print(f"{url}: {header_result}")

    print("\nÎncercări repetate...")
    for url in SITES:
        retry_result = retry_check(url)
        print(f"{url}: {retry_result}")
