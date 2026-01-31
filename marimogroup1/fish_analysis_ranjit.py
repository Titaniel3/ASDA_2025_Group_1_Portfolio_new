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
    from sklearn.linear_model import LogisticRegression
    import plotly.express as px
    from sklearn.metrics import accuracy_score, classification_report
    import plotly.graph_objects as go
    return (
        LogisticRegression,
        accuracy_score,
        classification_report,
        mo,
        np,
        pd,
        px,
        train_test_split,
    )


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
def _(
    LogisticRegression,
    X_test,
    X_train,
    accuracy_score,
    classification_report,
    y_test,
    y_train,
):
    from sklearn.preprocessing import StandardScaler
    from sklearn.pipeline import make_pipeline

    model = make_pipeline(
        StandardScaler(),
        LogisticRegression(max_iter=1000)
    )
    model.fit(X_train, y_train)

    pred = model.predict(X_test)

    print("Accuracy:", accuracy_score(y_test, pred))
    print(classification_report(y_test, pred))
    return (model,)


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
def _(height_in, len2_in, mo, model, np, pd, predict_btn, weight_in, width_in):

    # Stop execution until the button is clicked
    mo.stop(not predict_btn.value, mo.md("### Standing by... \n Fill the form and click **Predict**."))

    # 1. Define "Reasonable" limits based on your training data
    limits = {
        "Weight": 1700,
        "Height": 22,
        "Width": 12,
        "Length2": 68
    }

    # 2. Validation Check
    too_large = [k for k, v in {
        "Weight": weight_in.value, 
        "Height": height_in.value, 
        "Width": width_in.value, 
        "Length2": len2_in.value
    }.items() if v > limits.get(k, 100)]

    if too_large:
        result_display = mo.md(f"🛑 **Unreasonable Value!** The input for **{', '.join(too_large)}** is much larger than any fish in our records.")
    elif any(v <= 0 for v in [weight_in.value, height_in.value, width_in.value, len2_in.value]):
        result_display = mo.md("⚠️ **Missing Data:** Please ensure all measurements are greater than 0.")
    else:
        # 3. Data is valid -> Proceed to Prediction
        try:
            # Create the data row
            input_data = pd.DataFrame([{
                "Length2": len2_in.value,
                "Height": height_in.value,
                "Width": width_in.value,
                "Weight": weight_in.value
            }])

            # Predict Species
            prediction = model.predict(input_data)[0]
        
            # --- NEW: CALCULATE CONFIDENCE SCORE ---
            # predict_proba returns a list of probabilities (e.g., [0.1, 0.8, 0.1])
            probs = model.predict_proba(input_data)[0]
            confidence = np.max(probs) * 100
            # ---------------------------------------

            # 4. Setup images
            fish_images = {
                "Bream": "images/Bream.jpg", "Roach": "images/roach.jpg",
                "Whitefish": "images/Lake_whitefish.jpg", "Parkki": "images/parrki.jpg",
                "Perch": "images/perch-fish.jpg", "Pike": "images/pike-fish-species.jpg", 
                "Smelt": "images/smelt.jpg"
            }

            img_path = fish_images.get(prediction, "")

            # 5. Build the Result Display
            # We use a color-coded span for the confidence score
            conf_color = "green" if confidence > 85 else "orange" if confidence > 50 else "red"
        
            result_display = mo.vstack([
                mo.md(f"## 🎉 Result: This is a **{prediction}**!"),
                mo.md(f"**Confidence Score:** <span style='color: {conf_color}; font-size: 1.2em;'>{confidence:.1f}%</span>"),
                mo.image(img_path) if img_path else mo.md("_Image not available_")
            ])

        except Exception as e:
            # Note: If this fails, make sure your model supports predict_proba (like RandomForest or LogisticRegression)
            result_display = mo.md(f"⚠️ **Error during prediction:** {e}")

    result_display
    return


@app.cell
def _(df, mo, px):
    counts = df['Species'].value_counts().reset_index()
    counts.columns = ['Species', 'Count']

    fig1 = px.bar(
        counts, 
        x='Species', 
        y='Count', 
        color='Species',
        title="<b>Total Samples per Species</b>",
        text_auto=True,
        template="plotly_white"
    )

    mo.md(f"### 📊 Dataset Balance\n{mo.as_html(fig1)}")
    return


@app.cell
def _(df, mo, px):
    fig2 = px.scatter(
        df, 
        x="Length2", 
        y="Weight", 
        color="Species",
        symbol="Species",
        title="<b>Weight vs. Length Growth Curve</b>",
        labels={"Length2": "Length (cm)", "Weight": "Weight (g)"}, 
        template="plotly_white"
    )

    mo.md(f"### 📈 Growth Trends\n{mo.as_html(fig2)}")
    return


@app.cell
def _(df, mo, px):
    fig3 = px.box(
        df, 
        x="Species", 
        y="Height", 
        color="Species",
        title="<b>Height Variation by Species</b>", # Shows confidence interval around the median
        template="plotly_white"
    )

    mo.md(f"### 📏 Height Analysis\n{mo.as_html(fig3)}")
    return


@app.cell
def _(df1, mo, px):


    # Calculate correlation matrix for numeric columns
    corr = df1.select_dtypes(include=['number']).corr()

    fig4 = px.imshow(
        corr, 
        text_auto=True, 
        aspect="auto",
        color_continuous_scale='RdBu_r',
        title="<b>Feature Correlation Heatmap</b>"
    )

    mo.md(f"### 🔗 Measurement Relationships\n{mo.as_html(fig4)}")
    return


if __name__ == "__main__":
    app.run()
