from PIL import Image

# Nacitaj subor
nazov_suboru = "ciernobiely_obrazok_1.txt"

with open(nazov_suboru, "r") as f:
    # Prvý riadok - rozmery obrázka
    prvy_riadok = f.readline().strip()
    sirka, vyska = int(prvy_riadok.split()[0]), int(prvy_riadok.split()[1])

    # Vytvor nový obrázok s bielymi pixelmi
    obrazok = Image.new("RGB", (sirka, vyska), (255, 255, 255))

    # Nacitaj pixely riadok po riadku
    for y in range(vyska):
        riadok = f.readline().strip()
        for x in range(sirka):
            # Kazdy pixel je 2 znaky (hex hodnota)
            hex_hodnota = riadok[x * 2: x * 2 + 2]
            odtien = int(hex_hodnota, 16)  # preved hex na cislo 0-255
            obrazok.putpixel((x, y), (odtien, odtien, odtien))

# Zobraz obrazok
obrazok.show()

# Uloz obrazok
obrazok.save("vystup.png")
print("Hotovo! Obrazok ulozeny ako vystup.png")