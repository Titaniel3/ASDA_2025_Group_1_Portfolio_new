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
            # FISCHBILDER (Online-URLs, funktionieren im WASM-Export)
            # ============================================================
            fish_images = {
                "Bream": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Abramis_brama.jpg/320px-Abramis_brama.jpg",
                "Roach": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Rutilus_rutilus.jpg/320px-Rutilus_rutilus.jpg",
                "Whitefish": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Coregonus_lavaretus.jpg/320px-Coregonus_lavaretus.jpg",
                "Parkki": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/39/Perca_fluviatilis.jpg/320px-Perca_fluviatilis.jpg",
                "Perch": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/39/Perca_fluviatilis.jpg/320px-Perca_fluviatilis.jpg",
                "Pike": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Esox_lucius1.jpg/320px-Esox_lucius1.jpg",
                "Smelt": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Osmerus_eperlanus.jpg/320px-Osmerus_eperlanus.jpg"
            }

            img_url = fish_images.get(prediction, "")

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
                mo.image(img_url) if img_url else mo.md("_Kein Bild verfügbar_")
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


if __name__ == "__main__":
    app.run()
