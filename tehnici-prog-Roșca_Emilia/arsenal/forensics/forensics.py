import re
import zipfile
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

print("B1: Magic bytes - tipul real, nu extensia")
def tip_real(cale):
    with open(cale, "rb") as f:
        cap = f.read(8)
    if cap.startswith(b"%PDF"):
        return "pdf"
    elif cap.startswith(b"\x89PNG"):
        return "png"
    elif cap.startswith(b"\xff\xd8"):
        return "jpeg"
    elif cap.startswith(b"PK\x03\x04"):
        return "zip/docx"
    return cap.hex()

print("B2: Strings.Textul citibil dintr-un binar")
def extrage_strings(cale, lungime_minimă=4):
    date = open(cale, "rb").read()
    rezultate = []
    for m in re.findall(rb"[ -~]{%d,}" % lungime_minimă, date):
        rezultate.append(m.decode())
    return rezultate

print("B3: Metadate EXIF și GPS din poză")
def dms_in_grade_zecimale(dms, ref):
# Se convertesc coordonatele GPS (grade, minute, secunde) în grade zecimale
    grade, minute, secunde = (float(x) for x in dms)
    val = grade + minute / 60 + secunde / 3600
    if ref in ("S", "W"):
     val = -val
    return val
def citește_exif_gps(cale):
    try:
        img = Image.open(cale)
        exif = img._getexif() or {}
    except Exception as e:
        print(f"Eroare la citirea EXIF: {e}")
        return

    print("Metadate EXIF")
    gps_data = {}
    for tag_id, val in exif.items():
        tag_nume = TAGS.get(tag_id, tag_id)
        if tag_nume == "GPSInfo":
            for gps_tag_id in val:
                sub_tag = GPSTAGS.get(gps_tag_id, gps_tag_id)
                gps_data[sub_tag] = val[gps_tag_id]
        else:
            print(f"{tag_nume} = {val}")

    if gps_data:
        print("\n--- Date GPS ---")
        lat = dms_in_grade_zecimale(gps_data['GPSLatitude'], gps_data['GPSLatitudeRef'])
        lon = dms_in_grade_zecimale(gps_data['GPSLongitude'], gps_data['GPSLongitudeRef'])
        print(f"Latitudine:  {lat:.6f}")
        print(f"Longitudine: {lon:.6f}")
        print(f"Google Maps Link: https://maps.google.com/?q={lat},{lon}")


print("B4: File carving - scoți fișierul ascuns")
def extrage_ascuns(cale, semnătură=b"PK\x03\x04", ieșire="gasit.zip"):
    date = open(cale, "rb").read()
    i = date.find(semnătură)
    if i != -1:
        open(ieșire, "wb").write(date[i:])
        print("Arhiva extrasă de la octetul", i)
        return ieșire
    print("Nu s-a găsit nicio arhivă ascunsă")
    return None

if __name__ == "__main__":

    
    print("B1")
    print("probe/foto.jpg:", tip_real("probe/foto.jpg"))
    print("probe/ascuns.png:", tip_real("probe/ascuns.png"))

    print("B2")
    strings_gasiți = extrage_strings("probe/ascuns.png")
    for s in strings_gasiți[:10]: # afișează primele 10
        print(" >", s)

    print("B3")
    citește_exif_gps("probe/foto.jpg")

    print("B4")
    extrage_ascuns("probe/ascuns.png")