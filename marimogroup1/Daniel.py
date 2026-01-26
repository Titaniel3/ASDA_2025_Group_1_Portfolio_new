import marimo

__generated_with = "0.19.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np
    #import plotly.express as px
    return mo, pd, plt


@app.cell
def _(pd):
    # Load dataset (works locally and on GitHub Pages / WASM)

    try:
        # Local: read from filesystem
        df = pd.read_csv("../datasets/airbnb_cleaned.csv")
    except FileNotFoundError:
        # WASM/GitHub Pages: fetch from the deployed URL
        from urllib.request import urlopen  # standard library
        from io import StringIO  # standard library

        BASE_URL = "https://titaniel3.github.io/ASDA_2025_Group_1_Portfolio_new/"
        CSV_URL = BASE_URL + "datasets/airbnb_cleaned.csv"

        with urlopen(CSV_URL) as f:
            csv_text = f.read().decode("utf-8")

        df = pd.read_csv(StringIO(csv_text))

    # df is loaded

    return (df,)


@app.cell
def _(mo):
    mo.md(r"""
    ## Daniel Part
    """)
    return


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
        price_min,
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
    return (fig,)


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
    return cities, df_city


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


@app.cell
def _(mo):
    mo.md(r"""
    ## Ranjits Part
    """)
    return


@app.cell
def _(df):
    cities_ranjit = sorted(df["City"].unique())
    room_types = sorted(df["room_type"].unique())
    host_portfolio = sorted(df["host_portfolio"].unique())
    return cities_ranjit, host_portfolio, room_types


@app.cell
def _(cities_ranjit, mo):
    selected_cities = mo.ui.multiselect(
        options=cities_ranjit,
        value=cities_ranjit,
        label="Select Cities"
    )
    return (selected_cities,)


@app.cell
def _(mo, room_types):
    selected_room_type = mo.ui.dropdown(
        options=room_types,
        value=room_types[0],
        label="Select Room Type"
    )
    return (selected_room_type,)


@app.cell
def _(host_portfolio, mo):
    selected_host_portfolio = mo.ui.dropdown(
        options= host_portfolio,
        value=host_portfolio[0],
        label="Select host Type"
    )
    return (selected_host_portfolio,)


@app.cell
def _(df, selected_cities, selected_room_type):
    filtered_df = df[df["City"].isin(selected_cities.value)]

    counts = (
        filtered_df
        .groupby(["City", "room_type"])
        .size()
        .unstack(fill_value=0)
    )

    shares = counts.div(counts.sum(axis=1), axis=0)

    # Select only one room type
    room_share = shares[selected_room_type.value]
    return (room_share,)


@app.cell
def _(plt, room_share, selected_room_type):
    fig_ranjit, ax_ranjit = plt.subplots(figsize=(10, 5))

    ax_ranjit.bar(
        room_share.index,
        room_share.values
    )

    ax_ranjit.set_title(f"Share of {selected_room_type.value} by City")
    ax_ranjit.set_ylabel("Share")
    ax_ranjit.set_ylim(0, 1)
    ax_ranjit.tick_params(axis="x", rotation=45)
    return


@app.cell
def _(fig, mo, selected_cities, selected_room_type):
    mo.vstack([
        mo.md("## Room Type Share by City"),
        mo.hstack([selected_cities, selected_room_type]),
        fig
    ])
    return


@app.cell
def _(df, selected_cities, selected_host_portfolio):
    filtered_df1 = df[df["City"].isin(selected_cities.value)]

    counts1 = (
        filtered_df1
        .groupby(["City", "host_portfolio"])
        .size()
        .unstack(fill_value=0)
    )

    shares1 = counts1.div(counts1.sum(axis=1), axis=0)

    # Select only one room type
    host = shares1[selected_host_portfolio.value]
    return (host,)


@app.cell
def _(host, plt, selected_host_portfolio):
    figure, ax1 = plt.subplots(figsize=(10, 5))

    ax1.bar(
        host.index,
        host.to_numpy()
    )

    ax1.set_title(f"Share of {selected_host_portfolio.value} by City")
    ax1.set_ylabel("Share")
    ax1.set_ylim(0, 1)
    ax1.tick_params(axis="x", rotation=45)
    return (figure,)


