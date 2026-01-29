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

    return mo, pd, plt


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

    return


if __name__ == "__main__":
    app.run()
