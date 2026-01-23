import marimo

__generated_with = "0.19.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    return (pd,)


@app.cell
def _():
    x = 15
    return (x,)


@app.cell
def _(x):
    x
    return


@app.cell
def _(pd):
    # Read Airbnb dataset using a relative path
    df = pd.read_csv("../datasets/airbnb_cleaned.csv")

    # Show first rows
    df.head()
    return


if __name__ == "__main__":
    app.run()
