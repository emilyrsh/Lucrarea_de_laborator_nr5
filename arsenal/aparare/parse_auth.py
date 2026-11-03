# LUCRAREA A (nucleu). parse_auth.py: scoate și numără eșecurile
import re
import sys
from collections import Counter
TIPAR = re.compile(r"Failed password for (?:invalid user )?(\S+) from (\S+) port")

#A1. Scheletul și funcția care întoarce o fișă
def esec(linie):  
# Întoarce (user, ip) dacă rândul e un esec, altfel None
    m = TIPAR.search(linie)
    if m is None:
        return None
    return (m.group(1), m.group(2))

#A2. Lista de eșecuri, robustă la rânduri stricate
def citeste_esecuri(cale):
# Întoarce lista de dicționare {"user", "ip"}; sare peste rândurile stricate
    esecuri = []
    try:
        f = open(cale, encoding="utf-8")
    except FileNotFoundError:
        print("nu gasesc", cale)
        return esecuri
    with f:
        for linie in f:
            r = esec(linie)
            if r is not None:
                esecuri.append({"user": r[0], "ip": r[1]})
    return esecuri

#A3. numărarea pe IP:o funcție cu return
def pe_ip(esecuri):
# Întoarce un Counter al adreselor din eșecuri
    return Counter(e["ip"] for e in esecuri)

#A4. Rezumatul (funcția main)
def main():
    if len(sys.argv) < 2:
        print("folosire: python -m arsenal.aparare.parse_auth <auth.log>")
        return
    esecuri = citeste_esecuri(sys.argv[1])
    print("Eșecuri de autentificare:", len(esecuri))
    for ip, n in pe_ip(esecuri).most_common():
        print(f"{ip}: {n}")

if __name__ == "__main__":
    main()