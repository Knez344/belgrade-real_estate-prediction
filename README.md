# Belgrade Apartment Price Predictor 🏠

A machine learning project that predicts apartment prices in Belgrade, Serbia, based on real listings scraped from [halooglasi.com](https://www.halooglasi.com). Built end-to-end: web scraping → data cleaning → model training → deployed web app.

**Live app:** [belgrade-realestate-prediction.streamlit.app](https://belgrade-realestate-prediction.streamlit.app)

## Overview

Instead of using a pre-packaged dataset, this project collects real, current market data directly from Serbia's largest real estate listing site, then builds a regression model to estimate apartment prices based on size, number of rooms, and municipality (opština).

## Pipeline

1. **Web scraping** (`dan1_test_konekcije.py`, `dan1_izvlacenje_podataka.py`, `dan2_prikupljanje_podataka.py`)
   Collected ~800 apartment listings across 40 pages using `requests` and `BeautifulSoup`, extracting price, size, room count, and location for each listing.

2. **Data cleaning & exploration** (`dan3_ciscenje_podataka.ipynb`)
   - Converted scraped text fields into proper numeric types
   - Handled inconsistent formatting (thousand separators, non-breaking spaces, "5+" room notation)
   - Removed duplicate listings (including near-duplicates with different titles but identical size/price/location)
   - Investigated and validated outliers — several listings priced at €8,000–11,000/m² turned out to be legitimate, from the Belgrade Waterfront/St. Regis development
   - Grouped rare municipalities into an "Other" category
   - Visualized price vs. size relationships, checked feature correlations

3. **Model training**
   - Compared Linear Regression and Random Forest
   - Used one-hot encoding for municipality
   - Applied log-transformation to price to reduce the influence of extreme luxury listings
   - Validated with 5-fold cross-validation for a reliable performance estimate

4. **Deployment**
   - Built an interactive web app with Streamlit
   - Deployed on Streamlit Community Cloud

## Results

| Model | MAE | R² |
|---|---|---|
| Linear Regression | ~€54,000 | 0.88 |
| Random Forest (log price, cross-validated) | ~€55,000 | 0.85 (stable across folds) |

Random Forest with log-transformed price was chosen as the final model for its stability across cross-validation folds, despite a comparable single-split score to Linear Regression.

## Tech stack

- **Scraping:** `requests`, `BeautifulSoup`
- **Data processing:** `pandas`, `numpy`
- **Modeling:** `scikit-learn` (Linear Regression, Random Forest)
- **App:** `Streamlit`
- **Environment:** Jupyter Notebook, PyCharm

## Running locally

```bash
git clone https://github.com/Knez344/belgrade-real_estate-prediction.git
cd belgrade-real_estate-prediction
pip install -r requirements.txt
streamlit run app.py
```

## Notes

This is a learning project built to practice the full data science workflow, from raw data collection to a deployed, usable tool. The model is trained on a limited sample (~750 listings after cleaning) and should be treated as an estimate, not an appraisal.
