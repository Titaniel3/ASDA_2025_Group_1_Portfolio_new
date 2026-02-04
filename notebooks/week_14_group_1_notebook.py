import marimo

__generated_with = "0.19.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import marimo as mo
    import scipy.stats as stats
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LogisticRegression
    import plotly.express as px
    from sklearn.metrics import accuracy_score, classification_report
    return (
        LogisticRegression,
        accuracy_score,
        classification_report,
        mo,
        np,
        pd,
        plt,
        px,
        train_test_split,
    )


@app.cell
def _(pd):
    df = pd.read_csv("../datasets/Fish.csv") 
    return (df,)


@app.cell
def _(df):
    df1 = df.drop(["Length1", "Length3"], axis=1)
    return (df1,)


@app.cell
def _(mo):
    mo.md("""
    # 🐟 Fish Species Analysis Dashboard (Group1)
    """)
    return


@app.cell
def _(df_filtered, mo, np):
    # --- KPI tiles (based on df_filtered) ---

    # Compute KPIs
    kpi_total_n = int(len(df_filtered))

    kpi_mean_weight = float(df_filtered["Weight"].mean()) if kpi_total_n > 0 else np.nan
    kpi_mean_length2 = float(df_filtered["Length2"].mean()) if kpi_total_n > 0 else np.nan

    # Species composition (only > 0 automatically, because value_counts only returns present categories)
    kpi_species_counts = (
        df_filtered["Species"]
        .value_counts()
        .sort_values(ascending=False)
    )

    # Build a small markdown "table" for counts
    species_lines = ["**Species composition**"]
    for species_name_kpi, count_kpi in kpi_species_counts.items():
        species_lines.append(f"- {species_name_kpi}: **{int(count_kpi)}**")

    species_breakdown_md = "\n".join(species_lines)

    # Helper: HTML tile (emoji icons are easiest and reliable)
    def _kpi_tile(title, value, icon, subtitle=""):
        # Simple HTML tile; works well in marimo markdown
        return mo.md(
            f"""
    <div style="
      border: 1px solid rgba(0,0,0,0.12);
      border-radius: 14px;
      padding: 14px 16px;
      background: rgba(255,255,255,0.9);
    ">
      <div style="display:flex; align-items:center; justify-content:space-between;">
        <div style="font-size: 14px; opacity: 0.8;">{title}</div>
        <div style="font-size: 20px;">{icon}</div>
      </div>
      <div style="font-size: 30px; font-weight: 700; margin-top: 6px;">{value}</div>
      <div style="font-size: 12px; opacity: 0.75; margin-top: 4px;">{subtitle}</div>
    </div>
    """
        )

    tile_total = _kpi_tile(
        title="Number of fish",
        value=f"{kpi_total_n}",
        icon="🐟",
        subtitle="After applying all meta-filters"
    )

    tile_mean_weight = _kpi_tile(
        title="Average weight",
        value="-" if np.isnan(kpi_mean_weight) else f"{kpi_mean_weight:.1f}",
        icon="⚖️",
        subtitle="Mean of Weight"
    )

    tile_mean_length2 = _kpi_tile(
        title="Average Length2",
        value="-" if np.isnan(kpi_mean_length2) else f"{kpi_mean_length2:.1f}",
        icon="📏",
        subtitle="Mean of Length2"
    )

    # A larger tile for species breakdown (acts like a KPI panel)
    tile_species = mo.md(
        f"""
    <div style="
      border: 1px solid rgba(0,0,0,0.12);
      border-radius: 14px;
      padding: 14px 16px;
      background: rgba(255,255,255,0.9);
    ">
      <div style="display:flex; align-items:center; justify-content:space-between;">
        <div style="font-size: 14px; opacity: 0.8;">Species breakdown</div>
        <div style="font-size: 20px;">🧾</div>
      </div>
      <div style="margin-top: 10px;">
        {species_breakdown_md.replace("\n", "<br>")}
      </div>
    </div>
    """
    )

    # Layout: 3 small tiles on top, then breakdown tile
    mo.vstack(
        [
            mo.md("## KPI Tiles"),
            mo.hstack([tile_total, tile_mean_weight, tile_mean_length2], widths=[1, 1, 1]),
            tile_species,
        ],
        gap=1
    )

    return


