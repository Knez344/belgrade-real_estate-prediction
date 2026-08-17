"""
DAN 1 - Test konekcije i prvo istrazivanje HTML-a
====================================================
Cilj danas NIJE da izvucemo sve podatke, nego da:
1. Proverimo da li uopste mozemo da "posetimo" sajt kroz Python
2. Pogledamo kako izgleda HTML koji dobijamo
3. Pocnemo da trazimo gde se u tom HTML-u kriju podaci o stanu

Pre pokretanja, instaliraj biblioteke (u terminalu):
    pip install requests beautifulsoup4
"""

import requests
from bs4 import BeautifulSoup

# Sajtovi ponekad blokiraju zahteve koji "izgledaju" kao da dolaze od robota.
# Zato saljemo header koji kaze "ja sam obican browser" - ovo je standardna praksa.
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# Pocinjemo sa stranicom za prodaju stanova (mozes promeniti grad u URL-u kasnije)
url = "https://www.halooglasi.com/nekretnine/prodaja-stanova/beograd?page=2"

print("Saljem zahtev ka sajtu...")
response = requests.get(url, headers=headers)

# status_code 200 znaci "uspesno", 403 znaci "zabranjeno", 404 "ne postoji" itd.
print(f"Status odgovora: {response.status_code}")

if response.status_code == 200:
    print("Uspesno! Sajt nam je vratio podatke.\n")

    soup = BeautifulSoup(response.text, "html.parser")

    # Ovo je samo da vidimo da li smo stvarno "unutra" - stampa naslov stranice
    print("Naslov stranice:", soup.title.text.strip())

    # Sacuvacemo ceo HTML u fajl da bismo ga mogli pogledati
    # i pronaci gde su tacno podaci o oglasima (cena, kvadratura...)
    with open("stranica.html", "w", encoding="utf-8") as f:
        f.write(soup.prettify())

    print("\nSacuvao sam ceo HTML u fajl 'stranica.html'.")
    print("Otvori taj fajl u browseru ILI u text editoru i")
    print("pokusaj da nadjes deo gde pise cena jednog stana.")
else:
    print("Nesto nije uspelo. Mozda sajt blokira automatske zahteve.")
    print("Javi mi status kod i probacemo drugaciji pristup.")