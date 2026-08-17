"""
STREAMLIT APLIKACIJA - Predvidjanje cena stanova u Beogradu
================================================================
Pokrece se komandom: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import joblib

# --- UCITAVANJE MODELA (samo jednom, na pocetku) ---
model = joblib.load("model_cena_stanova.pkl")
kolone_modela = joblib.load("kolone_modela.pkl")

# --- NASLOV APLIKACIJE ---
st.title("🏠 Predviđanje cena stanova u Beogradu")
st.write("Unesi karakteristike stana i dobij procenu cene na osnovu podataka sa halooglasi.com")

# --- UNOS PODATAKA OD KORISNIKA ---
kvadratura = st.slider("Kvadratura (m²)", min_value=15, max_value=300, value=65)
broj_soba = st.slider("Broj soba", min_value=0.5, max_value=5.0, value=2.5, step=0.5)

# Izvlacimo listu opstina iz kolona modela (ukljucuje i "Ostalo")
opstine = [k.replace("opstina_Opština ", "").replace("opstina_", "") for k in kolone_modela if k.startswith("opstina_")]
opstine.sort()
opstina = st.selectbox("Opština", opstine)

# --- DUGME ZA PREDVIDJANJE ---
if st.button("Izračunaj procenjenu cenu"):
    # Pravimo red podataka u ISTOM formatu kao sto je model treniran
    unos = pd.DataFrame([[0] * len(kolone_modela)], columns=kolone_modela)
    unos["kvadratura"] = kvadratura
    unos["broj_soba"] = broj_soba

    # Pronalazimo tacan naziv kolone za izabranu opstinu (moze biti "Ostalo" ili "Opština X")
    kolona_opstine = None
    for k in kolone_modela:
        if k.startswith("opstina_") and (k == f"opstina_Opština {opstina}" or k == f"opstina_{opstina}"):
            kolona_opstine = k
            break

    if kolona_opstine:
        unos[kolona_opstine] = 1

    # Model predvidja LOG cene - moramo da vratimo u obicne evre pomocu expm1
    predvidjena_cena_log = model.predict(unos)[0]
    predvidjena_cena = np.expm1(predvidjena_cena_log)

    st.success(f"### Procenjena cena: {predvidjena_cena:,.0f} EUR")
    st.caption(f"To je oko {predvidjena_cena / kvadratura:,.0f} EUR po m²")

st.divider()
st.caption("Model treniran na ~750 oglasa prikupljenih sa halooglasi.com. "
           "Ovo je procena zasnovana na istorijskim podacima, ne garancija tacne cene.")
