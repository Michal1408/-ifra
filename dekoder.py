# ============================================================
#  STEGANOGRAFIA – DEKODÉR  (pre úplných začiatočníkov)
#  
#  Čo robí tento program?
#    → Vezme obrázok, v ktorom je skrytá správa
#    → Vytiahne z neho tajný text a vypíše ho
#
#  Funguje len s obrázkami, ktoré boli zakódované pomocou
#  súboru steganografia.py (alebo rovnakej LSB metódy).
# ============================================================

# Potrebuješ nainštalovať Pillow (ak si to ešte nespravil):
#   pip install Pillow

from PIL import Image   # knižnica na prácu s obrázkami


# ──────────────────────────────────────────────
#  POMOCNÉ FUNKCIE
# ──────────────────────────────────────────────

def bity_na_text(bity):
    """
    Prevedie reťazec núl a jednotiek (bity) na čitateľný text.
    Príklad:  '01000001 01000010'  →  'AB'
    """
    text = ""
    # Čítame vždy 8 bitov naraz = 1 znak
    for i in range(0, len(bity), 8):
        osem_bitov = bity[i : i + 8]
        if len(osem_bitov) < 8:
            break                       # neúplný znak = koniec, zastavíme sa
        cislo = int(osem_bitov, 2)      # '01000001' → 65
        text += chr(cislo)              # 65 → 'A'
    return text


def vytahni_bity_z_obrazka(cesta_k_obrazku):
    """
    Otvorí obrázok a vytiahne posledné bity z každej farby každého pixela.
    Práve v týchto bitoch je schovaná správa.
    """
    obrazok = Image.open(cesta_k_obrazku).convert("RGB")
    pixely  = list(obrazok.getdata())

    bity = ""
    for pixel in pixely:
        r, g, b = pixel          # každý pixel = tri čísla (červená, zelená, modrá)
        bity += str(r & 1)       # & 1  →  vyberieme posledný bit červenej
        bity += str(g & 1)       # vyberieme posledný bit zelenej
        bity += str(b & 1)       # vyberieme posledný bit modrej

    return bity


# ──────────────────────────────────────────────
#  HLAVNÁ FUNKCIA DEKODÉRA
# ──────────────────────────────────────────────

def dekoduj_spravu(cesta_k_obrazku):
    """
    Prečíta a vráti tajnú správu skrytú v obrázku.

    Parametre:
        cesta_k_obrazku – cesta k PNG súboru so skrytou správou

    Vráti:
        text tajnej správy, alebo hlásenie ak správa nebola nájdená
    """

    # Toto je špeciálna značka, ktorú enkodér vložil na koniec správy.
    # Podľa nej vieme, kde správa končí.
    KONIEC_SPRAVY = "###KONIEC###"

    print(f"\n🔍 Otváram obrázok: {cesta_k_obrazku}")

    # 1. Vytiahnutie skrytých bitov z obrázka
    bity = vytahni_bity_z_obrazka(cesta_k_obrazku)
    print(f"   Načítaných {len(bity)} bitov z obrázka...")

    # 2. Prevedenie bitov na text
    print("   Prevádzam bity na text...")
    cely_text = bity_na_text(bity)

    # 3. Hľadáme značku konca správy
    if KONIEC_SPRAVY in cely_text:
        # Odrežeme všetko za značkou – to je iba šum (nedôležité dáta)
        sprava = cely_text[: cely_text.index(KONIEC_SPRAVY)]
        return sprava
    else:
        return None   # žiadna správa nebola nájdená


# ──────────────────────────────────────────────
#  HLAVNÝ PROGRAM
# ──────────────────────────────────────────────

if __name__ == "__main__":

    print("=" * 55)
    print("    🔓 STEGANOGRAFIA – DEKODÉR SKRYTÝCH SPRÁV")
    print("=" * 55)

    # ── ZDE NASTAV CESTU K OBRAZKU ──────────────────────────
    obrazok = "tajny.png"   # ← zmeň na cestu k svojmu obrázku
    # ────────────────────────────────────────────────────────

    # Spustíme dekódovanie
    sprava = dekoduj_spravu(obrazok)

    # Vypíšeme výsledok
    print()
    if sprava:
        print("✅ Správa úspešne nájdená!")
        print()
        print("┌─────────────────────────────────────────────┐")
        print("│  TAJNÁ SPRÁVA:                              │")
        print("├─────────────────────────────────────────────┤")
        # Vypíšeme správu, prípadne rozdelenú na riadky po 45 znakov
        for i in range(0, max(1, len(sprava)), 45):
            riadok = sprava[i : i + 45]
            print(f"│  {riadok:<43} │")
        print("└─────────────────────────────────────────────┘")
        print(f"\n   Dĺžka správy: {len(sprava)} znakov")
    else:
        print("⚠️  V tomto obrázku nebola nájdená žiadna skrytá správa.")
        print("   Možné dôvody:")
        print("   • Obrázok nebol zakódovaný týmto programom")
        print("   • Obrázok bol uložený ako JPG (musí byť PNG!)")
        print("   • Obrázok bol upravený alebo stiahnutý zo sociálnych sietí")

    print()
    print("=" * 55)


# ──────────────────────────────────────────────
#  AKO POUŽÍVAŤ TENTO PROGRAM
# ──────────────────────────────────────────────
#
#  1. Uisti sa, že máš nainštalovaný Pillow:
#       pip install Pillow
#
#  2. Zmeň premennú obrazok na cestu k tvojmu obrázku:
#       obrazok = "tajny.png"
#
#  3. Spusti program:
#       python dekoder.py
#
#  ⚠️  Program funguje IBA s PNG obrázkami zakódovanými
#     pomocou LSB steganografie (napr. súborom steganografia.py).
#     JPG obrázky NIE SÚ podporované – komprimácia zničí správu.
