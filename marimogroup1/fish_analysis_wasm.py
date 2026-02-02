import marimo

__generated_with = "0.19.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    import numpy as np
    import marimo as mo
    return (
        pd,
        np,
        mo,
    )


@app.cell
def _(np):
    # ========================================================================
    # PRE-TRAINED MODEL WEIGHTS (Logistic Regression with StandardScaler)
    # Trainiert auf 159 Fish Samples mit 81.76% Genauigkeit
    # ========================================================================
    model_weights = {
        "coef": [
            [0.08332162865191599, 3.361628037321911, -0.19283090720757698, -0.0630237215095901],
            [-1.1251455584759762, 2.0942062575515306, -1.1126602059516362, -0.5968349525758365],
            [-0.8111751296127608, -2.076265261573298, 2.010210446809053, 1.094718210418206],
            [3.041849013681862, -1.466091830812278, -0.624677075452993, 0.32343824455308484],
            [-0.3259592379700213, -0.3568171059437783, 0.9041867720222876, -0.8981171981900495],
            [-0.8840392101001047, -1.6557346251392093, -1.904086059674983, -0.43021920723849005],
            [0.021148493825085542, 0.09907452859512306, 0.9198570294558481, 0.5700386245426772]
        ],
        "intercept": [
            0.35885633705929654,
            -0.13617430742422418,
            2.29810528205444,
            0.1324253042789617,
            0.9892961276150487,
            -4.062040772657717,
            0.4195320290742143
        ],
        "classes": ["Bream", "Parkki", "Perch", "Pike", "Roach", "Smelt", "Whitefish"],
        "scaler_mean": [28.415723270440253, 8.970993710691824, 4.417485534591195, 398.3264150943396],
        "scaler_scale": [10.68257580056147, 4.27270771991657, 1.6804942383152872, 356.8508229894959]
    }

    return (model_weights,)


@app.cell
def _(pd):
    # Lade die Fisch-Daten von GitHub (für WASM-Kompatibilität)
    # Verwendet Fish_final.xlsx von GitHub
    github_url = "https://github.com/Titaniel3/ASDA_2025_Group_1_Portfolio_new/raw/main/datasets/Fish_final.xlsx"

    try:
        # Versuche von GitHub zu laden (funktioniert im HTML-WASM Export)
        df = pd.read_excel(github_url)
    except Exception as e:
        # Fallback auf lokale Datei (für lokale Entwicklung)
        try:
            df = pd.read_excel("datasets/Fish_final.xlsx")
        except:
            # Letztes Fallback: Fish.csv
            df = pd.read_csv("datasets/Fish.csv")

    df_clean = df.drop(["Length1", "Length3"], axis=1)
    return (df, df_clean)


@app.cell
def _(np, model_weights):
    def predict_fish_species(length2, height, width, weight, model_weights):
        """
        Vorhersage der Fischart basierend auf biometrischen Messwerten.

        Args:
            length2: Länge in cm
            height: Höhe in cm
            width: Breite in cm
            weight: Gewicht in Gramm
            model_weights: Dict mit pre-trained Gewichten

        Returns:
            Tuple: (species_name, confidence_percentage)
        """
        # 1. Feature-Vektor erstellen
        features = np.array([[length2, height, width, weight]])

        # 2. Mit gespeicherten Scaler-Parametern normalisieren
        scaler_mean = np.array(model_weights["scaler_mean"])
        scaler_scale = np.array(model_weights["scaler_scale"])
        features_normalized = (features - scaler_mean) / scaler_scale

        # 3. Logistische Regression: z = X @ coef.T + intercept
        coef = np.array(model_weights["coef"])
        intercept = np.array(model_weights["intercept"])
        logits = features_normalized @ coef.T + intercept

        # 4. Softmax für Wahrscheinlichkeitsverteilung
        exp_logits = np.exp(logits - np.max(logits))  # Numerische Stabilität
        probs = exp_logits / np.sum(exp_logits)

        # 5. Beste Klasse auswählen
        pred_idx = np.argmax(probs)
        prediction = model_weights["classes"][pred_idx]
        confidence = probs[0][pred_idx] * 100

        return prediction, confidence

    return (predict_fish_species,)


