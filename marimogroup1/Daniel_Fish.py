import marimo

__generated_with = "0.19.4"
app = marimo.App(width="medium")


@app.cell
def _():
    # --- Core / app ---
    import marimo as mo  # Interactive notebook/dashboard framework

    # --- Data handling ---
    import pandas as pd  # DataFrames
    import numpy as np   # Numeric utilities

    # --- Plotting (simple + beginner-friendly) ---
    import matplotlib.pyplot as plt  # Plots with matplotlib

    # --- Optional: ML / evaluation (handy for dashboards with simple models) ---
    from sklearn.model_selection import train_test_split  # Train/test split
    from sklearn.preprocessing import StandardScaler      # Feature scaling
    from sklearn.pipeline import Pipeline                 # Combine steps
    from sklearn.metrics import r2_score, mean_absolute_error, accuracy_score  # Metrics

    from sklearn.linear_model import LinearRegression, LogisticRegression  # Baseline models
    from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier  # Stronger models

    return (
        LogisticRegression,
        Pipeline,
        StandardScaler,
        accuracy_score,
        mo,
        np,
        pd,
        plt,
        train_test_split,
    )


@app.cell
def _(pd):
    # --- Load dataset ---
    data_path = "../datasets/Fish_final.xlsx"  # Path relative to marimogroup1
    df = pd.read_excel(data_path)

    # Quick check
    df.head()

    return (df,)


@app.cell
def _(df, mo):
    # --- Prepare a clean base dataframe for the dashboard ---

    species_cols = [c for c in df.columns if c.startswith("Species_")]

    df_base = df.copy()
    df_base["Species"] = (
        df_base[species_cols]
        .idxmax(axis=1)
        .str.replace("Species_", "", regex=False)
    )

    # --- Helper for slider limits ---

    def _min_max(series):
        # Helper for slider limits
        s = series.dropna()
        return float(s.min()), float(s.max())

    # --- Species widget: multi-select (start with ALL selected) ---

    species_options = sorted(df_base["Species"].dropna().unique().tolist())

    species_ms = mo.ui.multiselect(
        options=species_options,
        value=species_options,  # start with all selected
        label="Species"
    )

    # --- Numeric sliders ---

    w_min, w_max = _min_max(df_base["Weight"])
    l2_min, l2_max = _min_max(df_base["Length2"])
    h_min, h_max = _min_max(df_base["Height"])
    wd_min, wd_max = _min_max(df_base["Width"])

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
        label="Length2 (range)"
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
        df_base,
        height_slider,
        length2_slider,
        species_ms,
        weight_slider,
        width_slider,
    )


@app.cell
def _(
    df_base,
    height_slider,
    length2_slider,
    mo,
    plt,
    species_ms,
    weight_slider,
    width_slider,
):
    # --- Apply meta filters (shared for all plots) ---

    df_filtered = df_base.copy()

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
    ax.set_title("Length2 vs Weight (filtered)")
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
    # --- Visualization 2: Boxplot Weight by Species (filtered) ---

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
def _(
    LogisticRegression,
    Pipeline,
    StandardScaler,
    accuracy_score,
    df_base,
    mo,
    train_test_split,
):
    # --- Model: Predict Species from fish measurements ---

    # Features and target
    feature_cols_cls = ["Weight", "Length2", "Height", "Width"]

    # Remove rows with missing values in features/target
    train_df_cls = df_base.dropna(subset=feature_cols_cls + ["Species"]).copy()

    X_cls = train_df_cls[feature_cols_cls]
    y_cls = train_df_cls["Species"]

    # Split
    X_train_cls, X_test_cls, y_train_cls, y_test_cls = train_test_split(
        X_cls, y_cls, test_size=0.2, random_state=42, stratify=y_cls
    )

    # Pipeline: scaling + classifier
    species_model = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("clf", LogisticRegression(max_iter=2000))
        ]
    )

    # Train
    species_model.fit(X_train_cls, y_train_cls)

    # Quick evaluation
    y_pred_cls = species_model.predict(X_test_cls)
    acc_cls = accuracy_score(y_test_cls, y_pred_cls)

    mo.md(f"### Model trained ✅\nAccuracy on test set: **{acc_cls:.3f}**")

    return (species_model,)


@app.cell
def _(df_base, mo):
    # --- Angler Tool: create UI elements (NO .value access here) ---

    angler_get_state, angler_set_state = mo.state(None)

    angler_weight_inp = mo.ui.number(label="Weight", value=float(df_base["Weight"].median()))
    angler_length2_inp = mo.ui.number(label="Length2", value=float(df_base["Length2"].median()))
    angler_height_inp = mo.ui.number(label="Height", value=float(df_base["Height"].median()))
    angler_width_inp = mo.ui.number(label="Width", value=float(df_base["Width"].median()))

    angler_submit_btn = mo.ui.button(label="🎣 Predict species")

    mo.vstack(
        [
            mo.md("## 🎣 Angler Tool"),
            mo.md("Enter the measurements and click **Predict species**."),
            angler_weight_inp,
            angler_length2_inp,
            angler_height_inp,
            angler_width_inp,
            angler_submit_btn,
        ],
        gap=0.5
    )

    return (
        angler_get_state,
        angler_height_inp,
        angler_length2_inp,
        angler_set_state,
        angler_submit_btn,
        angler_weight_inp,
        angler_width_inp,
    )


@app.cell
def _(
    angler_height_inp,
    angler_length2_inp,
    angler_set_state,
    angler_submit_btn,
    angler_weight_inp,
    angler_width_inp,
    mo,
):
    # --- Angler Tool: submit handler (reads .value in a separate cell) ---

    if angler_submit_btn.value:
        angler_set_state(
            {
                "Weight": float(angler_weight_inp.value),
                "Length2": float(angler_length2_inp.value),
                "Height": float(angler_height_inp.value),
                "Width": float(angler_width_inp.value),
            }
        )

    mo.md("✅ Ready to predict. Click the button above.")

    return


@app.cell
def _(angler_get_state, mo, pd, species_model):
    # --- Angler Tool: prediction output (from state) ---

    submitted_vals_tool = angler_get_state()

    if submitted_vals_tool is None:
        out_pred_tool = mo.md("Click **Predict species** to see the result.")
    else:
        user_df_tool = pd.DataFrame([submitted_vals_tool])

        pred_species_tool = species_model.predict(user_df_tool)[0]

        if hasattr(species_model, "predict_proba"):
            proba_vals_tool = species_model.predict_proba(user_df_tool)[0]
            class_names_tool = species_model.named_steps["clf"].classes_

            top_df_tool = (
                pd.DataFrame({"Species": class_names_tool, "Probability": proba_vals_tool})
                .sort_values("Probability", ascending=False)
                .head(3)
            )

            lines_tool = [f"## ✅ Prediction: **{pred_species_tool}**", "", "**Top 3 probabilities:**"]
            for _, row_tool in top_df_tool.iterrows():
                lines_tool.append(f"- {row_tool['Species']}: **{row_tool['Probability']:.1%}**")

            out_pred_tool = mo.md("\n".join(lines_tool))
        else:
            out_pred_tool = mo.md(f"## ✅ Prediction: **{pred_species_tool}**")

    out_pred_tool

    return


if __name__ == "__main__":
    app.run()
