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


    return (df,)


@app.cell
def _(df, mo):
    # --- Prepare dropdown options (clean display) ---

    city_options = ["All"] + sorted(df["City"].dropna().astype(str).unique().tolist())

    capacity_options = ["All"] + sorted(df["person_capacity"].dropna().astype(int).unique().tolist())

    superhost_options = ["All", True, False]

    room_type_options = ["All"] + sorted(df["room_type"].dropna().astype(str).unique().tolist())

    days_options = ["All"] + sorted(df["days"].dropna().astype(str).unique().tolist())  # expects: weekdays/weekends

    # --- Price range defaults ---
    price_min = int(df["Price"].min())
    price_slider_max = int(df["Price"].quantile(0.99))

    # --- Widgets ---
    city_select = mo.ui.dropdown(options=city_options, value="All", label="City")
    capacity_select = mo.ui.dropdown(options=capacity_options, value="All", label="Person capacity")
    superhost_select = mo.ui.dropdown(options=superhost_options, value="All", label="Host is superhost")
    room_type_select = mo.ui.dropdown(options=room_type_options, value="All", label="Room type")
    days_select = mo.ui.dropdown(options=days_options, value="All", label="Days")

    price_range = mo.ui.range_slider(
        start=price_min,
        stop=price_slider_max,
        step=10,
        value=(price_min, min(300, price_slider_max)),
        label="Price range (two nights)"
    )

    bins_slider = mo.ui.slider(start=10, stop=100, step=5, value=30, label="Histogram bins")

    mo.vstack(
        [
            mo.md("## Price distribution"),
            mo.md("Use the filters below to explore Airbnb prices."),
            mo.hstack([city_select, capacity_select, superhost_select]),
            mo.hstack([room_type_select, days_select]),
            mo.hstack([price_range, bins_slider]),
        ],
        gap=1
    )

    return (
        bins_slider,
        capacity_select,
        city_select,
        days_select,
        price_range,
        room_type_select,
        superhost_select,
    )


@app.cell
def _(
    bins_slider,
    capacity_select,
    city_select,
    days_select,
    df,
    mo,
    pd,
    plt,
    price_range,
    room_type_select,
    superhost_select,
):
    # --- Apply filters ---
    df_filtered = df.copy()

    if city_select.value != "All":
        df_filtered = df_filtered[df_filtered["City"].astype(str) == str(city_select.value)]

    if capacity_select.value != "All":
        df_filtered = df_filtered[df_filtered["person_capacity"].astype(int) == int(capacity_select.value)]

    if superhost_select.value != "All":
        df_filtered = df_filtered[df_filtered["host_is_superhost"] == bool(superhost_select.value)]

    if room_type_select.value != "All":
        df_filtered = df_filtered[df_filtered["room_type"].astype(str) == str(room_type_select.value)]

    if days_select.value != "All":
        df_filtered = df_filtered[df_filtered["days"].astype(str) == str(days_select.value)]

    # Price range (two nights)
    min_p, max_p = price_range.value
    df_filtered = df_filtered[df_filtered["Price"].between(min_p, max_p)]

    # --- Compute average price (two nights) ---
    avg_price = df_filtered["Price"].mean()

    if pd.isna(avg_price):
        avg_text = mo.md("For this selection the average price for two nights is: **<span style='font-size: 28px;'>—</span>**")
    else:
        avg_text = mo.md(
            "For this selection the average price for two nights is: "
            f"**<span style='font-size: 28px;'>{avg_price:.2f} €</span>**"
        )

    # --- Plot histogram ---
    fig, ax = plt.subplots()
    ax.hist(df_filtered["Price"], bins=int(bins_slider.value))
    ax.set_xlabel("Price (EUR, two nights)")
    ax.set_ylabel("Number of Airbnbs")
    ax.set_title("Price distribution")

    mo.vstack(
        [
            mo.md(f"**Number of listings:** {len(df_filtered)}"),
            mo.md(f"**Price range (two nights):** {min_p} to {max_p}"),
            mo.hstack(
                [
                    fig,
                    mo.vstack(
                        [
                            mo.md("### Average price"),
                            avg_text,
                        ],
                        gap=1
                    ),
                ],
                gap=2
            ),
        ],
        gap=1
    )

    return


