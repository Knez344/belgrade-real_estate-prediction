"""
DAN 2 - Prikupljanje sa vise stranica + cuvanje u CSV
=========================================================
Sada prolazimo kroz vise stranica pretrage (ne samo jednu) i
sve prikupljene podatke cuvamo trajno u CSV fajl (tabela, kao Excel).

Nova biblioteka: pandas - standardni alat za rad sa tabelarnim
podacima u Python-u. Koristicemo je i kasnije za analizu i model.

Instaliraj je isto kao requests/beautifulsoup4 (Alt+Enter na "pandas"
kad ti PyCharm podvuce crveno, ili preko Settings).
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# Koliko stranica zelimo da prikupimo. Pocni sa malim brojem (npr. 5)
# da testiras da sve radi, pa kasnije povecaj na 30-50 kad si siguran/na.
BROJ_STRANICA = 40

svi_podaci = []  # ovde ce se skupljati podaci sa SVIH stranica

for broj_stranice in range(1, BROJ_STRANICA + 1):
    url = f"https://www.halooglasi.com/nekretnine/prodaja-stanova/beograd?page={broj_stranice}"

    print(f"Prikupljam stranicu {broj_stranice}/{BROJ_STRANICA}...")
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"  Preskacem stranicu {broj_stranice} - status {response.status_code}")
        continue

    soup = BeautifulSoup(response.text, "html.parser")
    oglasi = soup.find_all("div", class_="product-item")

    for oglas in oglasi:
        cena_tag = oglas.select_one(".central-feature span")
        cena = cena_tag["data-value"] if cena_tag else None

        naslov_tag = oglas.select_one("h3.product-title a")
        naslov = naslov_tag.text.strip() if naslov_tag else None

        lokacija_lista = oglas.select("ul.subtitle-places li")
        lokacija = ", ".join(li.text.strip() for li in lokacija_lista)

        kvadratura = None
        broj_soba = None
        features = oglas.select("ul.product-features li .value-wrapper")
        for f in features:
            legend = f.select_one(".legend")
            if legend:
                tip = legend.text.strip()
                vrednost = f.get_text(strip=True).replace(legend.text.strip(), "")
                if "Kvadratura" in tip:
                    kvadratura = vrednost
                elif "soba" in tip:
                    broj_soba = vrednost

        if naslov is None or cena is None or kvadratura is None:
            continue

        svi_podaci.append({
            "naslov": naslov,
            "cena_eur": cena,
            "lokacija": lokacija,
            "kvadratura": kvadratura,
            "broj_soba": broj_soba,
        })

    # Pauza od 2 sekunde pre sledece stranice - "pristojnost" prema sajtu
    # i smanjuje sansu da nas privremeno blokiraju zbog previse brzih zahteva
    time.sleep(2)

print(f"\nUkupno prikupljeno: {len(svi_podaci)} oglasa sa {BROJ_STRANICA} stranica.\n")

# Pretvaramo listu u pandas tabelu (DataFrame) i cuvamo kao CSV
df = pd.DataFrame(svi_podaci)
df.to_csv("stanovi_beograd.csv", index=False, encoding="utf-8-sig")

print("Sacuvano u fajl 'stanovi_beograd.csv'")
print("\nPrvih 5 redova:")
print(df.head())