import marimo

__generated_with = "0.19.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd 
    return (pd,)


@app.cell
<<<<<<< HEAD
def _(pd):
    url = "https://docs.google.com/spreadsheets/d/1ecopK6oyyb4d_7-QLrCr8YlgFrCetHU7-VQfnYej7JY/export?format=xlsx"
    dataset = pd.ExcelFile(url, engine='openpyxl')

    sheets = []
    for sheet in dataset.sheet_names:
        df = dataset.parse(sheet)
        df["City"] = sheet #adding a column to track from which group is the data
        sheets.append(df)

    df = pd.concat(sheets, ignore_index=True)
    return (df,)
=======
def _():
    x=15
    return (x,)
>>>>>>> 1223547381cab8efb28912e1da363081eaaea635


@app.cell
def _(df):
    df
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
