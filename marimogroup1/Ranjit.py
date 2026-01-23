import marimo

__generated_with = "0.19.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd 
    import marimo as mo
    import matplotlib.pyplot as plt
    return mo, pd, plt


@app.cell
def _(pd):
    df = pd.read_csv("../datasets/airbnb_cleaned.csv")
    return (df,)


@app.cell
def _(df):
    cities = sorted(df["City"].unique())
    room_types = sorted(df["room_type"].unique())
    host_portfolio = sorted(df["host_portfolio"].unique())
    return cities, host_portfolio, room_types


@app.cell
def _(cities, mo):
    selected_cities = mo.ui.multiselect(
        options=cities,
        value=cities,
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
    fig, ax = plt.subplots(figsize=(10, 5))

    ax.bar(
        room_share.index,
        room_share.values
    )

    ax.set_title(f"Share of {selected_room_type.value} by City")
    ax.set_ylabel("Share")
    ax.set_ylim(0, 1)
    ax.tick_params(axis="x", rotation=45)
    return ax, fig


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
def _(df, mo):

    # UI CONTROL
    # ----------------------------------

    max_capacity = int(df["person_capacity"].max())

    capacity_slider = mo.ui.slider(
        start=1,
        stop=max_capacity,
        value=max_capacity,
        step=1,
        label="Maximum Person Capacity"
    )
    return (capacity_slider,)


@app.cell
def _(capacity_slider, df):

    # ----------------------------------
    # DATA FILTERING
    # ----------------------------------

    filtered_df3 = df[df["person_capacity"] <= capacity_slider.value]

    capacity_counts = (
        filtered_df3["person_capacity"]
        .value_counts()
        .sort_index()
    )
    return (capacity_counts,)


@app.cell
def _(ax, capacity_counts, plt):
    # ----------------------------------
    # PLOT
    # ----------------------------------

    figure4, ax4 = plt.subplots(figsize=(10, 5))

    capacity_counts.plot(
        kind="bar",
        ax=ax4
    )

    ax.set_title("Number of Listings by Person Capacity")
    ax.set_xlabel("Person Capacity")
    ax.set_ylabel("Number of Listings")
    plt.close(figure4)
    return (figure4,)


@app.cell
def _(capacity_slider, figure4, mo):
    # ----------------------------------
    # DASHBOARD LAYOUT
    # ----------------------------------

    mo.vstack([
        mo.md("## Listings by Person Capacity"),
        mo.hstack([
            capacity_slider,
            figure4])
        ])
    return


if __name__ == "__main__":
    app.run()