@app.cell
def _(df1, mo):
    # --- Helper for slider limits ---

    def _min_max(series):
        # Helper for slider limits
        s = series.dropna()
        return float(s.min()), float(s.max())

    # --- Species widget: multi-select (start with ALL selected) ---

    species_options = sorted(df1["Species"].dropna().unique().tolist())

    species_ms = mo.ui.multiselect(
        options=species_options,
        value=species_options,  # start with all selected
        label="Species"
    )

    # --- Numeric sliders ---

    w_min, w_max = _min_max(df1["Weight"])
    l2_min, l2_max = _min_max(df1["Length2"])
    h_min, h_max = _min_max(df1["Height"])
    wd_min, wd_max = _min_max(df1["Width"])

    weight_slider = mo.ui.range_slider(
        start=w_min,
        stop=w_max,
        value=(w_min, w_max),
        step=max((w_max - w_min) / 200, 1),
        label="Weight (range)"
    )

    length2_slider = mo.ui.range_slider(
        start=l2_min,
        stop=l2_max,
        value=(l2_min, l2_max),
        step=max((l2_max - l2_min) / 200, 0.1),
        label="Length (range)"
    )

    height_slider = mo.ui.range_slider(
        start=h_min,
        stop=h_max,
        value=(h_min, h_max),
        step=max((h_max - h_min) / 200, 0.1),
        label="Height (range)"
    )

    width_slider = mo.ui.range_slider(
        start=wd_min,
        stop=wd_max,
        value=(wd_min, wd_max),
        step=max((wd_max - wd_min) / 200, 0.01),
        label="Width (range)"
    )

    # --- Compact sidebar layout ---

    mo.sidebar(
        mo.vstack(
            [
                mo.md("## Meta-Filter"),
                species_ms,
                weight_slider,
                length2_slider,
                height_slider,
                width_slider,
            ],
            gap=0.25
        )
    )
    return (
        height_slider,
        length2_slider,
        species_ms,
        weight_slider,
        width_slider,
    )


@app.cell
def _(
    df1,
    height_slider,
    length2_slider,
    mo,
    plt,
    species_ms,
    weight_slider,
    width_slider,
):
    # --- Apply meta filters (shared for all plots) ---

    df_filtered = df1.copy()

    # Species filter (multi-select)
    selected_species = species_ms.value

    # If nothing selected: show empty result (prevents confusion)
    if len(selected_species) == 0:
        df_filtered = df_filtered.iloc[0:0]
    else:
        df_filtered = df_filtered[df_filtered["Species"].isin(selected_species)]

    # Numeric range filters
    w_lo, w_hi = weight_slider.value
    l2_lo, l2_hi = length2_slider.value
    h_lo, h_hi = height_slider.value
    wd_lo, wd_hi = width_slider.value

    df_filtered = df_filtered[
        (df_filtered["Weight"] >= w_lo) & (df_filtered["Weight"] <= w_hi) &
        (df_filtered["Length2"] >= l2_lo) & (df_filtered["Length2"] <= l2_hi) &
        (df_filtered["Height"] >= h_lo) & (df_filtered["Height"] <= h_hi) &
        (df_filtered["Width"] >= wd_lo) & (df_filtered["Width"] <= wd_hi)
    ]

    # --- Scatterplot: Length2 vs Weight (colored by Species) ---

    fig, ax = plt.subplots()

    species_in_plot = sorted(df_filtered["Species"].dropna().unique().tolist())

    for sp in species_in_plot:
        sub = df_filtered[df_filtered["Species"] == sp]
        ax.scatter(sub["Length2"], sub["Weight"], label=sp)

    ax.set_xlabel("Length2")
    ax.set_ylabel("Weight")
    ax.set_title("Length vs Weight Scatterplot ")
    ax.grid(True)

    # Legend below the plot
    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, -0.15),
        ncol=3,
        frameon=False
    )

    mo.vstack(
        [
            mo.md(f"### Scatterplot\n**Filtered rows:** {len(df_filtered)}"),
            fig,
        ],
        gap=1
    )
    return (df_filtered,)


