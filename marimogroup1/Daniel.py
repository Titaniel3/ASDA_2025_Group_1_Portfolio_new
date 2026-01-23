import marimo

__generated_with = "0.19.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np
    return mo, pd, plt


@app.cell
def _(pd):
    # Read Airbnb dataset using a relative path
    df = pd.read_csv("../datasets/airbnb_cleaned.csv")

    # Show first rows
    df.head()
    return (df,)


@app.cell
def _(df, mo):
    # --- Prepare dropdown options (clean display) ---

    city_options = ["All"] + sorted(df["City"].dropna().astype(str).unique().tolist())

    capacity_options = ["All"] + sorted(df["person_capacity"].dropna().astype(int).unique().tolist())

    superhost_options = ["All", True, False]

    # --- Price range defaults ---
    price_min = int(df["Price"].min())
    price_max = int(df["Price"].max())

    # Use 99th percentile to avoid extreme outliers for the slider max
    price_slider_max = int(df["Price"].quantile(0.99))

    # --- Widgets ---
    city_select = mo.ui.dropdown(
        options=city_options,
        value="All",
        label="City"
    )

    capacity_select = mo.ui.dropdown(
        options=capacity_options,
        value="All",
        label="Person capacity"
    )

    superhost_select = mo.ui.dropdown(
        options=superhost_options,
        value="All",
        label="Host is superhost"
    )

    price_range = mo.ui.range_slider(
        start=price_min,
        stop=price_slider_max,
        step=10,
        value=(price_min, min(300, price_slider_max)),
        label="Price range"
    )

    bins_slider = mo.ui.slider(
        start=10,
        stop=100,
        step=5,
        value=30,
        label="Histogram bins"
    )

    mo.vstack(
        [
            mo.md("## Price distribution"),
            mo.md("Use the filters below to explore Airbnb prices."),
            mo.hstack([city_select, capacity_select, superhost_select]),
            mo.hstack([price_range, bins_slider]),
        ],
        gap=1
    )

    return (
        bins_slider,
        capacity_select,
        city_select,
        price_range,
        superhost_select,
    )


@app.cell
def _(
    bins_slider,
    capacity_select,
    city_select,
    df,
    mo,
    plt,
    price_range,
    superhost_select,
):
    # --- Apply filters ---
    df_filtered = df.copy()

    # City filter
    if city_select.value != "All":
        df_filtered = df_filtered[df_filtered["City"].astype(str) == str(city_select.value)]

    # Person capacity filter
    if capacity_select.value != "All":
        df_filtered = df_filtered[df_filtered["person_capacity"].astype(int) == int(capacity_select.value)]

    # Superhost filter
    if superhost_select.value != "All":
        df_filtered = df_filtered[df_filtered["host_is_superhost"] == bool(superhost_select.value)]

    # Price range filter (min and max)
    min_p, max_p = price_range.value
    df_filtered = df_filtered[df_filtered["Price"].between(min_p, max_p)]

    # --- Plot ---
    fig, ax = plt.subplots()
    ax.hist(df_filtered["Price"], bins=int(bins_slider.value))
    ax.set_xlabel("Price")
    ax.set_ylabel("Number of Airbnbs")
    ax.set_title("Price distribution")

    mo.vstack(
        [
            mo.md(f"**Number of listings:** {len(df_filtered)}"),
            mo.md(f"**Price range:** {min_p} to {max_p}"),
            fig,
        ],
        gap=1
    )

    return


if __name__ == "__main__":
    app.run()
