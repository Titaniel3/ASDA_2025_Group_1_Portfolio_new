import marimo

__generated_with = "0.19.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    import numpy as np
    import seaborn as sns
    import matplotlib.pyplot as plt
    import marimo as mo

    import scipy.stats as stats


    from statsmodels.stats.outliers_influence import variance_inflation_factor

    from sklearn.model_selection import train_test_split

    from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score



    import statsmodels.api as sm

    from sklearn.model_selection import train_test_split
    return mo, pd, train_test_split


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
    y = df1["Species"]
    X = df1[["Length2", "Height", "Width"]]   # example clean feature set

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,      # 20% test data
        random_state=42,    # reproducible
    )

    print("Train rows:", len(X_train))
    print("Test rows:", len(X_test))
    return X_test, X_train, y_test, y_train


@app.cell
def _(X_test, X_train, y_test, y_train):
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score, classification_report


    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    pred = model.predict(X_test)

    print("Accuracy:", accuracy_score(y_test, pred))
    print(classification_report(y_test, pred))

    return (accuracy_score,)


@app.cell
def _(X_test, X_train, accuracy_score, y_test, y_train):
    from sklearn.ensemble import RandomForestClassifier

    rf = RandomForestClassifier(n_estimators=200, random_state=42)
    rf.fit(X_train, y_train)

    pred_rf = rf.predict(X_test)

    print("Accuracy:", accuracy_score(y_test, pred_rf))

    return (rf,)


@app.cell
def _(mo, pd, rf):
    length = mo.ui.slider(20, 50, label="Length2")
    height = mo.ui.slider(5, 20, label="Height")
    width = mo.ui.slider(2, 10, label="Width")

    def predict_species():
        sample = pd.DataFrame([{
            "Length2": length.value,
            "Height": height.value,
            "Width": width.value
        }])
        return rf.predict(sample)[0]   # or model.predict()



    return


if __name__ == "__main__":
    app.run()