@app.cell
def _(df_filtered, mo, plt):
    fig_box_only, ax_box_only = plt.subplots()

    species_in_box_only = sorted(df_filtered["Species"].dropna().unique().tolist())

    box_data_only = []
    box_labels_only = []

    for species_name_only in species_in_box_only:
        weights_values_only = (
            df_filtered.loc[df_filtered["Species"] == species_name_only, "Weight"]
            .dropna()
            .values
        )
        if len(weights_values_only) > 0:
            box_data_only.append(weights_values_only)
            box_labels_only.append(species_name_only)

    if len(box_data_only) == 0:
        out_box_only = mo.md("No data available for the boxplot with the current filters.")
    else:
        ax_box_only.boxplot(box_data_only, tick_labels=box_labels_only)

        ax_box_only.set_title("Weight distribution by Species (filtered)")
        ax_box_only.set_xlabel("Species")
        ax_box_only.set_ylabel("Weight")
        ax_box_only.grid(True, axis="y")

        plt.setp(ax_box_only.get_xticklabels(), rotation=30, ha="right")

        out_box_only = mo.vstack(
            [
                mo.md("### Boxplot: Weight by Species"),
                fig_box_only,
            ],
            gap=1
        )

    out_box_only
    return


@app.cell
def _(df1, train_test_split):
    y = df1["Species"]
    X = df1[["Length2", "Height", "Width","Weight"]]   # example clean feature set

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,      # 20% test data
        random_state=42,    # reproducible
    )

    print("Train rows:", len(X_train))
    print("Test rows:", len(X_test))
    return X_test, X_train, y_test, y_train


@app.cell
def _(
    LogisticRegression,
    X_test,
    X_train,
    accuracy_score,
    classification_report,
    y_test,
    y_train,
):
    from sklearn.preprocessing import StandardScaler
    from sklearn.pipeline import make_pipeline

    model = make_pipeline(
        StandardScaler(),
        LogisticRegression(max_iter=1000)
    )
    model.fit(X_train, y_train)

    pred = model.predict(X_test)

    print("Accuracy:", accuracy_score(y_test, pred))
    print(classification_report(y_test, pred))
    return (model,)


@app.cell
def _(mo):
    # 1. Add a "How-to-use" guide at the top
    instructions = mo.md("""
        ### 📖 How to use:
        1.  Look at the **typical ranges** mentioned in the labels.
        2.  Enter your fish's measurements (Weight, Length, etc.).
        3.  Click **Predict Species** to see the result and confidence score.
    """).callout(kind="info")

    # 2. Use labels to show "Example" or "Typical" values
    # This acts as a placeholder that never disappears
    weight_in = mo.ui.number(label="Weight in grams (e.g., 300)", start=0, stop=1800, value=0)
    len2_in = mo.ui.number(label="Length in cm (e.g., 25.4)", start=0, stop=70, value=0)
    height_in = mo.ui.number(label="Height in cm (e.g., 11.5)", start=0, stop=20, value=0)
    width_in = mo.ui.number(label="Width in cm (e.g., 4.0)", start=0, stop=15, value=0)

    predict_btn = mo.ui.run_button(label="🔮 Predict Species")

    # 3. Organize the UI with clear spacing
    form = mo.vstack([
        mo.md("# 🐟 Fish Species Predictor"),
        instructions,
        mo.md("---"),
        mo.hstack([weight_in, len2_in], justify="start"),
        mo.hstack([height_in, width_in], justify="start"),
        mo.md(" "), # Spacer
        mo.hstack([predict_btn], justify="start")
    ])

    form
    return height_in, len2_in, predict_btn, weight_in, width_in


