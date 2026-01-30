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
    X = df1[["Length2", "Height", "Width","Weight"]]   # example clean feature set

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
    return accuracy_score, classification_report


@app.cell
def _(X_test, X_train, accuracy_score, classification_report, y_test, y_train):
    from sklearn.ensemble import RandomForestClassifier

    rf = RandomForestClassifier(n_estimators=200,random_state=42)
    rf.fit(X_train, y_train)

    pred_rf = rf.predict(X_test)

    print("Accuracy:", accuracy_score(y_test, pred_rf))
    print(classification_report(y_test, pred_rf,zero_division=0))
    return (rf,)


@app.cell
def _(mo):
    # Header and Instructions
    header = mo.md("""
        # 🐟 Fish Species Predictor
        *Enter measurements within the normal range of our database.*
    """)

    # We set 'stop' limits based on your training data (e.g., max weight was 1650)
    weight_in = mo.ui.number(label="Weight (g)", start=0, stop=1700, value=0, step=1)
    len2_in = mo.ui.number(label="Length (cm)", start=0, stop=68, value=0, step=0.1)
    height_in = mo.ui.number(label="Height (cm)", start=0, stop=20, value=0, step=0.1)
    width_in = mo.ui.number(label="Width (cm)", start=0, stop=10, value=0, step=0.1)

    predict_btn = mo.ui.run_button(label="🔮 Predict Species")

    # Layout the form
    form = mo.vstack([
        header,
        mo.hstack([weight_in, len2_in], justify="start"),
        mo.hstack([height_in, width_in], justify="start"),
        predict_btn
    ])

    form
    return height_in, len2_in, predict_btn, weight_in, width_in


@app.cell
def _(height_in, len2_in, mo, pd, predict_btn, rf, weight_in, width_in):
    # Stop execution until the button is clicked
    mo.stop(not predict_btn.value, mo.md("### Standing by... \n Fill the form and click **Predict**."))

    # 1. Define "Reasonable" limits based on your training data
    # Max Weight was 1650, Max Height ~19, Max Width ~8
    limits = {
        "Weight": 1700,
        "Height": 22,
        "Width": 12,
        "Length2": 68
    }

    # 2. Validation Check
    # We check if any input is significantly higher than our training data
    too_large = [k for k, v in {
        "Weight": weight_in.value, 
        "Height": height_in.value, 
        "Width": width_in.value, 
        "Length2": len2_in.value
    }.items() if v > limits.get(k, 100)]

    if too_large:
        result_display = mo.md(f"🛑 **Unreasonable Value!** The input for **{', '.join(too_large)}** is much larger than any fish in our records. Please enter a realistic measurement.")
    elif any(v <= 0 for v in [weight_in.value, height_in.value, width_in.value, len2_in.value]):
        result_display = mo.md("⚠️ **Missing Data:** Please ensure all measurements are greater than 0.")
    else:
        # 3. Data is valid -> Proceed to Prediction
        try:
            # Create the data row (Ensure column order matches your model.fit order)
            input_data = pd.DataFrame([{
                "Length2": len2_in.value,
                "Height": height_in.value,
                "Width": width_in.value,
                "Weight": weight_in.value
            }])

            prediction = rf.predict(input_data)[0]
        
            # 4. Setup images
            fish_images = {
                "Bream": "images/Bream.jpg", "Roach": "images/roach.jpg",
                "Whitefish": "images/Lake_whitefish.jpg", "Parkki": "images/parrki.jpg",
                "Perch": "images/perch-fish.jpg", "Pike": "images/pike-fish-species.jpg", 
                "Smelt": "images/smelt.jpg"
            }
        
            img_path = fish_images.get(prediction, "")

            # 5. Show Result
            result_display = mo.vstack([
                mo.md(f"## 🎉 Result: This is a **{prediction}**!"),
                mo.image(img_path) if img_path else mo.md("_Image not available_")
            ])
        
        except Exception as e:
            result_display = mo.md(f"⚠️ **Error during prediction:** {e}")

    result_display
    return


if __name__ == "__main__":
    app.run()
