# Student: <Roșca Emilia> 

BASE_URL = "https://cybercor.org" 

ECHO_URL = "https://httpbin.org" 

TIMEOUT = 10  # secunde 

import csv
import argparse
from datetime import datetime

print("Ex44 și 45")
import webtools
from webtools import get_title, security_headers, DEFAULT_HEADERS, check_paths, site_report

print("Ex48")
parser = argparse.ArgumentParser(description="Instrument de analiză și raportare site-uri web.")
parser.add_argument("url", nargs="?", default="https://cybercor.org", help="URL-ul site-ului țintă")
args = parser.parse_args()
target_url = args.url
print(f"Rulare main.py pentru ținta: {target_url} ---")

# Rularea exercițiilor 44-47
print("User-Agent folosit (DEFAULT_HEADERS):", DEFAULT_HEADERS)
page_res = webtools.fetch(target_url)
print("Titlul paginii prin webtools:", get_title(page_res.text))

print("Ex49")
print("Generare raport CSV")
paths_to_check = ["/", "/robots.txt", "/sitemap.xml", "/admin"]
check_results = check_paths(target_url, paths_to_check)

with open("report.csv", "w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["path", "status", "checked_at"])
    now_iso = datetime.now().isoformat()
    for path, status in check_results.items():
        writer.writerow([path, status, now_iso])
print("Rezultatele verificării căilor au fost salvate în 'report.csv'.")
print("Ex50")
print("Rularea proiectului final:")
site_report(target_url)