import argparse
import hashlib
import os
import re
import base64
import json
from pathlib import Path
from urllib.parse import unquote

INTRARE_DEMO = "53616c7574"

print("A1: Text și octeți.Încălzirea")
def demo_text_octeți():
    s = "salut"
    b = s.encode() #bytes
    print(f"Bytes: {b}, Primul octet (în codul ASCII): {b[0]}")    
    # TODO A1: tipareste b.hex() si refa bytes din hex
    h = b.hex()
    print(f"Hex: {h}")
    b_refăcut = bytes.fromhex(h)
    print(f"Bytes refăcuți din hex: {b_refăcut}")
    
print("A2: Recunoști stratul după formă")
def ghicim_stratul(s):
    if "%" in s:
        return "url"
    # Daca doar 0-9 a-f/A-F si lungime para -> "hex"
    if re.fullmatch(r"[0-9a-fA-F]+", s) and len(s) % 2 == 0:
        return "hex"
    # Daca doar A-Za-z0-9+/= -> "base64"
    if re.fullmatch(r"[A-Za-z0-9+/=]+", s) and len(s) % 4 == 0:
        return "base64"
    return "necunoscut"

print("A3: Desface stratul recunoscut")
def desfacem(s: str):
    strat = ghicim_stratul(s)
    if strat == "base64":
        try:
            return strat, base64.b64decode(s)
        except Exception:
            return "necunoscut", s.encode()
    if strat == "hex":
        try:
            return strat, bytes.fromhex(s)
        except Exception:
            return "necunoscut", s.encode()
    if strat == "url":
        return strat, unquote(s).encode()
    return "necunoscut", s.encode()

print("A4: Verificare dacă un buchet de octeți e text citibil")
def citibil(b):
    # True daca toti octetii sunt caractere ASCII imprimabile (32..126)
    return all(32 <= c < 127 for c in b)

def desfă_multistrat(val_inițială):
    val = val_inițială
    straturi_parcurse = []
    for _ in range(8):
        strat, b = desfacem(val)
        if strat == "necunoscut":
            break
        straturi_parcurse.append(strat)
        if citibil(b):
            return straturi_parcurse, b.decode('latin1')
        try:
            val = b.decode('utf-8')
        except UnicodeDecodeError:
            try:
                val = b.decode('latin1')
            except Exception:
                break
    return straturi_parcurse, val

print("A5: Spargi un XOR cu cheie de un octet")
def sparge_xor(date):
    for k in range(256):
        clar = bytes(b ^ k for b in date)
        if citibil(clar):
            return k, clar.decode('utf-8', errors='ignore')
    return None, None

print("A6: Spargi un hash prin dicționar")
def sparge_hash(cale_hashuri="probe/hashuri.txt", cale_wordlist="probe/wordlist.txt"):
    try:
        țintă = open(cale_hashuri).readline().strip()
    except FileNotFoundError:
        return None, None
    lungime = len(țintă)
    algoritm = "md5" if lungime == 32 else ("sha1" if lungime == 40 else "sha256")

    try:
        with open(cale_wordlist, encoding="latin1") as f:
            for linie in f:
                cuv = linie.strip()
                h = getattr(hashlib, algoritm)(cuv.encode()).hexdigest()
                if h == țintă:
                    return țintă, cuv
    except FileNotFoundError:
        pass
    return țintă, None


print("A7: argparse și fișa JSON")
def main():
    p = argparse.ArgumentParser(description="Decoder universal forensics")
    p.add_argument(
        "intrare",
        nargs="?",
        help="Șir de text sau cale către fișier (implicit: text demonstrativ)",
    )
    moduri = p.add_mutually_exclusive_group()
    moduri.add_argument("--fisier", action="store_true", help="Tratează intrarea ca fișier binar pentru XOR")
    moduri.add_argument("--sparge-hash", action="store_true", help="Sparge hash-ul din probe/hashuri.txt")
    a = p.parse_args()
    if a.fisier and a.intrare is None:
        p.error("intrare este necesară pentru decodare sau pentru modul --fisier")
    rezultat_json = {}
    if a.sparge_hash:
        hash_tinta, parola = sparge_hash()
        print(f"[Hash] Țintă: {hash_tinta} -> Parola găsită: {parola}")
        rezultat_json = {"tip": "hash", "hash": hash_tinta, "rezultat": parola}
    elif a.fisier:
        # Citeste octeții din cale
        try:
            date = open(a.intrare, "rb").read()
            cheie, text_clar = sparge_xor(date)
            print(f"[XOR] Cheie găsită: {cheie} (0x{cheie:02x}) -> Text: {text_clar}")
            rezultat_json = {"tip": "xor", "cheie": cheie, "rezultat": text_clar}
        except FileNotFoundError:
            print(f"Eroare: Fișierul {a.intrare} nu există.")
            return
    else:
        # Tratează intrarea ca șir
        intrare = a.intrare if a.intrare is not None else INTRARE_DEMO
        straturi, rezultat = desfă_multistrat(intrare)
        print(f"[Straturi] Decodat prin {straturi} -> Rezultat: {rezultat}")
        rezultat_json = {"strat": straturi, "rezultat": rezultat}
    # Salvăm fișa JSON
    cale_fisa = Path(__file__).resolve().with_name("fisa.json")
    with cale_fisa.open("w", encoding="utf-8") as f:
        json.dump(rezultat_json, f, indent=4, ensure_ascii=False)
    print("Fișa a fost salvată în arsenal/forensics/fisa.json")
if __name__ == "__main__":
    main()
