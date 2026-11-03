# Lucrarea B: Detector de brute force cu prag reglabil și raport JSON
import argparse
import json
from collections import Counter

try:
    from arsenal.aparare.parse_auth import citeste_esecuri, pe_ip
except ModuleNotFoundError:
    from parse_auth import citeste_esecuri, pe_ip

# B1. suspecti() cu valoare implicită și validare
def suspecti(counts, prag=10):
# Întoarce lista (ip, n) cu n >= prag, sortată descrescător după n
    if prag < 1:
        raise ValueError(f"prag invalid: {prag} (cel puțin 1)")
    sus = [(ip, n) for ip, n in Counter(counts).items() if n >= prag]
    return sorted(sus, key=lambda x: x[1], reverse=True)

#B3. Argparse și raportul JSON
def main():
    p = argparse.ArgumentParser()
    p.add_argument("log")
    p.add_argument("--prag", type=int, default=10)
    p.add_argument("--json", action="store_true")
    a = p.parse_args()

    esecuri = citeste_esecuri(a.log)
    counts = pe_ip(esecuri)
    sus = suspecti(counts, a.prag)

    if a.json:
        print(json.dumps({
            "esecuri": len(esecuri),
            "pe_ip": dict(counts.most_common()),
            "suspecti": [{"ip": ip, "incercari": n} for ip, n in sus],}, indent=2))
    else:
        print("Eșecuri de autentificare:", len(esecuri))
        for ip, n in counts.most_common():
            print(f"{ip}: {n}")
        print(f"Suspecti (prag {a.prag}):")
        for ip, n in sus:
            print(f"{ip} ({n} incercari) BRUTE FORCE")


if __name__ == "__main__":
    main()