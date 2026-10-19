from httptools import PATHS, report
def main():
    # 1. Apelăm report pentru fiecare adresă și adăugăm adresa în dicționar
    rezultate = []
    for path in PATHS:
        rezultat = report(path)
        rezultat["path"] = path
        rezultate.append(rezultat)

    # 2. Păstrăm doar paginile cu status 200, cea mai lentă prima
    reusite = [r for r in rezultate if r.get("status") == 200]
    reusite.sort(key=lambda r: r["seconds"], reverse=True)

    for r in reusite:
        print(f"{r['path']} -> {r['status']}, {r['seconds']} secunde")

    # 3. Totalurile: tot ce nu e 200 (inclusiv 404 și timeout) e eșec
    esuate = len(rezultate) - len(reusite)
    print(f"Reușite: {len(reusite)} | Eșuate: {esuate}")


if __name__ == "__main__":
    main()
