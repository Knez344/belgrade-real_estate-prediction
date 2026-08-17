"""
DAN 1 (zavrsetak) - Izvlacenje podataka iz jedne stranice
============================================================
Sad kad znamo tacnu strukturu HTML-a (zahvaljujuci Inspect Element-u),
mozemo da napisemo kod koji AUTOMATSKI prolazi kroz SVE oglase
na stranici i izvlaci: cenu, naslov, lokaciju, kvadraturu, broj soba.
"""

import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

url = "https://www.halooglasi.com/nekretnine/prodaja-stanova/beograd?page=2"

print("Saljem zahtev ka sajtu...")
response = requests.get(url, headers=headers)
print(f"Status odgovora: {response.status_code}\n")

soup = BeautifulSoup(response.text, "html.parser")

# Svaki oglas je jedan <div class="product-item ...">
# Trazimo SVE takve div-ove na stranici
oglasi = soup.find_all("div", class_="product-item")
print(f"Pronasao sam {len(oglasi)} oglasa na ovoj stranici.\n")

# Ovde cemo skupljati sve podatke - lista recnika (dictionary)
podaci = []

for oglas in oglasi:
    # --- CENA ---
    # Trazimo span sa klasom "central-feature" pa unutra span sa data-value
    cena_tag = oglas.select_one(".central-feature span")
    cena = cena_tag["data-value"] if cena_tag else None

    # --- NASLOV ---
    naslov_tag = oglas.select_one("h3.product-title a")
    naslov = naslov_tag.text.strip() if naslov_tag else None

    # --- LOKACIJA (spajamo sve delove: grad, opstina, naselje) ---
    lokacija_lista = oglas.select("ul.subtitle-places li")
    lokacija = ", ".join(li.text.strip() for li in lokacija_lista)

    # --- KVADRATURA i BROJ SOBA ---
    # Ova dva se nalaze u ul.product-features, ali moramo da prepoznamo
    # KOJI je koji po tekstu u <span class="legend">
    kvadratura = None
    broj_soba = None

    features = oglas.select("ul.product-features li .value-wrapper")
    for f in features:
        legend = f.select_one(".legend")
        if legend:
            tip = legend.text.strip()
            # Uzimamo sav tekst OSIM legende (to je sama vrednost, npr. "78 m2")
            vrednost = f.get_text(strip=True).replace(legend.text.strip(), "")

            if "Kvadratura" in tip:
                kvadratura = vrednost
            elif "soba" in tip:
                broj_soba = vrednost

        # Preskacemo oglase kod kojih fale kljucni podaci (nije prava kartica stana)
    if naslov is None or cena is None or kvadratura is None:
        continue

        # Dodajemo sve u nasu listu kao jedan "red" podataka
    podaci.append({
        "naslov": naslov,
        "cena_eur": cena,
        "lokacija": lokacija,
        "kvadratura": kvadratura,
        "broj_soba": broj_soba,
    })

# Ispisujemo prvih 5 da proverimo da li sve ima smisla
print("Prvih 5 oglasa:\n")
for i, p in enumerate(podaci[:5], start=1):
    print(f"{i}. {p['naslov']}")
    print(f"   Cena: {p['cena_eur']} EUR")
    print(f"   Lokacija: {p['lokacija']}")
    print(f"   Kvadratura: {p['kvadratura']}, Broj soba: {p['broj_soba']}")
    print()