from PIL import Image


#binarne čisla na text
def binarnu_na_text(binarny_text):
    sprava = ""
    koniec = "1111111111111110"

    for i in range(0, len(binarny_text), 8):
        osem_bitov = binarny_text[i:i + 8]

        if binarny_text[i:i + 16] == koniec:
            break

        cislo = int(osem_bitov, 2)
        pismeno = chr(cislo)
        sprava += pismeno

    return sprava


#vytiahne spravu z obrázka
def citaj_z_obrazka(cesta_obrazka):
    obrazok = Image.open(cesta_obrazka)
    pixely = list(obrazok.getdata())

    binarny_text = ""

    for pixel in pixely:
        r = pixel[0]
        g = pixel[1]
        b = pixel[2]

        binarny_text += str(r & 1)
        binarny_text += str(g & 1)
        binarny_text += str(b & 1)

    sprava = binarnu_na_text(binarny_text)

    return sprava

najdena_sprava = citaj_z_obrazka("tajny_obrazok.png")
print(f"Nájdená správa: {najdena_sprava}")