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
    return LinearRegression, pd, train_test_split


@app.cell
def _(pd):
    df = pd.read_csv("../datasets/Fish.csv") 
    return (df,)


@app.cell
def _(df):
    df
    return


@app.cell
def _(df):
    df1 = df.drop(["Length1", "Length3"], axis=1)

    return (df1,)


@app.cell
def _(df1, train_test_split):
    y = df1[["Species_Bream", "Species_Parkki", "Species_Perch","Species_Pike", "Species_Roach", "Species_Smelt", "Species_Whitefish"]]
    X = df1[["Length2", "Height", "Width","sqrt_weight"]]   # example clean feature set

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,      # 20% test data
        random_state=42,    # reproducible
    )

    print("Train rows:", len(X_train))
    print("Test rows:", len(X_test))
    return X_test, X_train, y_train


@app.cell
def _(df):
    species_cols = [col for col in df.columns if col.startswith("Species_")]

    df["Species"] = df[species_cols].idxmax(axis=1).str.replace("Species_", "")

    return


@app.cell
def _(LinearRegression, X_train, y_train):
    # Train linear regression model on training data

    # Create the model
    model = LinearRegression()

    # Train (fit) the model on the training data
    model.fit(X_train, y_train)
    return (model,)


@app.cell
def _(X_test, model):
    y_pred = model.predict(X_test)
    return (y_pred,)


@app.cell
def _(y_pred):
    y_pred
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
