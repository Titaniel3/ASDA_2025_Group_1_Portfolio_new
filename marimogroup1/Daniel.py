import marimo

__generated_with = "0.19.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return


@app.cell
def _():
    x = 14
    return (x,)


@app.cell
def _(x):
    x
    return


if __name__ == "__main__":
    app.run()
