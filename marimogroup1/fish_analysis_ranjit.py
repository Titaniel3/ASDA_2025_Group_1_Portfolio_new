import marimo

__generated_with = "0.19.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    import numpy as np
    import seaborn as sns
    import matplotlib.pyplot as plt

    import scipy.stats as stats


    from statsmodels.stats.outliers_influence import variance_inflation_factor

    from sklearn.model_selection import train_test_split

    from sklearn.linear_model import LinearRegression

    from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score



    import statsmodels.api as sm

    from sklearn.model_selection import train_test_split
    return (pd,)


@app.cell
def _(pd):
    df = pd.read_excel("../datasets/Fish_final.xlsx") 
    return (df,)


@app.cell
def _(df):
    df
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