@app.cell
def _(figure, mo, selected_cities, selected_host_portfolio):
    mo.vstack([
        mo.md("## Share of host portfolio by City"),
        mo.hstack([selected_cities, selected_host_portfolio]),
        figure
    ])
    return


@app.cell
def _(df):
    listing_by_day = df.groupby(['City', 'days']).size().reset_index(name='count')
    return (listing_by_day,)


@app.cell
def _(cities, listing_by_day, mo):
    cities2 = sorted(listing_by_day["City"].unique())
    day_types = sorted(listing_by_day["days"].unique())

    selected_cities2 = mo.ui.multiselect(
        options=cities,
        value=cities,
        label="Select Cities"
    )

    selected_days = mo.ui.multiselect(
        options=day_types,
        value=day_types,
        label="Select Day Type"
    )
    return (selected_days,)


@app.cell
def _(listing_by_day, selected_cities, selected_days):
    filtered_data = listing_by_day[
        (listing_by_day["City"].isin(selected_cities.value)) &
        (listing_by_day["days"].isin(selected_days.value))
    ]

    pivot_data = filtered_data.pivot(
        index="City",
        columns="days",
        values="count"
    )
    return (pivot_data,)


@app.cell
def _(pivot_data, plt):
    figure2, ax2 = plt.subplots(figsize=(10, 5))

    pivot_data.plot(
        kind="bar",
        ax=ax2
    )

    ax2.set_title("Number of Listings per City by Day Type")
    ax2.set_ylabel("Number of Listings")
    ax2.set_xlabel("City")
    ax2.tick_params(axis="x", rotation=45)
    ax2.legend(title="Day Type")
    plt.close(figure2)

    # nothing returned → nothing displayed
    return (figure2,)


