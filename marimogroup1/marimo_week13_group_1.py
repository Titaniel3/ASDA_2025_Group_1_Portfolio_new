import marimo

__generated_with = "0.19.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return


@app.cell
def _():
    x=5
    return (x,)


@app.cell
def _(x):
    y=4

    print(x+y)
    return


if __name__ == "__main__":
    app.run()