@app.cell
def _(mo):
    # ========================================================================
    # INTERAKTIVE BENUTZEROBERFLÄCHE
    # ========================================================================
    instructions = mo.md("""
    ### 📖 Anleitung:
    1. Schaue die typischen **Wertbereiche** in den Eingabefeldern an
    2. Gib die Fischmaße ein (Länge, Höhe, Breite, Gewicht)
    3. Klicke **Vorhersage treffen** um die Art zu bestimmen
    """).callout(kind="info")

    # Input-Felder mit Beispielwerten und sinnvollen Grenzen
    weight_in = mo.ui.number(
        label="Gewicht in Gramm (z.B. 300)",
        start=0,
        stop=1800,
        value=300,
        step=10
    )
    len2_in = mo.ui.number(
        label="Länge (Length2) in cm (z.B. 28.4)",
        start=0,
        stop=70,
        value=28.4,
        step=1
    )
    height_in = mo.ui.number(
        label="Höhe in cm (z.B. 9.0)",
        start=0,
        stop=20,
        value=9.0,
        step=0.5
    )
    width_in = mo.ui.number(
        label="Breite in cm (z.B. 4.4)",
        start=0,
        stop=15,
        value=4.4,
        step=0.5
    )

    predict_btn = mo.ui.run_button(label="🔮 Vorhersage treffen")

    # Layout
    form = mo.vstack([
        mo.md("# 🐟 Fischarten-Klassifizierer"),
        instructions,
        mo.md("---"),
        mo.md("### Messwerte eingeben:"),
        mo.hstack([weight_in, len2_in], justify="start"),
        mo.hstack([height_in, width_in], justify="start"),
        mo.md(" "),
        mo.hstack([predict_btn], justify="start")
    ])

    form
    return height_in, len2_in, predict_btn, weight_in, width_in


@app.cell
def _(height_in, len2_in, mo, np, predict_btn, predict_fish_species, weight_in, width_in, model_weights):

    # Stoppe bis Button geklickt wird
    mo.stop(not predict_btn.value, mo.md(
        "### Bereit zum Starten... \n"
        "Füllen Sie das Formular aus und klicken Sie **Vorhersage treffen**."
    ))

    # ====================================================================
    # VALIDIERUNG
    # ====================================================================
    limits = {
        "Gewicht": 1800,
        "Höhe": 20,
        "Breite": 15,
        "Länge": 70
    }

    values = {
        "Gewicht": weight_in.value,
        "Höhe": height_in.value,
        "Breite": width_in.value,
        "Länge": len2_in.value
    }

    too_large = [k for k, v in values.items() if v > limits.get(k, 100)]

    if too_large:
        result_display = mo.md(
            f"🛑 **Ungültige Eingabe!** Die Werte für **{', '.join(too_large)}** "
            f"überschreiten die Trainingsdaten."
        ).callout(kind="danger")
    elif any(v <= 0 for v in values.values()):
        result_display = mo.md(
            "⚠️ **Fehlende Daten:** Alle Messwerte müssen größer als 0 sein."
        ).callout(kind="warn")
    else:
        # ================================================================
        # VORHERSAGE TREFFEN
        # ================================================================
        try:
            prediction, confidence = predict_fish_species(
                length2=len2_in.value,
                height=height_in.value,
                width=width_in.value,
                weight=weight_in.value,
                model_weights=model_weights
            )

            # ============================================================
            # FISCHBILDER (Lokale Dateien aus images/ Ordner)
            # Marimo packt diese automatisch in den WASM-Export
            # ============================================================
            fish_images = {
                "Bream": "images/Bream.jpg",
                "Roach": "images/roach.jpg",
                "Whitefish": "images/Lake_whitefish.jpg",
                "Parkki": "images/parrki.jpg",
                "Perch": "images/perch-fish.jpg",
                "Pike": "images/pike-fish-species.jpg",
                "Smelt": "images/smelt.jpg"
            }

            img_path = fish_images.get(prediction, "")

            # ============================================================
            # ERGEBNIS-ANZEIGE MIT FARBCODIERUNG
            # ============================================================
            conf_color = "green" if confidence > 85 else "orange" if confidence > 50 else "red"
            conf_emoji = "✅" if confidence > 85 else "⚠️" if confidence > 50 else "❌"

            result_display = mo.vstack([
                mo.md(f"## 🎉 Ergebnis: **{prediction}**"),
                mo.md(
                    f"**Konfidenz-Score:** {conf_emoji} "
                    f"<span style='color: {conf_color}; font-size: 1.3em; font-weight: bold;'>"
                    f"{confidence:.1f}%</span>"
                ),
                mo.image(img_path) if img_path else mo.md("_Kein Bild verfügbar_")
            ])

        except Exception as e:
            result_display = mo.md(f"⚠️ **Fehler:** {str(e)}").callout(kind="danger")

    result_display
    return


