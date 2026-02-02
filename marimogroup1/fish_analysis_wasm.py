import marimo

__generated_with = "0.19.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    import numpy as np
    import marimo as mo
    import requests
    from io import BytesIO
    from PIL import Image
    import plotly.express as px
    import plotly.io as pio
    import plotly.graph_objects as go
    return BytesIO, Image, go, mo, np, pd, pio, px, requests


@app.cell
def _():
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
def _(BytesIO, pd):
    from urllib.request import urlopen

    # Lade Fisch-Daten von GitHub Pages (WASM-kompatibel)
    url = "https://github.com/Titaniel3/ASDA_2025_Group_1_Portfolio_new/raw/refs/heads/main/datasets/Fish.csv"
    with urlopen(url) as response:
        csv_data = BytesIO(response.read())
    df = pd.read_csv(csv_data)

    df_clean = df.drop(["Length1", "Length3"], axis=1)
    return (df,)


@app.cell
def _(np):
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
    ### 📖 Instructions:
    1. Look at the typical **value ranges** shown in the input fields
    2. Enter the fish measurements (length, height, width, weight)
    3. Click **Make prediction** to determine the species

    """).callout(kind="info")

    # Input-Felder mit Beispielwerten und sinnvollen Grenzen
    weight_in = mo.ui.number(
        label="Weight in Gramm (z.B. 300)",
        start=0,
        stop=1800,
        value=300,
        step=10
    )
    len2_in = mo.ui.number(
        label="Length in cm (z.B. 28.4)",
        start=0,
        stop=70,
        value=28.4,
        step=1
    )
    height_in = mo.ui.number(
        label="Height in cm (z.B. 9.0)",
        start=0,
        stop=20,
        value=9.0,
        step=0.5
    )
    width_in = mo.ui.number(
        label="Width in cm (z.B. 4.4)",
        start=0,
        stop=15,
        value=4.4,
        step=0.5
    )

    predict_btn = mo.ui.run_button(label="🔮 Make Prediction")

    # Layout
    form = mo.vstack([
        mo.md("# 🐟 Fish Classifier"),
        instructions,
        mo.md("---"),
        mo.md("### Input Fish Measurments:"),
        mo.hstack([weight_in, len2_in], justify="start"),
        mo.hstack([height_in, width_in], justify="start"),
        mo.md(" "),
        mo.hstack([predict_btn], justify="start")
    ])

    form
    return height_in, len2_in, predict_btn, weight_in, width_in


@app.cell
def _(
    BytesIO,
    Image,
    height_in,
    len2_in,
    mo,
    model_weights,
    predict_btn,
    predict_fish_species,
    requests,
    weight_in,
    width_in,
):

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
            # FISCHBILDER (Von GitHub Raw geladen)
            # ============================================================
            fish_image_urls = {
                "Bream": "https://raw.githubusercontent.com/Titaniel3/ASDA_2025_Group_1_Portfolio_new/refs/heads/main/additional_material/Images_Fish/bream.png",
                "Roach": "https://raw.githubusercontent.com/Titaniel3/ASDA_2025_Group_1_Portfolio_new/refs/heads/main/additional_material/Images_Fish/Roach.png",
                "Whitefish": "https://raw.githubusercontent.com/Titaniel3/ASDA_2025_Group_1_Portfolio_new/refs/heads/main/additional_material/Images_Fish/Whitefish.png",
                "Parkki": "https://raw.githubusercontent.com/Titaniel3/ASDA_2025_Group_1_Portfolio_new/refs/heads/main/additional_material/Images_Fish/Parrki.png",
                "Perch": "https://raw.githubusercontent.com/Titaniel3/ASDA_2025_Group_1_Portfolio_new/refs/heads/main/additional_material/Images_Fish/Perch.png",
                "Pike": "https://raw.githubusercontent.com/Titaniel3/ASDA_2025_Group_1_Portfolio_new/refs/heads/main/additional_material/Images_Fish/Pike.png",
                "Smelt": "https://raw.githubusercontent.com/Titaniel3/ASDA_2025_Group_1_Portfolio_new/refs/heads/main/additional_material/Images_Fish/Smelt.png"
            }

            # Lade Bild von GitHub
            img_url = fish_image_urls.get(prediction, "")
            if img_url:
                try:
                    response_image = requests.get(img_url)
                    img = Image.open(BytesIO(response_image.content))
                    img_display = mo.image(img)
                except Exception as e:
                    img_display = mo.md(f"⚠️ Bild konnte nicht geladen werden")
            else:
                img_display = mo.md("_Kein Bild verfügbar_")

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
                img_display
            ])

        except Exception as e:
            result_display = mo.md(f"⚠️ **Fehler:** {str(e)}").callout(kind="danger")

    result_display
    return


@app.cell
def _(go, mo, pio):
    # Inject plotly.js ONCE (offline / GitHub Pages safe)
    _bootstrap = go.Figure()
    mo.Html(
        pio.to_html(
            _bootstrap,
            include_plotlyjs="inline",
            full_html=False,
        )
    )

    def plot(fig):
        """Render a plotly figure without re-embedding plotly.js."""
        return mo.Html(
            pio.to_html(
                fig,
                include_plotlyjs=False,
                full_html=False,
                config={
                    "responsive": True,
                    "displayModeBar": True,
                    "scrollZoom": True,
                },
            )
        )
    return (plot,)


@app.cell
def _(df, mo, plot, px):
    counts = df["Species"].value_counts().reset_index()
    counts.columns = ["Species", "Count"]

    fig1 = px.bar(
        counts,
        x="Species",
        y="Count",
        color="Species",
        title="Total Samples per Species",
        text_auto=True,
        template="plotly_white",
    )

    mo.md("### 📊 Dataset Balance")
    plot(fig1)
    return (fig1,)


@app.cell
def _(fig1):
    fig1
    return


@app.cell
def _(df, mo, plot, px):
    fig2 = px.scatter(
        df,
        x="Length2",
        y="Weight",
        color="Species",
        symbol="Species",
        title="Weight vs. Length Growth Curve",
        labels={"Length2": "Length (cm)", "Weight": "Weight (g)"},
        template="plotly_white",
    )

    mo.md("### 📈 Growth Trends")
    plot(fig2)
    return (fig2,)


@app.cell
def _(fig2):
    fig2
    return


@app.cell
def _(df, mo, plot, px):
    fig3 = px.box(
        df,
        x="Species",
        y="Height",
        color="Species",
        title="Height Variation by Species",
        template="plotly_white",
    )

    mo.md("### 📏 Height Analysis")
    plot(fig3)
    return (fig3,)


@app.cell
def _(fig3):
    fig3
    return


@app.cell
def _(df, mo, plot, px):
    corr = df.select_dtypes(include=["number"]).corr()

    fig4 = px.imshow(
        corr,
        text_auto=True,
        aspect="auto",
        color_continuous_scale='RdBu_r',
        title="Feature Correlation Heatmap",
    )

    mo.md("### 🔗 Measurement Relationships")
    plot(fig4)
    return (fig4,)


@app.cell
def _(fig4):
    fig4
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## But how much is the fish? We couldn't find out.
    """)
    return


@app.cell
def _(mo):
    mo.Html(
        """
        <div style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;">
          <iframe
            src="https://www.youtube.com/embed/cbB3iGRHtqA?start=118"
            title="YouTube video player"
            frameborder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
            allowfullscreen
            style="position:absolute;top:0;left:0;width:100%;height:100%;">
          </iframe>
        </div>
        """
    )
    return


if __name__ == "__main__":
    app.run()
