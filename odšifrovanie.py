# ============================================================
#  STEGANOGRAFIA V PYTHONE  –  pre úplných začiatočníkov
#  Čo robí tento program?
#    → Skryje tajnú správu do obrázka (nikto na prvý pohľad
#      nevidí, že tam niečo je)
#    → Vie správu aj znova vybrať z obrázka
#
#  Ako to funguje?  (metóda LSB – Least Significant Bit)
#    Každý pixel obrázka má farby R, G, B (čísla 0–255).
#    My zmeníme posledný bit každého čísla – ľudské oko
#    tento drobounký rozdiel vôbec nezbadá!
#    Do tých posledných bitov schovávame písmená správy.
# ============================================================

# Najprv musíme nainštalovať knižnicu Pillow:
#   pip install Pillow
# (spusti tento príkaz v termináli, stačí raz)

from PIL import Image   # Pillow – práca s obrázkami


# ──────────────────────────────────────────────
#  POMOCNÉ FUNKCIE  (malé „nástroje" programu)
# ──────────────────────────────────────────────

def text_na_bity(text):
    """
    Prevedie text na reťazec núl a jednotiek (bity).
    Príklad:  'A'  →  '01000001'
    """
    bity = ""
    for pismeno in text:
        # ord() vráti číslo znaku, format(..., '08b') ho prevedie na 8 bitov
        bity += format(ord(pismeno), '08b')
    return bity


def bity_na_text(bity):
    """
    Prevedie reťazec bitov späť na čitateľný text.
    Príklad:  '01000001'  →  'A'
    """
    text = ""
    # Berieme vždy 8 bitov (= 1 znak)
    for i in range(0, len(bity), 8):
        osem_bitov = bity[i:i+8]
        if len(osem_bitov) == 8:                # uistíme sa, že máme kompletný znak
            cislo = int(osem_bitov, 2)          # prevedieme bity na číslo
            text += chr(cislo)                  # číslo na znak
    return text


# ──────────────────────────────────────────────
#  HLAVNÉ FUNKCIE
# ──────────────────────────────────────────────

def skry_spravu(cesta_k_obrazku, tajná_sprava, cesta_vystupu):
    """
    Skryje tajnú správu do obrázka a uloží nový obrázok.

    Parametre:
        cesta_k_obrazku  – kde sa nachádza pôvodný obrázok
        tajná_sprava     – text, ktorý chceme skryť
        cesta_vystupu    – kam uložiť obrázok so skrytou správou
    """

    # 1. Otvoríme obrázok
    obrazok = Image.open(cesta_k_obrazku)
    obrazok = obrazok.convert("RGB")   # zabezpečíme formát R, G, B
    pixely = list(obrazok.getdata())   # načítame všetky pixely do zoznamu

    # 2. Pripravíme správu
    #    Pridáme špeciálnu značku na koniec – podľa nej neskôr poznáme,
    #    kde správa končí. Použijeme znaky, ktoré sa bežne v texte nevyskytujú.
    KONIEC_SPRAVY = "###KONIEC###"
    cela_sprava = tajná_sprava + KONIEC_SPRAVY

    # 3. Prevedieme správu na bity
    bity_spravy = text_na_bity(cela_sprava)
    pocet_bitov = len(bity_spravy)

    # 4. Skontrolujeme, či sa správa do obrázka zmestí
    #    Každý pixel má 3 hodnoty (R, G, B), do každej skryjeme 1 bit
    maximalny_pocet_bitov = len(pixely) * 3
    if pocet_bitov > maximalny_pocet_bitov:
        print("❌ Chyba: Správa je príliš dlhá pre tento obrázok!")
        print(f"   Obrázok pojme max. {maximalny_pocet_bitov // 8} znakov.")
        return

    # 5. Schovávame bity do pixelov
    index_bitu = 0          # sledujeme, ktorý bit práve schováme
    nove_pixely = []        # sem uložíme upravené pixely

    for pixel in pixely:
        r, g, b = pixel     # rozbalíme pixel na tri farby

        # Zmeníme posledný bit farby R
        if index_bitu < pocet_bitov:
            r = (r & 0b11111110) | int(bity_spravy[index_bitu])
            # vysvetlenie:
            #   r & 0b11111110  →  vynuluje posledný bit (napr. 10110111 → 10110110)
            #   | int(bit)      →  nastaví posledný bit na náš bit správy
            index_bitu += 1

        # Zmeníme posledný bit farby G
        if index_bitu < pocet_bitov:
            g = (g & 0b11111110) | int(bity_spravy[index_bitu])
            index_bitu += 1

        # Zmeníme posledný bit farby B
        if index_bitu < pocet_bitov:
            b = (b & 0b11111110) | int(bity_spravy[index_bitu])
            index_bitu += 1

        nove_pixely.append((r, g, b))

    # Pixely, ktoré sme nestihli použiť, pridáme nezmenené
    nove_pixely += pixely[len(nove_pixely):]

    # 6. Uložíme nový obrázok
    novy_obrazok = Image.new("RGB", obrazok.size)
    novy_obrazok.putdata(nove_pixely)
    novy_obrazok.save(cesta_vystupu, "PNG")   # PNG zachová každý pixel presne

    print(f"✅ Hotovo! Správa bola skrytá v obrázku: {cesta_vystupu}")
    print(f"   Skrytých {len(tajná_sprava)} znakov ({pocet_bitov} bitov).")