@app.cell
def _(height_in, len2_in, mo, model, np, pd, predict_btn, weight_in, width_in):

    # Stop execution until the button is clicked
    mo.stop(not predict_btn.value, mo.md("### Standing by... \n Fill the form and click **Predict**."))

    # 1. Define "Reasonable" limits based on your training data
    limits = {
        "Weight": 1800,
        "Height": 20,
        "Width": 15,
        "Length2": 70
    }

    # 2. Validation Check
    too_large = [k for k, v in {
        "Weight": weight_in.value, 
        "Height": height_in.value, 
        "Width": width_in.value, 
        "Length2": len2_in.value
    }.items() if v > limits.get(k, 100)]

    if too_large:
        result_display = mo.md(f"🛑 **Unreasonable Value!** The input for **{', '.join(too_large)}** is much larger than any fish in our records.")
    elif any(v <= 0 for v in [weight_in.value, height_in.value, width_in.value, len2_in.value]):
        result_display = mo.md("⚠️ **Missing Data:** Please ensure all measurements are greater than 0.")
    else:
        # 3. Data is valid -> Proceed to Prediction
        try:
            # Create the data row
            input_data = pd.DataFrame([{
                "Length2": len2_in.value,
                "Height": height_in.value,
                "Width": width_in.value,
                "Weight": weight_in.value
            }])

            # Predict Species
            prediction = model.predict(input_data)[0]

            # --- NEW: CALCULATE CONFIDENCE SCORE ---
            # predict_proba returns a list of probabilities (e.g., [0.1, 0.8, 0.1])
            probs = model.predict_proba(input_data)[0]
            confidence = np.max(probs) * 100
            # ---------------------------------------

            # 4. Setup images
            fish_images = {
                "Bream": "images/Bream.jpg", "Roach": "images/roach.jpg",
                "Whitefish": "images/Lake_whitefish.jpg", "Parkki": "images/parrki.jpg",
                "Perch": "images/perch-fish.jpg", "Pike": "images/pike-fish-species.jpg", 
                "Smelt": "images/smelt.jpg"
            }

            img_path = fish_images.get(prediction, "")

            # 5. Build the Result Display
            # We use a color-coded span for the confidence score
            conf_color = "green" if confidence > 85 else "orange" if confidence > 50 else "red"

            result_display = mo.vstack([
                mo.md(f"## 🎉 Result: This is a **{prediction}**!"),
                mo.md(f"**Confidence Score:** <span style='color: {conf_color}; font-size: 1.2em;'>{confidence:.1f}%</span>"),
                mo.image(img_path) if img_path else mo.md("_Image not available_")
            ])

        except Exception as e:
            # Note: If this fails, make sure your model supports predict_proba (like RandomForest or LogisticRegression)
            result_display = mo.md(f"⚠️ **Error during prediction:** {e}")

    result_display
    return


@app.cell
def _(df, mo, px):
    counts = df['Species'].value_counts().reset_index()
    counts.columns = ['Species', 'Count']

    fig1 = px.bar(
        counts, 
        x='Species', 
        y='Count', 
        color='Species',
        title="<b>Total Samples per Species</b>",
        text_auto=True,
        template="plotly_white"
    )

    mo.md(f"### 📊 Dataset Balance\n{mo.as_html(fig1)}")
    return


@app.cell
def _(df, mo, px):
    fig2 = px.scatter(
        df, 
        x="Length2", 
        y="Weight", 
        color="Species",
        symbol="Species",
        title="<b>Weight vs. Length Growth Curve</b>",
        labels={"Length2": "Length (cm)", "Weight": "Weight (g)"}, 
        template="plotly_white"
    )

    mo.md(f"### 📈 Growth Trends\n{mo.as_html(fig2)}")
    return


@app.cell
def _(df, mo, px):
    fig3 = px.box(
        df, 
        x="Species", 
        y="Height", 
        color="Species",
        title="<b>Height Variation by Species</b>", # Shows confidence interval around the median
        template="plotly_white"
    )

    mo.md(f"### 📏 Height Analysis\n{mo.as_html(fig3)}")
    return


@app.cell
def _(df1, mo, px):


    # Calculate correlation matrix for numeric columns
    corr = df1.select_dtypes(include=['number']).corr()

    fig4 = px.imshow(
        corr, 
        text_auto=True, 
        aspect="auto",
        color_continuous_scale='RdBu_r',
        title="<b>Feature Correlation Heatmap</b>"
    )

    mo.md(f"### 🔗 Measurement Relationships\n{mo.as_html(fig4)}")
    return


if __name__ == "__main__":
    app.run()