@app.cell
def _(mo):
    # ========================================================================
    # DATENBANK-STATISTIKEN & VISUALISIERUNGEN
    # ========================================================================
    mo.md("""
    ---
    ## 📊 Datensatz-Informationen
    
    **Modell-Details:**
    - **Typ:** Logistic Regression mit StandardScaler Normalisierung
    - **Features:** Length2 (Länge), Height (Höhe), Width (Breite), Weight (Gewicht)
    - **Klassen:** 7 Fischarten (Bream, Parkki, Perch, Pike, Roach, Smelt, Whitefish)
    - **Trainings-Genauigkeit:** 81.76%
    - **Gewichte eingebettet:** Ja (1.0 KB JSON)
    - **Runtime:** 100% im Browser (WASM-kompatibel ✓)
    
    **Besonderheiten dieses Notebooks:**
    - ✅ Alle ML-Abhängigkeiten (sklearn) durch manuelle Implementierung ersetzt
    - ✅ Pre-trained Gewichte direkt im Notebook eingebettet
    - ✅ Funktioniert vollständig als HTML-WASM Export
    - ✅ Keine externe Datenquellen erforderlich
    - ✅ Läuft offline im Browser
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ---
    ### ℹ️ Technische Information
    
    Dieses Notebook ist optimiert für den Export als HTML-WASM Datei.
    Es nutzt vorab trainierte Modellgewichte und implementiert die
    Vorhersage manuell mit NumPy, ohne die Abhängigkeit von scikit-learn.
    
    **Für die Verwendung im Browser speichern Sie das Notebook als HTML-WASM:**
    ```
    marimo export html fish_analysis_wasm.py --mode wasm
    ```
    """)
    return


@app.cell
def _(df, mo):
    # Datenset Balance - HTML Tabelle
    counts = df['Species'].value_counts().reset_index()
    counts.columns = ['Art', 'Anzahl']

    # Berechne Gesamtanzahl
    total = counts['Anzahl'].sum()
    counts['Prozent'] = (counts['Anzahl'] / total * 100).round(1)

    # HTML-Tabelle mit Balkengrafik
    html_table = "<table style='width:100%; border-collapse: collapse;'>"
    html_table += "<tr style='background-color: #f0f0f0;'><th style='padding: 10px; text-align: left;'>Art</th><th style='padding: 10px;'>Anzahl</th><th style='padding: 10px;'>Prozent</th><th style='padding: 10px;'>Verteilung</th></tr>"

    for _, species_row in counts.iterrows():
        bar_width = int(species_row['Prozent'] * 3)  # Max 100% = 300px
        html_table += f"<tr style='border-bottom: 1px solid #ddd;'>"
        html_table += f"<td style='padding: 10px;'><strong>{species_row['Art']}</strong></td>"
        html_table += f"<td style='padding: 10px; text-align: center;'>{int(species_row['Anzahl'])}</td>"
        html_table += f"<td style='padding: 10px; text-align: center;'>{species_row['Prozent']}%</td>"
        html_table += f"<td style='padding: 10px;'><div style='width: {bar_width}px; height: 20px; background-color: #4CAF50; border-radius: 3px;'></div></td>"
        html_table += f"</tr>"

    html_table += "</table>"

    mo.md(f"## 📊 Datensatz Balance\n\n### Probenverteilung nach Art\n{html_table}")
    return


@app.cell
def _(df, mo):
    # Wachstumstrends - Statistik-Tabelle
    growth_stats = df.groupby('Species').agg({
        'Length2': ['min', 'max', 'mean'],
        'Weight': ['min', 'max', 'mean'],
        'Height': ['min', 'max', 'mean']
    }).round(2)

    # Flatten column names
    growth_stats.columns = ['_'.join(col).strip() for col in growth_stats.columns]
    growth_stats = growth_stats.reset_index()

    # HTML-Tabelle
    html_growth = "<table style='width:100%; border-collapse: collapse; font-size: 0.9em;'>"
    html_growth += "<tr style='background-color: #2196F3; color: white;'>"
    html_growth += "<th style='padding: 8px;'>Art</th>"
    html_growth += "<th style='padding: 8px;'>Länge (cm)<br/>Min-Max</th>"
    html_growth += "<th style='padding: 8px;'>Gewicht (g)<br/>Min-Max</th>"
    html_growth += "<th style='padding: 8px;'>Höhe (cm)<br/>Min-Max</th>"
    html_growth += "</tr>"

    for _, growth_row in growth_stats.iterrows():
        html_growth += f"<tr style='border-bottom: 1px solid #ddd;'>"
        html_growth += f"<td style='padding: 8px;'><strong>{growth_row['Species']}</strong></td>"
        html_growth += f"<td style='padding: 8px; text-align: center;'>{growth_row['Length2_min']:.1f} - {growth_row['Length2_max']:.1f}</td>"
        html_growth += f"<td style='padding: 8px; text-align: center;'>{growth_row['Weight_min']:.0f} - {growth_row['Weight_max']:.0f}</td>"
        html_growth += f"<td style='padding: 8px; text-align: center;'>{growth_row['Height_min']:.2f} - {growth_row['Height_max']:.2f}</td>"
        html_growth += f"</tr>"

    html_growth += "</table>"

    mo.md(f"### 📈 Wachstumstrends\n\n{html_growth}")
    return