def citaj_spravu(cesta_k_obrazku):
    """
    Prečíta skrytú správu z obrázka.

    Parametre:
        cesta_k_obrazku – obrázok, z ktorého chceme správu vybrať

    Vráti:
        nájdená tajná správa (text)
    """

    KONIEC_SPRAVY = "###KONIEC###"

    # 1. Otvoríme obrázok a načítame pixely
    obrazok = Image.open(cesta_k_obrazku).convert("RGB")
    pixely = list(obrazok.getdata())

    # 2. Vyberieme posledné bity z každej farby každého pixela
    bity = ""
    for pixel in pixely:
        r, g, b = pixel
        bity += str(r & 1)   # posledný bit červenej
        bity += str(g & 1)   # posledný bit zelenej
        bity += str(b & 1)   # posledný bit modrej

    # 3. Prevedieme bity na text
    cely_text = bity_na_text(bity)

    # 4. Nájdeme značku konca a odrežeme zvyšok
    if KONIEC_SPRAVY in cely_text:
        sprava = cely_text[:cely_text.index(KONIEC_SPRAVY)]
        return sprava
    else:
        return "⚠️ V tomto obrázku nebola nájdená žiadna skrytá správa."


# ──────────────────────────────────────────────
#  HLAVNÝ PROGRAM  –  tu sa všetko spúšťa
# ──────────────────────────────────────────────

if __name__ == "__main__":

    print("=" * 50)
    print("      STEGANOGRAFIA – skrývanie správ")
    print("=" * 50)

    # ── Krok 1: Skryť správu ──
    print("\n📌 SKRÝVANIE SPRÁVY")

    vstupny_obrazok  = "Selsky_les.png"   # ← zmeň na cestu k tvojmu obrázku
    vystupny_obrazok = "tajny.png"      # ← sem sa uloží obrázok so správou
    sprava           = "Rasto dalecky, blabla bla."

    skry_spravu(vstupny_obrazok, sprava, vystupny_obrazok)

    # ── Krok 2: Prečítať správu ──
    print("\n📌 ČÍTANIE SPRÁVY")

    najdena_sprava = citaj_spravu(vystupny_obrazok) #meniť vystupny obrazok/tajny.png
    print(f"🔓 Nájdená správa: {najdena_sprava}")

    print("\n" + "=" * 50)


# ──────────────────────────────────────────────
#  AKO POUŽÍVAŤ TENTO PROGRAM
# ──────────────────────────────────────────────
#
#  1. Nainštaluj Pillow:
#       pip install Pillow
#
#  2. Daj do rovnakého priečinka:
#       - tento súbor (steganografia.py)
#       - nejaký obrázok (napr. original.png)
#
#  3. Zmeň premenné:
#       vstupny_obrazok  = "original.png"    ← tvoj obrázok
#       sprava           = "Tvoja správa"    ← čo chceš skryť
#       vystupny_obrazok = "tajny.png"       ← názov výstupu
#
#  4. Spusti program:
#       python steganografia.py
#
#  ⚠️  Dôležité:
#     • Používaj formát PNG (nie JPG!) – JPG komprimuje obrázok
#       a zničí skryté bity.
#     • Čím väčší obrázok, tým dlhšiu správu môžeš skryť.
#     • 1 megapixel = cca 37 000 znakov kapacity.