@app.cell
def _(
    capacity_select,
    days_select,
    df,
    mo,
    plt,
    room_type_select,
    superhost_select,
):
    # --- Show filters above the boxplot ---
    boxplot_controls = mo.vstack(
        [
            mo.md("## Airbnb Prices by City"),
            mo.md("Filters: Person capacity, Superhost, Room type, Days"),
            mo.hstack([capacity_select, superhost_select, room_type_select, days_select]),
        ],
        gap=1
    )

    # --- Filter for the city boxplot (no city filter, because we compare cities) ---
    df_city = df.copy()

    if capacity_select.value != "All":
        df_city = df_city[df_city["person_capacity"].astype(int) == int(capacity_select.value)]

    if superhost_select.value != "All":
        df_city = df_city[df_city["host_is_superhost"] == bool(superhost_select.value)]

    if room_type_select.value != "All":
        df_city = df_city[df_city["room_type"].astype(str) == str(room_type_select.value)]

    if days_select.value != "All":
        df_city = df_city[df_city["days"].astype(str) == str(days_select.value)]

    cities = sorted(df_city["City"].dropna().astype(str).unique().tolist())

    if len(cities) == 0:
        output_city_plot = mo.md("No data available for this selection.")
    else:
        price_data = [
            df_city[df_city["City"].astype(str) == c]["Price"].dropna().astype(float).values
            for c in cities
        ]
        city_means = [
            df_city[df_city["City"].astype(str) == c]["Price"].mean()
            for c in cities
        ]

        fig_city, ax_city = plt.subplots(figsize=(12, 5))

        bp = ax_city.boxplot(
            price_data,
            tick_labels=cities,
            showfliers=False
        )

        ax_city.set_title("Airbnb Prices by City")
        ax_city.set_ylabel("Price (EUR, two nights)")
        ax_city.tick_params(axis="x", rotation=45)

        # --- Add mean labels next to the median (orange line) ---
        for i, mean_val in enumerate(city_means):
            median_line = bp["medians"][i]
            median_y = float(median_line.get_ydata()[0])

            ax_city.text(
                i + 1.28,
                median_y,
                f"Ø {float(mean_val):.0f}",
                ha="left",
                va="center",
                fontsize=9
            )

        ax_city.set_xlim(0.5, len(cities) + 0.8)

        output_city_plot = fig_city

    # --- Return controls + plot ---
    mo.vstack([boxplot_controls, output_city_plot], gap=1)

    return (df_city,)


@app.cell
def _(df_city, mo):
    # --- Compute cheapest listing per city for the current selection ---
    # Uses df_city (already filtered by capacity/superhost/room_type/days)

    cheapest_per_city = (
        df_city
        .dropna(subset=["City", "Price"])
        .sort_values("Price", ascending=True)
        .groupby("City", as_index=False)
        .first()
    )

    cheapest_city_options = sorted(cheapest_per_city["City"].astype(str).unique().tolist())

    if len(cheapest_city_options) == 0:
        cheapest_city_select = None
        output_cheapest_ui = mo.md("No listings found for this selection.")
    else:
        cheapest_city_select = mo.ui.dropdown(
            options=cheapest_city_options,
            value=cheapest_city_options[0],
            label="Select city (cheapest listing)"
        )
        output_cheapest_ui = mo.vstack(
            [
                mo.md("## Cheapest listing by city"),
                cheapest_city_select,
            ],
            gap=1
        )

    output_cheapest_ui

    return cheapest_city_select, cheapest_per_city


@app.cell
def _(cheapest_city_select, cheapest_per_city, mo):
    # --- Show details for the selected city (reactive) ---

    if cheapest_city_select is None:
        details_out = mo.md("")
    else:
        selected_city = str(cheapest_city_select.value)

        # Safety: if selected city is not present (can happen after filters change)
        available_cities = cheapest_per_city["City"].astype(str).values

        if selected_city not in available_cities:
            details_out = mo.md("No cheapest listing available for the selected city under current filters.")
        else:
            row = cheapest_per_city[cheapest_per_city["City"].astype(str) == selected_city].iloc[0]

            price = float(row["Price"])
            cleanliness = row["cleanliness_rating"]
            satisfaction = row["guest_satisfaction_overall"]

            details_out = mo.md(
                "### Cheapest listing details (based on current filters)\n"
                f"- **City:** {selected_city}\n"
                f"- **Price (two nights):** {price:.2f} €\n"
                f"- **Cleanliness rating:** {cleanliness}\n"
                f"- **Guest satisfaction overall:** {satisfaction}\n"
            )

    # IMPORTANT: return the output
    details_out

    return


if __name__ == "__main__":
    app.run()
