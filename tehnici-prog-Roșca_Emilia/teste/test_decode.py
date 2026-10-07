import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from arsenal.forensics.decode import desfacem, ghicim_stratul, citibil, sparge_xor

def test_base64():
    strat, b = desfacem("U2FsdXQ=")
    assert strat == "base64"
    assert b == b"Salut"

def test_hex():
    strat, b = desfacem("48656c6c6f")
    assert strat == "hex"
    assert b == b"Hello"

def test_url():
    strat, b = desfacem("%2Fetc%2Fpasswd")
    assert strat == "url"
    assert b == b"/etc/passwd"

def test_ghici_necunoscut():
    assert ghicim_stratul("$$$ nu e nimic $$$") == "necunoscut"

def test_citibil():
    assert citibil(b"text normal") is True
    assert citibil(bytes([0, 1, 2, 255])) is False

def test_sparge_xor():
    cheie_reala = 0x2A
    clar = b"salut lume"
    criptat = bytes(c ^ cheie_reala for c in clar)
    candidati = sparge_xor(criptat)
    chei_gasite = [k for k, _ in candidati]
    assert cheie_reala in chei_gasite