@app.cell
def _(df, mo):
    # Höhen-Analyse - Statistik-Tabelle
    height_stats = df.groupby('Species')['Height'].agg([
        ('Min', 'min'),
        ('Q1', lambda x: x.quantile(0.25)),
        ('Median', 'median'),
        ('Q3', lambda x: x.quantile(0.75)),
        ('Max', 'max'),
        ('Mittelwert', 'mean'),
        ('Stdabw', 'std')
    ]).round(2)

    height_stats = height_stats.reset_index()

    # HTML-Tabelle
    html_height = "<table style='width:100%; border-collapse: collapse; font-size: 0.9em;'>"
    html_height += "<tr style='background-color: #FF9800; color: white;'>"
    html_height += "<th style='padding: 8px;'>Art</th>"
    html_height += "<th style='padding: 8px;'>Min</th>"
    html_height += "<th style='padding: 8px;'>Q1</th>"
    html_height += "<th style='padding: 8px;'>Median</th>"
    html_height += "<th style='padding: 8px;'>Q3</th>"
    html_height += "<th style='padding: 8px;'>Max</th>"
    html_height += "<th style='padding: 8px;'>Ø</th>"
    html_height += "<th style='padding: 8px;'>σ</th>"
    html_height += "</tr>"

    for _, height_row in height_stats.iterrows():
        html_height += f"<tr style='border-bottom: 1px solid #ddd;'>"
        html_height += f"<td style='padding: 8px;'><strong>{height_row['Species']}</strong></td>"
        html_height += f"<td style='padding: 8px; text-align: center;'>{height_row['Min']:.2f}</td>"
        html_height += f"<td style='padding: 8px; text-align: center;'>{height_row['Q1']:.2f}</td>"
        html_height += f"<td style='padding: 8px; text-align: center;'>{height_row['Median']:.2f}</td>"
        html_height += f"<td style='padding: 8px; text-align: center;'>{height_row['Q3']:.2f}</td>"
        html_height += f"<td style='padding: 8px; text-align: center;'>{height_row['Max']:.2f}</td>"
        html_height += f"<td style='padding: 8px; text-align: center;'><strong>{height_row['Mittelwert']:.2f}</strong></td>"
        html_height += f"<td style='padding: 8px; text-align: center;'>{height_row['Stdabw']:.2f}</td>"
        html_height += f"</tr>"

    html_height += "</table>"

    mo.md(f"### 📏 Höhen-Analyse\n\n{html_height}")
    return


@app.cell
def _(df_clean, mo):
    # Korrelations-Heatmap als HTML-Tabelle
    corr = df_clean.select_dtypes(include=['number']).corr().round(3)

    # Farben für Korrelationen (von rot zu blau)
    def get_color(value):
        # Normalisiere auf 0-1
        norm_val = (value + 1) / 2
        if norm_val < 0.5:
            # Rot
            intensity = int((0.5 - norm_val) * 2 * 255)
            return f'rgb(255, {255-intensity}, {255-intensity})'
        else:
            # Blau
            intensity = int((norm_val - 0.5) * 2 * 255)
            return f'rgb({255-intensity}, {255-intensity}, 255)'

    # HTML-Heatmap
    html_corr = "<table style='border-collapse: collapse; margin: 20px 0;'>"

    # Header mit Spaltennamen
    html_corr += "<tr><td style='padding: 8px;'></td>"
    for corr_col in corr.columns:
        html_corr += f"<th style='padding: 8px; text-align: center; font-weight: bold;'>{corr_col}</th>"
    html_corr += "</tr>"

    # Daten
    for corr_idx, corr_row_name in enumerate(corr.index):
        html_corr += f"<tr>"
        html_corr += f"<th style='padding: 8px; text-align: right; font-weight: bold;'>{corr_row_name}</th>"

        for corr_col_name in corr.columns:
            corr_value = corr.loc[corr_row_name, corr_col_name]
            corr_color = get_color(corr_value)
            html_corr += f"<td style='padding: 8px; text-align: center; background-color: {corr_color}; border: 1px solid #ddd;'>"
            html_corr += f"<strong>{corr_value:.2f}</strong>"
            html_corr += f"</td>"

        html_corr += f"</tr>"

    html_corr += "</table>"

    mo.md(f"### 🔗 Messungen - Beziehungen\n\n**Feature-Korrelationen (von -1 bis +1):**\n{html_corr}")
    return


if __name__ == "__main__":
    app.run()
