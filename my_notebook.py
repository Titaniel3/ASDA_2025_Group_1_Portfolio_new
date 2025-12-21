import marimo

__generated_with = "0.18.3"
app = marimo.App(width="medium")


@app.cell
def _():

    import marimo as mo
    import pandas as pd

    return mo, pd


@app.cell
def _(mo, pd):

    df = pd.read_csv("C:/Users/USER/Downloads/happy.csv")
    transformed_df = mo.ui.dataframe(df)
    transformed_df


    return


@app.cell
def _(mo):
    import pandas as pd

    df = pd.read_csv(
        "C:/Users/USER/Downloads/happy.csv")
    transformed_df = mo.ui.dataframe(df)
    transformed_df
    return (pd,)


@app.cell
def _(mo, pd):


    df1 = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    table = mo.ui.table(df1, selection="multi")
    table
    return (table,)


@app.cell
def _(table):
    # Cell 2 - display the selection
    table.value
    return


if __name__ == "__main__":
    app.run()
