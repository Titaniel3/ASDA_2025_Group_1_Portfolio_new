import marimo

__generated_with = "0.19.4"
app = marimo.App(width="medium")


@app.cell
def _():
    # --- Core / app ---
    import marimo as mo  # Interactive notebook/dashboard framework

    # --- Data handling ---
    import pandas as pd  # DataFrames
    import numpy as np   # Numeric utilities

    # --- Plotting (simple + beginner-friendly) ---
    import matplotlib.pyplot as plt  # Plots with matplotlib

    # --- Optional: ML / evaluation (handy for dashboards with simple models) ---
    from sklearn.model_selection import train_test_split  # Train/test split
    from sklearn.preprocessing import StandardScaler      # Feature scaling
    from sklearn.pipeline import Pipeline                 # Combine steps
    from sklearn.metrics import r2_score, mean_absolute_error, accuracy_score  # Metrics

    from sklearn.linear_model import LinearRegression, LogisticRegression  # Baseline models
    from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier  # Stronger models

    return (pd,)


@app.cell
def _(pd):
    # --- Load dataset ---
    data_path = "../datasets/Fish_final.xlsx"  # Path relative to marimogroup1
    df = pd.read_excel(data_path)

    # Quick check
    df.head()

    return


if __name__ == "__main__":
    app.run()
