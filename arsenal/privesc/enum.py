import argparse,  json, os

def citeste_linii(cale):
    with open(cale, encoding="utf-8") as f:
        # TODO: intoarce lista liniilor .strip(), fara cele goale si fara cele cu #
        linii_utile = []
        for linie_bruta in f:
            linie = linie_bruta.strip()
            if linie == "" or linie.startswith("#"):
                continue
            linii_utile.append(linie)
        return linii_utile

def nume(cale):
    # TODO: intoarce ce e dupa ultimul "/" (vezi rsplit)
    bucati = cale.rsplit("/", 1)
    return bucati[-1]

GTFO = {"find", "vim.basic", "vim", "nmap", "cp", "bash",
        "less", "awk", "python3", "perl"}

def suid_constatari(cale):
    cai = citeste_linii(cale)
    # TODO: pentru fiecare cale UNICA, in ordine sortata, un dict:
    # {"cale": c, "nume": nume(c),
    #  "risc": "mare" daca nume(c) in GTFO, altfel "normal"}
    rezultat = []
    for c in sorted(set(cai)):
        n = nume(c)
        nivel_risc = "mare" if n in GTFO else "normal"
        rezultat.append({"cale": c, "nume": n, "risc": nivel_risc})
    return rezultat

def sudo_constatari(cale):
    out = []
    for ln in citeste_linii(cale):
        user, drept = ln.split(" : ", 1)  # despachetare in tuplu
        # TODO: adauga {"user": user.strip(), "drept": drept.strip(),
        #  "risc": "mare" daca "NOPASSWD" in drept, altfel "normal"}
        user = user.strip()
        drept = drept.strip()
        nivel_risc = "mare" if "NOPASSWD" in drept else "normal"
        out.append({"user": user, "drept": drept, "risc": nivel_risc})
    return out

def cron_constatari(cale):
    out = []
    for ln in citeste_linii(cale):
        # TODO: campuri = ln.split(); user = campuri[5];
        # comanda = " ".join(campuri[6:]); dict cu user si comanda
        campuri = ln.split()
        user = campuri[5]
        comanda = " ".join(campuri[6:])
        out.append({"user": user, "comanda": comanda})
    return out

def enumereaza(d):
    return {
        "suid": suid_constatari(os.path.join(d, "suid.txt")),
        "sudo": sudo_constatari(os.path.join(d, "sudo.txt")),
        "cron": cron_constatari(os.path.join(d, "crontab.txt")),
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("capturi")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()

    raport = enumereaza(a.capturi)

    if a.json:
        print(json.dumps(raport, indent=2, ensure_ascii=False))
        return

    for categorie, lista in raport.items():
        mari = [c for c in lista if c.get("risc") == "mare"]
        print(f"{categorie}: {len(lista)} gasite, {len(mari)} cu risc mare")

    # TODO: utilizatorii implicati = multimea userilor din sudo REUNITA cu cei din cron
    din_sudo = {c["user"] for c in raport["sudo"]}
    din_cron = {c["user"] for c in raport["cron"]}
    utilizatori = din_sudo | din_cron
    print("utilizatori implicati:", ", ".join(sorted(utilizatori)))

    with open("enum.json", "w", encoding="utf-8") as f:
        json.dump(raport, f, indent=2, ensure_ascii=False)
    print("Raport salvat in enum.json")

if __name__ == "__main__":
    main()
