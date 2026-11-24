import os, hashlib, argparse

# A1. Tipul dupa magic bytes
MAGIC = {b"\x89PNG": "PNG", b"%PDF": "PDF", b"PK\x03\x04": "ZIP"}

def tip(head):
    for semnatura, nume in MAGIC.items():
        if head.startswith(semnatura):
            return nume
    return "necunoscut"   # După buclă (aliniem return cu for, nu cu if)

# A2. Amprenta unui fisier, citit cu with
def amprenta_fisier(cale):
    with open(cale, "rb") as f:      # "rb" = binar; with = inchide singur
        date = f.read()
    return {"nume": os.path.basename(cale),
            "tip": tip(date[:8]),
            "sha256": hashlib.sha256(date).hexdigest()[:16]}

# A3. Scanăm tot folderul
def scaneaza(folder):
    rez = []
    for nume in sorted(os.listdir(folder)):
        cale = os.path.join(folder, nume)
        if os.path.isfile(cale):
            rez.append(amprenta_fisier(cale))
    return rez


def main():
    parser = argparse.ArgumentParser(description="Amprente de fisiere")
    parser.add_argument("folder", help="folderul cu probe")
    args = parser.parse_args()
    for fisa in scaneaza(args.folder):
        print(f"{fisa['nume']:14} {fisa['tip']:11} {fisa['sha256']}")

if __name__ == "__main__":
    main()