@app.cell
def _(figure2, mo, selected_cities, selected_days):

    mo.vstack([
        mo.md("## Number of Listings per City by Day Type"),
        mo.hstack([selected_cities, selected_days]),
        figure2
    ])
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Tobis Part
    """)
    return


@app.cell
def _(cities, df, price_min):
    COL = {
        "city": "City",
        "lat": "lat",
        "lon": "lng",
        "bedrooms": "bedrooms",
        "host_portfolio": "host_portfolio",
        "capacity": "person_capacity",
        "room_type": "room_type",
        "price": "Price",
        "guest_satisfaction": "guest_satisfaction_overall",
        "superhost": "host_is_superhost",
        "cleanliness": "cleanliness_rating",
    }

    cities_t = sorted(df[COL["city"]].dropna().unique().tolist())
    room_types_t = sorted(df[COL["room_type"]].dropna().unique().tolist())
    bedrooms_vals = sorted(df[COL["bedrooms"]].dropna().unique().tolist())
    capacity_vals = sorted(df[COL["capacity"]].dropna().unique().tolist())
    host_portfolios = sorted(df[COL["host_portfolio"]].dropna().unique().tolist())

    price_min_t = float(df[COL["price"]].min())
    price_max = 1000
    # float(df[COL["price"]].max())

    sat_min = float(df[COL["guest_satisfaction"]].min())
    sat_max = float(df[COL["guest_satisfaction"]].max())

    clean_min = int(df[COL["cleanliness"]].min())
    clean_max = int(df[COL["cleanliness"]].max())

    (cities[:5], host_portfolios, (price_min, price_max), (sat_min, sat_max), (clean_min, clean_max))
    return (
        COL,
        bedrooms_vals,
        capacity_vals,
        cities_t,
        clean_max,
        clean_min,
        host_portfolios,
        price_max,
        price_min_t,
        room_types_t,
        sat_max,
        sat_min,
    )


@app.cell
def _(
    bedrooms_vals,
    capacity_vals,
    cities_t,
    clean_max,
    clean_min,
    host_portfolios,
    mo,
    price_max,
    price_min_t,
    room_types_t,
    sat_max,
    sat_min,
):
    city = mo.ui.dropdown(
        options=cities_t,
        value=cities_t[0] if cities_t else None,
        label="City",
    )

    room_type = mo.ui.multiselect(
        options=room_types_t,
        value=room_types_t,  # default: all
        label="Room type",
    )

    bedrooms = mo.ui.multiselect(
        options=bedrooms_vals,
        value=bedrooms_vals,
        label="Bedrooms",
    )

    capacity = mo.ui.multiselect(
        options=capacity_vals,
        value=capacity_vals,
        label="Capacity (person_capacity)",
    )

    host_portfolio_t = mo.ui.multiselect(
        options=host_portfolios,
        value=host_portfolios,
        label="Host portfolio",
    )

    superhost_only = mo.ui.checkbox(value=False, label="Superhost only")

    price_t = mo.ui.range_slider(
        start=price_min_t,
        stop=price_max,
        value=(price_min_t, price_max),
        step=max(1.0, (price_max - price_min_t) / 200.0),
        label="Price range",
    )

    satisfaction_t = mo.ui.range_slider(
        start=sat_min,
        stop=sat_max,
        value=(sat_min, sat_max),
        step=max(0.1, (sat_max - sat_min) / 200.0),
        label="Guest satisfaction range",
    )

    cleanliness_t = mo.ui.range_slider(
        start=clean_min,
        stop=clean_max,
        value=(clean_min, clean_max),
        step=1,
        label="Cleanliness rating range",
    )

    mo.vstack(
        [
            mo.md("## Filters"),
            mo.hstack([city, superhost_only]),
            mo.hstack([price_t, satisfaction_t]),
            cleanliness_t,
            mo.hstack([room_type, host_portfolio_t]),
            mo.hstack([bedrooms, capacity]),
        ]
    )
    return (
        bedrooms,
        capacity,
        city,
        cleanliness_t,
        host_portfolio_t,
        price_t,
        room_type,
        satisfaction_t,
        superhost_only,
    )


@app.cell
def _(
    COL,
    bedrooms,
    capacity,
    city,
    cleanliness_t,
    df,
    host_portfolio_t,
    price_t,
    room_type,
    satisfaction_t,
    superhost_only,
):
    d = df.copy()

    if city.value is not None:
        d = d[d[COL["city"]] == city.value]

    if room_type.value:
        d = d[d[COL["room_type"]].isin(room_type.value)]

    if host_portfolio_t.value:
        d = d[d[COL["host_portfolio"]].isin(host_portfolio_t.value)]

    if bedrooms.value:
        d = d[d[COL["bedrooms"]].isin(bedrooms.value)]

    if capacity.value:
        d = d[d[COL["capacity"]].isin(capacity.value)]

    if superhost_only.value:
        d = d[d[COL["superhost"]] == True]

    p_lo, p_hi = price_t.value
    d = d[(d[COL["price"]] >= p_lo) & (d[COL["price"]] <= p_hi)]

    s_lo, s_hi = satisfaction_t.value
    d = d[(d[COL["guest_satisfaction"]] >= s_lo) & (d[COL["guest_satisfaction"]] <= s_hi)]

    c_lo, c_hi = cleanliness_t.value
    d = d[(d[COL["cleanliness"]] >= c_lo) & (d[COL["cleanliness"]] <= c_hi)]

    # ensure coordinates exist
    d = d.dropna(subset=[COL["lat"], COL["lon"]])

    d.shape
    return (d,)


@app.cell
def _(COL, d, mo, px):
    if d.empty:
        mo.md("No data for this filter combination.")
    else:
        fig_t = px.scatter_map(
            d,
            lat=COL["lat"],
            lon=COL["lon"],
            color=COL["room_type"],
            hover_name=COL["city"],
            hover_data={
                COL["price"]: True,
                COL["guest_satisfaction"]: True,
                COL["cleanliness"]: True,
                COL["capacity"]: True,
                COL["bedrooms"]: True,
                COL["host_portfolio"]: True,
                COL["superhost"]: True,
            },
            zoom=11,
            height=650,
        )

        # force constant dot size
        fig_t.update_traces(marker=dict(size=8))

        fig_t.update_layout(
            map_style="open-street-map",
            margin=dict(l=0, r=0, t=0, b=0),
        )
        fig_t
    return (fig_t,)


@app.cell
def _(fig_t):
    fig_t
    return


if __name__ == "__main__":
    app.run()
