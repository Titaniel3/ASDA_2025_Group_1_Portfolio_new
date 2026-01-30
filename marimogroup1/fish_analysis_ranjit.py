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


    model = LogisticRegression(max_iter=1000,class_weight="balanced")
    model.fit(X_train, y_train)

    pred = model.predict(X_test)

    print("Accuracy:", accuracy_score(y_test, pred))
    print(classification_report(y_test, pred))
    return accuracy_score, classification_report, model


@app.cell
def _(X_test, X_train, accuracy_score, classification_report, y_test, y_train):
    from sklearn.ensemble import RandomForestClassifier

    rf = RandomForestClassifier(n_estimators=200,random_state=42)
    rf.fit(X_train, y_train)

    pred_rf = rf.predict(X_test)

    print("Accuracy:", accuracy_score(y_test, pred_rf))
    print(classification_report(y_test, pred_rf,zero_division=0))
    return


@app.cell
def _(mo):
    length_input = mo.ui.number(label="Length2 (cm)")
    height_input = mo.ui.number(label="Height (cm)")
    width_input  = mo.ui.number(label="Width (cm)")

    predict_btn = mo.ui.button(label="🔮 Predict Fish")

    mo.vstack([length_input, height_input, width_input, predict_btn])
    return height_input, length_input, predict_btn, width_input


@app.cell
def _(height_input, length_input, mo, model, pd, predict_btn, width_input):

    fish_images = {
        "Bream": "images/Bream.jpg",
        "Perch": "images/perch-fish.jpg",
        "Pike": "images/pike-fish-species.jpg",
        "Roach": "images/roach.gif",
        "Smelt": "images/smelt.jpg",
        "Parkki": "images/parrki.jpg",
        "Whitefish": "images/Lake_whitefish.jpg"
    }

    output = mo.md("Enter values and click Predict")

    if predict_btn.value:

        if None not in (length_input.value, height_input.value, width_input.value):
            sample = pd.DataFrame([{
                "Length2": length_input.value,
                "Height": height_input.value,
                "Width": width_input.value
            }])

            species = model.predict(sample)[0]
            img_path = fish_images.get(species, "")

            output = mo.vstack([
                mo.md(f"## 🐟 Predicted Species: **{species}**"),
                mo.image(img_path)
            ])
        else:
            output = mo.md("⚠️ Please enter all measurements.")

    output

    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
