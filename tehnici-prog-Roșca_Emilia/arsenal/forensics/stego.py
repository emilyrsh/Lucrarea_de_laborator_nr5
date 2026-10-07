import sys
from PIL import Image

print("B5:Ascunzi un mesaj prin LSB")
def ascunde_mesajul(cale_sursa: str, cale_iesire: str, mesaj: bytes):
    img = Image.open(cale_sursa).convert("RGB")
    px = list(img.getdata())
    # Adăugăm un octet NULL (b'\x00') la final pentru a cunoaște oprirea la citire
    mesaj = mesaj + b"\x00"
    biti = "".join(f"{byte:08b}" for byte in mesaj)

    if len(biti) > len(px) * 3:
        raise ValueError("mesajul e prea lung pentru aceasta imagine")

    px_noi = []
    bit_idx = 0
    for r, g, b in px:
        canale = [r, g, b]
        for i in range(3):
            if bit_idx < len(biti):
                # Înlocuiește LSB-ul (ultimul bit) cu bitul din mesaj
                canale[i] = (canale[i] & ~1) | int(biti[bit_idx])
                bit_idx += 1
        px_noi.append(tuple(canale))

    img_stego = Image.new(img.mode, img.size)
    img_stego.putdata(px_noi)
    img_stego.save(cale_iesire)
    print(f"Mesaj ascuns cu succes în '{cale_iesire}'")

print("B6: Dezvăluie mesajul ascuns LSB")
def dezvaluie_mesaj_lsb(cale_stego):
    px = list(Image.open(cale_stego).convert("RGB").getdata())

    biti = []
    for (r, g, b) in px:
        biti.append(str(r & 1))
        biti.append(str(g & 1))
        biti.append(str(b & 1))

    # Grupează biții câte 8
    octeti = bytearray()
    for i in range(0, len(biti), 8):
        octet = "".join(biti[i:i+8])
        if len(octet) < 8:
            break
        val = int(octet, 2)
        if val == 0:  # Delimitatorul de final de mesaj
            break
        octeti.append(val)
    return octeti.decode("utf-8", errors="ignore")

if __name__ == "__main__":
    print("B5")
    mesaj_secret = b"FLAG{ascuns_in_pixeli}"
    ascunde_mesajul("probe/foto.jpg", "stego.png", mesaj_secret)

    print("B6")
    mesaj_găsit = dezvaluie_mesaj_lsb("stego.png")
    print(f"Mesaj dezvăluit: {mesaj_găsit}")